#!/usr/bin/env python3

# Written for the WaterSystems collaboration (UC Berkeley, Stanford, and Northwestern)
# by Alvin Tan on 11/16/2020

# Plots temperature, electric conductivity, and volumetric moisture values
# collected by a TEROS device
# Converts raw TEROS moisture data into volumetric moisture measurements
# (see TEROS 11/12 manual section 4 for more details on calibration:
#  http://publications.metergroup.com/Manuals/20587_TEROS11-12_Manual_Web.pdf)

import os
import ast
import argparse
import numpy as np
import pandas as pd
from glob import glob
import matplotlib as mpl
mpl.use('Agg')
font= {'family': 'Arial',
        'size': 8}
mpl.rc('font', **font)
from matplotlib import pyplot as plt
import matplotlib.dates as md
import datetime

# This is our soil-specific calibration to convert from raw moisture measurements to 
# volumetric moisture values
def _raw_to_vm(rawBoi):
	# For lab incubated soil MFCs
        return (1.147e-9)*rawBoi**3 - (8.638e-6)*rawBoi**2 + (2.187e-2)*rawBoi - 1.821e1
	# For Unitarian Church rain garden soil
	#return (2.906e-9)*rawBoi**3 - (2.039e-5)*rawBoi**2 + (4.763e-2)*rawBoi - 3.683e1

# A couple helper functions used to write metadata to save some time
def _write_set(set_boi, file_name):
	with open(file_name, "w") as f:
		f.write(str(set_boi))
	return	# an empty return here just to make me feel better about the 'with' statement

def _load_set(file_name):
	with open(file_name, 'r') as f:
		meta_set = ast.literal_eval(f.read())
	return meta_set

# Loads our data, squishes it around a bit, and saves it as a pickle 
def load_and_process_data(args):
	# set up some paths
	pkl_dir = os.path.join(args.dd, "pkls")					# directory to hold pickled data
	pkl_gen = os.path.join(pkl_dir, "*data*")
	pkl_file = os.path.join(pkl_dir, "teros_data.pkl")		# file name for pickled data
	pkl_meta = os.path.join(pkl_dir, "seen_datasets.txt")	# file name for list of pickled datasets
	
	data_gen = os.path.join(args.dd, args.dn)
	
	
	# make our pickles directory if it doesn't already exist
	os.makedirs(pkl_dir, exist_ok=True)
	
	# if we want to clear our original pickles, we delete the existing files
	if args.c:
		old_pkls = glob(pkl_gen)
		for pkl_name in old_pkls:
			os.remove(pkl_name)
	
	
	# instantiate a dataframe for our teros data and a list of filenames for the datasets 
	# in our data directory
	data_df = None
	new_datasets = set(glob(data_gen))
	old_datasets = set()
	
	# if we've already done data processing before, we can load in the previously processed
	# data and ignore any dataset files that we have already processed
	if os.path.exists(pkl_meta) and os.path.exists(pkl_file):
		data_df = pd.read_pickle(pkl_file)
		old_datasets = _load_set(pkl_meta)
		new_datasets -= old_datasets
	# Dictionary for logging start time (local)
	startlog_local = {"./TEROSoutput-1466275535-f7.csv": "2021-08-13 17:48:56.061292410-05:00",
                          "./TEROSoutput-1466087260-f8.csv": "2021-10-19 15:35:00-0500"}

	#dtypes = {'timestamp':np.int64, 'sensorID':np.int64, 'raw_VWC':np.float64, 'temp':np.float64, 'EC':np.int64}
	# now load in new datasets, squish them around a bit, and add them to our dataframe
	for data_name in sorted(new_datasets, key=lambda x: int(x.split('-')[-2])):
		print("Loading and processing data from '{}'".format(data_name))	# print the dataset we are loading in for debugging purposes
		new_data = pd.read_csv(data_name)#, dtype=dtypes)
		new_data['timestamp'] = pd.to_datetime(new_data['timestamp'], errors='coerce', unit='s')
		if data_name in startlog_local.keys():
			time_delta = pd.to_datetime(startlog_local[data_name]).tz_convert('US/Central') - new_data.timestamp.dt.tz_localize('UTC').dt.tz_convert('US/Central')[0]
			new_data.timestamp = new_data.timestamp.dt.tz_localize('UTC').dt.tz_convert('US/Central') + time_delta
		else:
			new_data['timestamp'] = new_data['timestamp'].dt.tz_localize('UTC').dt.tz_convert('US/Central')
		new_data.set_index('timestamp', inplace=True)

		print(new_data.index[0])
		print(new_data.index[-1])

		# do some quick data cleaning to make sure we are getting numbers
		for column in new_data:
			new_data[column] = pd.to_numeric(new_data[column], errors='coerce')
		
		# drop any NaN values from junky data
		new_data.dropna()
		
		# calculate our volumetric moisture values from raw moisture measurements
		new_data['VWC'] = _raw_to_vm(new_data['raw_VWC'])
		# would it be faster to concatenate all the new datasets together before doing
		# this operation?
		new_data_roll = split_and_rolling_average_data(new_data)
		# add our new data to the full dataframe
		data_df = pd.concat([data_df, new_data_roll])
		
	# if we added new datasets, then we should sort, pickle, and save our dataframe
	#if new_datasets:
		# Note: we loaded data in the order of dataset file creation time (done with the
		# 'sorted' function in the 'for' statement above), so we might not have to sort
		# the dataframe here (i.e. the dataframe may already be sorted by construction)
		#data_df.sort_index(inplace=True, kind='heapsort')
		
		#data_df.to_pickle(pkl_file)
		#print("Saved new pickled data to '{}'".format(pkl_file))
		#_write_set(old_datasets.union(new_datasets), pkl_meta)
		#print("Saved new pickle metadata to '{}'".format(pkl_meta))
	
	# if we didn't load any data at all, print something saying so
	#elif data_df is None:
		#print("No TEROS data found. Returning None")
	
	# otherwise we just loaded up some data we already processed and saved, so we
	# don't need to save anything again
	#else:
		#print("Loaded previously processed data from '{}'".format(pkl_file))

	# return our dataframe for the next function to use
	return data_df
	


