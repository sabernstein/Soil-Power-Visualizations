import csv
from collections import defaultdict
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from datetime import datetime
#!/usr/bin/env python3
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Change according to date
dates = "2021_6_28-2022_3_10"
# #start_plot = datetime.datetime(2021,11,23,17)
# start_plot = datetime.date(2021,5,3)
# end_plot = datetime.date(2021,5,19)

# change according to cells
names = ["cell_5-6", "cell_7-8"]
fnames = [["Final_Data/Prelim_Studies_Data.csv"]]
vol_legend = [['Cell 1 volts', 'Cell 2 volts'],['Cell 3 volts', 'Cell 4 volts'],['Cell 5 volts', 'Cell 6 volts'],['Cell 7 volts', 'Cell 8 volts']]
amp_legend = [['Cell 1 amps', 'Cell 2 amps'],['Cell 3 amps', 'Cell 4 amps'],['Cell 5 amps', 'Cell 6 amps'],['Cell 7 amps', 'Cell 8 amps']]
p_legend = [['Cell 1', 'Cell 2'],['Cell 3', 'Cell 4'],['Cell 5', 'Cell 6'],['Cell 7', 'Cell 8']]

date_correction = ["soil_20160616-092735_8.csv"]

time_delta = {"soil_20160616-092735_8.csv": pd.to_timedelta('1951 days 06:08:00')}


for i in range(0,1):
    soil_data = None
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
    power1 = []
    for d in data['power1']:
        power1.append(1E6*d)

    power2 = []
    for d in data['power2']:
        power2.append(1E6*d)


columns = defaultdict(list) # each value in each column is appended to a list

with open('Final_Data/Prelim_Studies_VWC_Data_copy.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            if v != '':
                columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

x2 = columns['timestamp']

unix_time = []
for t in x2:
    unix_time.append(int(float(t)))

d0 = datetime.fromtimestamp(unix_time[0])
days = []
for d in unix_time:
    day = datetime.fromtimestamp(d)
    day_from_start = day-d0
    decimal_day = day_from_start.total_seconds()/(24 * 3600)
    days.append(decimal_day)

with open('Final_Data/Prelim_Studies_Data.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            if v != '':
                columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

x = columns['unix_time']

unix_time2 = []
for t in x:
    unix_time2.append(int(float(t)))

da0 = datetime.fromtimestamp(unix_time[0])
days2 = []
for d in unix_time2:
    day = datetime.fromtimestamp(d)
    day_from_start = day-da0
    decimal_day = day_from_start.total_seconds()/(24 * 3600)
    days2.append(decimal_day)

# This is our soil-specific calibration to convert from raw moisture measurements to 
# volumetric moisture values
def _raw_to_vm(rawBoi):
	# For lab incubated soil MFCs
        return (1.147e-9)*rawBoi**3 - (8.638e-6)*rawBoi**2 + (2.187e-2)*rawBoi - 1.821e1
	# For Unitarian Church rain garden soil
	#return (2.906e-9)*rawBoi**3 - (2.039e-5)*rawBoi**2 + (4.763e-2)*rawBoi - 3.683e1
    
vwc = columns['raw_VWC']
vwc_data = []
for i in range(0, len(vwc)):
    vwc_data.append(100*_raw_to_vm(float(vwc[i])))

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Filter requirements.
order = 6
fs = 1/60      # sample rate, Hz
cutoff = 1/(12*3600)  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)


# Demonstrate the use of the filter.
# First make some data to be filtered.
T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)
# new_v2 = np.array(v2_power)
# Filter the data, and plot both the original and filtered signals.
vwc_filtered = butter_lowpass_filter(vwc_data, cutoff, fs, order)
power1_filtered = butter_lowpass_filter(power1, cutoff, fs, order)
power2_filtered = butter_lowpass_filter(power2, cutoff, fs, order)
# for d in days:
#     if d < 0.02:
#         index = days.index(d)
#         print(str(vmc_filtered[index]) + " index: " + str(index))

# fig, ax1 = plt.subplots(figsize=(8, 8))
# ax2 = ax1.twinx()
# ax3 = ax1.twinx()

fig, (ax1, ax2) = plt.subplots(2)

# ax1.plot(x, y)
# ax2.plot(x, -y)


ax1.plot(days2[:1048555], power1_filtered, label = "Cell 1 Power", alpha = 1, color= "green")
ax1.plot(days2[:1048555], power2_filtered, label = "Cell 2 Power", alpha = 1, color= "blue")
ax2.plot(days[1800:], vwc_filtered[1800:], label = "VMC", alpha = 1, color= "red")
ax2.set_ylim(ymin=0)
ax2.set_ylim(ymax=80)
ax1.legend()
ax2.legend()
# ax3.legend()

for d in days:
    if d > 0.1 and d < 0.12:
        i = days.index(d)
        print("vwc is " + str(vwc_filtered[i]) + " at index " + str(i))

# ax.legend("upper left")

#import custom font
from matplotlib import font_manager
font_path = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
my_font = font_manager.FontProperties(fname=font_path, size=12)  # get the font based on the font_path, set font size

#set font type of x and y axis
# plt.ylabel('Volumetric Water Content', fontproperties=my_font)
ax2.set_ylabel('Volumetric Water Content (%)', fontproperties=my_font)
ax1.set_ylabel('Power (µW)', fontproperties=my_font)
plt.xlabel('Timeline (Days)', fontproperties=my_font)

#set font type of tickmarks
for label in ax1.get_xticklabels():
    label.set_fontproperties(my_font)
for label in ax1.get_yticklabels():
    label.set_fontproperties(my_font)

#set font type of legend
# plt.legend(prop=my_font)
plt.show()