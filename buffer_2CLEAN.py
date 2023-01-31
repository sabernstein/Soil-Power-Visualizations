import csv
import matplotlib.pyplot as plt
import numpy as geek
import numpy as np
from scipy.signal import butter, lfilter
from collections import defaultdict
from datetime import datetime

columns = defaultdict(list) 

with open('Final_Data/v2_Data.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            if v != '':
                columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

x2 = columns['unix_time']
d0 = datetime.fromtimestamp(int(x2[0]))
partial_days = []

for d in x2:
    day = datetime.fromtimestamp(int(d))
    day_from_start = day-d0
    decimal_day = day_from_start.total_seconds()/(24 * 3600)
    partial_days.append(decimal_day)

v1 = columns['v1']
v2 = columns['v2']
v3 = columns['v3']
h1 = columns['v4']
h2 = columns['v5']
h3 = columns['v6']

def string_to_float(voltage_column):
    partial_volt = []
    for i in range(0, len(voltage_column)):
        partial_volt.append(float(voltage_column[i]))
    return partial_volt

partial_v1_volt = string_to_float(v1)
partial_v2_volt = string_to_float(v2)
partial_v3_volt = string_to_float(v3)
partial_h1_volt = string_to_float(h1)
partial_h2_volt = string_to_float(h2)
partial_h3_volt = string_to_float(h3)

start1 = 53050
end1 = 53051
start_day = 37.90353009259259
end_day = 44.71061342592593
days_to_add = geek.linspace(start_day, end_day, 9485, endpoint = False)

def find_slope(start, end, partial_voltage):
    return (partial_voltage[start]-partial_voltage[end])/(partial_days[start]-partial_days[end])

v1_slope = find_slope(start1, end1, partial_v1_volt)
v2_slope = find_slope(start1, end1, partial_v2_volt)
v3_slope = find_slope(start1, end1, partial_v3_volt)
h1_slope = find_slope(start1, end1, partial_h1_volt)
h2_slope = find_slope(start1, end1, partial_h2_volt)
h3_slope = find_slope(start1, end1, partial_h3_volt)

def voltage_to_add(start, slope, partial_voltage):
    volt_to_add = []
    for d in days_to_add:
        voltage = slope*(d-partial_days[start])+partial_voltage[start]
        volt_to_add.append(voltage)
    return volt_to_add

v1_volt_to_add = voltage_to_add(start1, v1_slope, partial_v1_volt)
v2_volt_to_add = voltage_to_add(start1, v2_slope, partial_v2_volt)
v3_volt_to_add = voltage_to_add(start1, v3_slope, partial_v3_volt)
h1_volt_to_add = voltage_to_add(start1, h1_slope, partial_h1_volt)
h2_volt_to_add = voltage_to_add(start1, h2_slope, partial_h2_volt)
h3_volt_to_add = voltage_to_add(start1, h3_slope, partial_h3_volt)

def adding_arrays(partial_array, additions):
    temp = list(partial_array[:53051])
    temp2 = list(partial_array[53051:])
    to_add = list(additions)
    return temp + to_add + temp2 

days = adding_arrays(partial_days, days_to_add)
v1_volt = adding_arrays(partial_v1_volt, v1_volt_to_add)
v2_volt = adding_arrays(partial_v2_volt, v2_volt_to_add)
v3_volt = adding_arrays(partial_v3_volt, v3_volt_to_add)
h1_volt = adding_arrays(partial_h1_volt, h1_volt_to_add)
h2_volt = adding_arrays(partial_h2_volt, h2_volt_to_add)
h3_volt = adding_arrays(partial_h3_volt, h3_volt_to_add)

# fixing four major spikes 
i = 9731
start = 9730
end = 9759
slope = (v2_volt[start]-v2_volt[end])/(days[start]-days[end])
for v in v2_volt[start:end+1]:
    v2_volt[i] = slope*(days[i]-days[start])+v2_volt[start]
    i += 1

i = 60599
start = 60598
end = 60605
slope = (v2_volt[start]-v2_volt[end])/(days[start]-days[end])
for v in v2_volt[start:end+1]:
    v2_volt[i] = slope*(days[i]-days[start]) + v2_volt[start]
    i += 1

i = 64557
start = 64556
end = 64573
slope = (v2_volt[start]-v2_volt[end])/(days[start]-days[end])
for v in v2_volt[start:end+1]:
    v2_volt[i] = slope*(days[i]-days[start]) + v2_volt[start]
    i += 1

i = 70043
start = 70042
end = 70087
slope = (v2_volt[start]-v2_volt[end])/(days[start]-days[end])
for v in v2_volt[start:end+1]:
    v2_volt[i] = slope*(days[i]-days[start]) + v2_volt[start]
    i += 1

###

# 692.4 on day 50.75174768518519 at index 61424
# 461.14 on day 52.69890046296296 at index 61425
# 0.000717668248114478
start2 = 70909
end2 = 70910
start_day2 = 50.75174768518519
end_day2 = 52.69890046296296
days_to_add2 = geek.linspace(start_day2, end_day2, 2713, endpoint = False)
def find_slope2(start, end, partial_voltage):
    return (partial_voltage[start]-partial_voltage[end])/(days[start]-days[end])

v1_slope2 = find_slope2(start2, end2, v1_volt)
v2_slope2 = find_slope2(start2, end2, v2_volt)
v3_slope2 = find_slope2(start2, end2, v3_volt)
h1_slope2 = find_slope2(start2, end2, h1_volt)
h2_slope2 = find_slope2(start2, end2, h2_volt)
h3_slope2 = find_slope2(start2, end2, h3_volt)


def voltage_to_add2(start, slope, partial_voltage):
    volt_to_add = []
    for d in days_to_add2:
        voltage = slope*(d-days[start])+partial_voltage[start]
        volt_to_add.append(voltage)
    return volt_to_add

v1_volt_to_add2 = voltage_to_add2(start2, v1_slope2, v1_volt)
v2_volt_to_add2 = voltage_to_add2(start2, v2_slope2, v2_volt)
v3_volt_to_add2 = voltage_to_add2(start2, v3_slope2, v3_volt)
h1_volt_to_add2 = voltage_to_add2(start2, h1_slope2, h1_volt)
h2_volt_to_add2 = voltage_to_add2(start2, h2_slope2, h2_volt)
h3_volt_to_add2 = voltage_to_add2(start2, h3_slope2, h3_volt)


def adding_arrays2(partial_array, additions):
    temp = list(partial_array[:70910])
    temp2 = list(partial_array[70910:])
    to_add = list(additions)
    return temp + to_add + temp2 

days = adding_arrays2(days, days_to_add2)
v1_volt = adding_arrays2(v1_volt, v1_volt_to_add2)
v2_volt = adding_arrays2(v2_volt, v2_volt_to_add2)
v3_volt = adding_arrays2(v3_volt, v3_volt_to_add2)
h1_volt = adding_arrays2(h1_volt, h1_volt_to_add2)
h2_volt = adding_arrays2(h2_volt, h2_volt_to_add2)
h3_volt = adding_arrays2(h3_volt, h3_volt_to_add2)

#### 

def calc_power(voltage):
    power = []
    for v in voltage:
        power.append(v*(v/2000))
    return power 

v1_power = calc_power(v1_volt)
v2_power = calc_power(v2_volt)
v3_power = calc_power(v3_volt)
h1_power = calc_power(h1_volt)
h2_power = calc_power(h2_volt)
h3_power = calc_power(h3_volt)

for v in v2_volt:
    v2_power.append(v*(v/2000))

vertical_ave = []
planar_ave = []
for i in range(0, len(v3_power)):
    vertical_ave.append((v1_power[i] + v2_power[i] + v3_power[i])/3)
    planar_ave.append((h1_power[i] + h2_power[i] + h3_power[i])/3)

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
y1 = butter_lowpass_filter(v1_power, cutoff, fs, order)
y2 = butter_lowpass_filter(v2_power, cutoff, fs, order)
y3 = butter_lowpass_filter(v3_power, cutoff, fs, order)
y4 = butter_lowpass_filter(h1_power, cutoff, fs, order)
y5 = butter_lowpass_filter(h2_power, cutoff, fs, order)
y6 = butter_lowpass_filter(h3_power, cutoff, fs, order)
v_ave = butter_lowpass_filter(vertical_ave, cutoff, fs, order)
p_ave = butter_lowpass_filter(planar_ave, cutoff, fs, order)

# # plot line
fig, ax = plt.subplots()
ax.plot(days[:115102], v_ave[:115102], label = "Vertical Average", alpha = 1, color= (0,0.1,1))
ax.plot(days[:115102], y1[:115102], label = "Vertical 1", alpha = 0.2, color= (0,0.2,0.5))
ax.plot(days[:115102], y2[:115102], label='Vertical 2', alpha = 0.2, color= (0,0.4,0.5))
ax.plot(days[:115102], y3[:115102], label = "Vertical 3", alpha = 0.2, color= (0,0.6,0.5))
# ax.plot(days[:105102], h1_volt[:105102], label = "Horizontal 1 V", alpha = 1, color= (1, 0, 0))
ax.plot(days[:115102], p_ave[:115102], label = "Horizontal Average", alpha = 1, color= (1,0.1,0))
ax.plot(days[:115102], y4[:115102], label = "Horizontal 1", alpha = 0.2, color= (0.5,0.2,0))
ax.plot(days[:115102], y5[:115102], label = "Horizontal 2", alpha = 0.2, color="red")
ax.plot(days[:115102], y6[:115102], label = "Horizontal 3", alpha = 0.2, color= (0.5,0.4,0))
ax.legend("upper left")

# started drying cells'
# plt.axvspan(0, 25.536006944444445, label = "Flooded", color = 'blue', alpha = 0.1)
# plt.axvspan(25.536006944444445, 46.53662037037037, label = "Drying", color = 'yellow', alpha = 0.2)
# plt.axvspan(46.53662037037037, 61.43189814814815, color = 'blue', alpha = 0.1)
plt.axvspan(0, 50.153796,color = 'blue', alpha = 0.1)
# label = 'reflooded cells'
plt.axvspan(50, 58.886458, color = 'yellow', alpha = 0.2)
plt.axvspan(58.886458, 74.551516, color = 'blue', alpha = 0.1)
# label = 'started drying again'
plt.axvspan(74.551516, 85, color = 'yellow', alpha = 0.2)

#import custom font
from matplotlib import font_manager
font_path = './font/linux_libertine/LinLibertine_RB.ttf'  # the location of the font file
my_font = font_manager.FontProperties(fname=font_path, size=13)  # get the font based on the font_path, set font size

font_path2 = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
my_font2 = font_manager.FontProperties(fname=font_path2, size=13)  # get the font based on the font_path, set font size
#set font type of x and y axis
plt.ylabel('Power (µW)', fontproperties=my_font)
plt.xlabel('Timeline (Days)', fontproperties=my_font)
#adding text inside the plot
plt.text(22.11, 245.5, 'Flooded', fontsize = 18,  fontproperties=my_font)
plt.text(51.25, 245.5, 'Drying', fontsize = 18,  fontproperties=my_font)
plt.text(63, 245.5, 'Flooded', fontsize = 18,  fontproperties=my_font)
plt.text(76.5, 245.5, 'Drying', fontsize = 18,  fontproperties=my_font)
#set font type of tickmarks
for label in ax.get_xticklabels():
    label.set_fontproperties(my_font2)
for label in ax.get_yticklabels():
    label.set_fontproperties(my_font2)

#set font type of legend
plt.legend(prop=my_font)
plt.show()