# takes a dataframe containing data from only one sensor
# plots temperature, electrical current, and volumetric moisture values over time
# saves figures as png files in the designated directory
def _plot_and_save_data(args, data_df):
	# return if we got an empty dataframe
	if data_df is None or data_df.size == 0:
		return
	print(data_df['sensorID'].unique())
	# grab some descriptive information
	sensor_id = data_df['sensorID'].iat[0]
	data_df = data_df.sort_index()
	#start_time = data_df.index[0]
	#end_time = data_df.index[-1]
	start_time = datetime.datetime(2021,11,23,17)
	end_time = datetime.date(2022,1,9)
	
	# setup some paths
	fig_dir = os.path.join(args.dd, "figs")
	fig_file = os.path.join(fig_dir, "lab_soil_sensor-{}_from-{}_to-{}.{}".format(int(sensor_id), start_time, end_time, args.ft))
	# make the figures directory if it doesn't already exist
	os.makedirs(fig_dir, exist_ok=True)

	# make our plot
	plt.close()
	pd.plotting.register_matplotlib_converters()
	plt.xlabel("Time")
	fig, (ax1, ax3) = plt.subplots(2, figsize=(4, 2), sharex=True)
	fig.autofmt_xdate()

	temp_color = 'tab:purple'
	EC_color = 'tab:olive'
	VWC_color = 'tab:cyan'

	VWC_style = 'solid'
	EC_style = 'dashed'
	temp_style = 'solid'

	ax1.set_ylabel('VWC (%)')
	ax1.plot(data_df.index, data_df['VWC'], color=VWC_color, ls=VWC_style)
	ax1.tick_params(axis='y', labelcolor=VWC_color)
	ax1.set_ylim(0, 1)
	ax1.set_xlim(start_time,end_time)

	ax2 = ax1.twinx()
	ax2.set_ylabel('EC (mS/m)')
	ax2.plot(data_df.index, data_df['EC'], color=EC_color, ls=EC_style)
	ax2.tick_params(axis='y', labelcolor=EC_color)
	ax2.set_ylim(0, 1000)
	ax1.tick_params(axis='x', which='both', length=0)
	ax2.tick_params(axis='x', which='both', length=0)

	ax1.grid(True)
	ax1.legend(['Volumetric Water Content (VWC)'], loc='upper left', prop={'size': 6})
	ax2.legend(['Electrical Conductivity (EC)'], loc='upper right', prop={'size': 6})
	# Re-arrange legends, ensures data does not draw on top of them
	all_axes = fig.get_axes()
	for axis in all_axes:
		legend = axis.get_legend()
		if legend is not None:
			legend.remove()
			all_axes[-1].add_artist(legend)

	ax3.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
	ax3.set_ylabel("Temperature (C)")
	ax3.grid(True)
	ax3.set_ylim(0, 30)
	ax3.set_xlim(start_time,end_time)
	ax3.plot(data_df.index, data_df['temp'], color=temp_color, ls=temp_style)
	ax3.tick_params(axis='x', labelsize=6, rotation=0)
	for label in ax3.get_xticklabels():
		label.set_horizontalalignment('center')
	ax3.legend(['Temperature'], loc='lower center', prop={'size': 6})
	plt.tight_layout(pad=0.6, w_pad=0.5, h_pad=0.6)
	plt.subplots_adjust(hspace=0.15)
	plt.savefig(fig_file, dpi = 300)
	plt.close()
	print("Figure saved to '{}'".format(fig_file))

