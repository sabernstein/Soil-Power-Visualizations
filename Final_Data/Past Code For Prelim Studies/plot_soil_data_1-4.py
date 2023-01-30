#!/usr/bin/env python3
import matplotlib as mpl
mpl.use('Agg')
font= {'family': 'Arial',
        'size': 8}
mpl.rc('font', **font)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as md
import datetime
import numpy as np
from pytz import timezone
import pandas as pd
from glob import glob
import arrow
import os
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Change according to date
dates = "2021_6_28-2022_3_10"
#start_plot = datetime.datetime(2021,11,23,17)
start_plot = datetime.date(2021,5,3)
end_plot = datetime.date(2021,5,19)

# change according to cells
names = ["cell_5-6", "cell_7-8"]
#soil_20210421-151655_2.csv
#soil_20210628-132731_6.csv
fnames = [["Final_Data/Prelim_Studies_Data.csv"]]#, "D:/Research/IMWUT 2022 Paper/Data/Preliminary Study/soil_20210628-152118_2.csv"]]
# cell 1 and 2: 20210628, 20210813
# cell 3 and 4: 20210503, 20210813
# cell 5 and 6: starting on 20210628,20210716,20210813
# Cell 7 and 8: starting on 20210628, 20210816, 20210831
vol_legend = [['Cell 1 volts', 'Cell 2 volts'],['Cell 3 volts', 'Cell 4 volts'],['Cell 5 volts', 'Cell 6 volts'],['Cell 7 volts', 'Cell 8 volts']]
amp_legend = [['Cell 1 amps', 'Cell 2 amps'],['Cell 3 amps', 'Cell 4 amps'],['Cell 5 amps', 'Cell 6 amps'],['Cell 7 amps', 'Cell 8 amps']]
p_legend = [['Cell 1', 'Cell 2'],['Cell 3', 'Cell 4'],['Cell 5', 'Cell 6'],['Cell 7', 'Cell 8']]

date_correction = ["soil_20160616-092735_8.csv"]
#time_delta = pd.to_timedelta('1882 days 04:00:00')

time_delta = {"soil_20160616-092735_8.csv": pd.to_timedelta('1951 days 06:08:00')}

# Set color and style
volt_color= 'tab:blue'
amp_color = 'tab:red'

volt_color1= 'tab:blue'
volt_style1 = 'dashed'
volt_color2= 'tab:green'
volt_style2 = 'dotted'

amp_color1 = 'tab:red'
amp_style1='dashed'
amp_color2 = 'tab:orange'
amp_style2='dashdot'

for i in range(0,1):
    #new_pkl = f"../pkl/soil_data_{names[i]}_{dates}.pkl"
    soil_data = None
    # plot name
    # plot_name = f"D:/Research/IMWUT 2022 Paper/Data/Preliminary Study/{names[i]}_{dates}_zoomin.png"
    for fname in fnames[i]:
        print(fname)
        data = np.genfromtxt(fname, dtype=float, delimiter=',',skip_header=11, invalid_raise=False)
        data = pd.DataFrame({'timestamp':pd.to_datetime(data[:,0], unit='s'), 
                         'current1':np.abs(data[:,4]*10E-12), 
                         'voltage1':np.abs(data[:,5]*10E-9), 
                         'current2':np.abs(data[:,7]*10E-12), 
                         'voltage2':np.abs(data[:,8]*10E-9)})
        if fname in date_correction:
            data.timestamp = data.timestamp.dt.tz_localize('UTC').dt.tz_convert('US/Central') + time_delta[fname]
        else:
            data.timestamp = data.timestamp.dt.tz_localize('UTC').dt.tz_convert('US/Central')
        data['power1'] = np.abs(np.multiply(data['current1'], data['voltage1']))
        data['power2'] = np.abs(np.multiply(data['current2'], data['voltage2']))
        data.set_index('timestamp', inplace=True)
        print(f"{fname} starts from {data.index[0]}; {fname} ends at {data.index[-1]}.\n")
        if soil_data is None:
            soil_data = data
        else:
            soil_data = pd.concat([soil_data, data])
    #soil_data.to_pickle(new_pkl)

    # moving average
    mv = soil_data.rolling(5*60).mean()
    print(f"Starting time:{mv.index[0]}")
    print(f"Last recorded time:{mv.index[-1]}")
    plt.close()
    plt.xlabel("Time")
    fig, (ax1, ax3) = plt.subplots(2,figsize=(4,2), sharex=True)
    fig.autofmt_xdate()

    # Plot1, voltage axis
    ax1.set_ylabel('Cell Voltage (V)')
    ax1.plot(mv.index, mv['voltage1'], color=volt_color1, ls=volt_style1)
    ax1.plot(mv.index, mv['voltage2'], color=volt_color2, ls=volt_style2)
    ax1.tick_params(axis='y', labelcolor=volt_color1)
    #ax1.set_ylim(0, 2)

    ax1.set_xlim(start_plot, end_plot)

    # Plot1, current axis
    ax2 = ax1.twinx()
    ax2.set_ylabel('Cell Current (μA)')
    ax2.plot(mv.index, 1E6*mv['current1'], color=amp_color1, ls=amp_style1)
    ax2.plot(mv.index, 1E6*mv['current2'], color=amp_color2, ls=amp_style2)
    ax2.tick_params(axis='y', labelcolor=amp_color1)
    #ax2.set_ylim(0,500)

    ax1.tick_params(axis='x', which='both', length=0)
    ax2.tick_params(axis='x', which='both', length=0)

    ax1.grid(True)
    ax1.legend(vol_legend[i], loc='upper left', prop={'size': 6})
    ax2.legend(amp_legend[i], loc='upper center' , prop={'size': 6})

    ax3.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
    ax3.set_ylabel("Power (μW)")
    ax3.grid(True)

    #ax3.set_ylim(0,200)
    ax3.plot(mv.index, 1E6*mv['power1'], color=volt_color1, ls = volt_style1)
    ax3.plot(mv.index, 1E6*mv['power2'], color=volt_color2, ls = volt_style2)
    ax3.legend(p_legend[i], loc='upper left', prop={'size': 6})
    ax3.tick_params(axis='x', labelsize=6, rotation=30)
    ax3.set_xlim(start_plot, end_plot)

    for label in ax3.get_xticklabels():
        label.set_horizontalalignment('center')

    plt.tight_layout(pad=0.6, w_pad=0.5, h_pad=0.6)
    plt.subplots_adjust(hspace=0.15)
    plt.savefig(plot_name, dpi = 300)
    plt.close()

    tot_energy = np.trapz(soil_data['power1'])
    print(tot_energy)
    tot_energy = np.trapz(soil_data['power2'])
    print(tot_energy)
    print((soil_data.tail(1).index - soil_data.head(1).index).total_seconds())

    