# takes a dataframe generated by load_and_process_data, takes out smaller dataframes based

# split dataframe according to different sensorID
def split_and_rolling_average_data(data_df):
	data_roll = None
	# get a list of sensor IDs in our dataframe
	sensor_ids = data_df['sensorID'].unique()
	# for each sensor, subset out the relevant data
	for sensor_id in sensor_ids:
		sensor_data = data_df.loc[data_df['sensorID']==sensor_id]
		# calculate the rolling average over a 5 minute window
		sensor_roll = sensor_data.rolling(5*6, min_periods=1).mean()
		sensor_roll.iloc[0:1,1:] = np.nan
		sensor_roll.iloc[-1:0, 1:] = np.nan
		data_roll = pd.concat([data_roll, sensor_roll])
	return data_roll

# on sensorID, and feeds said smaller dataframe to _plot_and_save_data to be visualized
def split_and_plot_data(args, data_df):
	# get a list of sensor IDs in our dataframe
	print("split_and_plot_data input data_df sensor ID:")
	print(data_df['sensorID'].unique())
	sensor_ids = data_df['sensorID'].unique()
	# for each sensor, subset out the relevant data and then plot and save said data 
	for sensor_id in sensor_ids:
		sensor_data = data_df.loc[data_df['sensorID']==sensor_id]
		_plot_and_save_data(args, sensor_data)
	print("Done plotting all the data in our dataframe")



# main function that parses out command line inputs and feeds it into the
# corresponding functions
if __name__ == "__main__":
	# describe the optional command line inputs we are looking for
	parser = argparse.ArgumentParser(description='Plot TEROS data')
	
	parser.add_argument('-dd', type=str, default="./",
						help="data directory (default is './')")
	
	parser.add_argument('-dn', type=str, default="TEROSoutput*.csv",
						help="datafile name (default is 'TEROSoutput*.csv')")
	
	parser.add_argument('-c', action='count', default=0,
						help="delete all existing pickles before processing data")
	
	parser.add_argument('-ft', type=str, default="png",
						help="figure type (default is 'png')")


	# parse out command line inputs
	args = parser.parse_args()

	# load in our data and put it in a dataframe
	data_df = load_and_process_data(args)

	# plot our data and save the plots 
	split_and_plot_data(args, data_df)

