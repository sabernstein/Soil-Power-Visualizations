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

unix_time = []
for t in x2:
    unix_time.append(int(t))

h1 = columns['v4']
partial_h1_volt = []
for i in range(0, len(h1)):
    partial_h1_volt.append(float(h1[i]))

h2 = columns['v5']
partial_h2_volt = []
for i in range(0, len(h2)):
    partial_h2_volt.append(float(h2[i]))

h3 = columns['v6']
partial_h3_volt = []
for i in range(0, len(h3)):
    partial_h3_volt.append(float(h3[i]))

for d in x2:
    day = datetime.fromtimestamp(int(d))
    day_from_start = day-d0
    decimal_day = day_from_start.total_seconds()/(24 * 3600)
    partial_days.append(decimal_day)

i = 53050
start = 53050
end = 53051
start_day = 37.90353009259259
end_day = 44.71061342592593
days_to_add = geek.linspace(start_day, end_day, 9485, endpoint = False)

h1_slope = (partial_h1_volt[start]-partial_h1_volt[end])/(partial_days[start]-partial_days[end])
h1_volt_to_add = []

h2_slope = (partial_h2_volt[start]-partial_h2_volt[end])/(partial_days[start]-partial_days[end])
h2_volt_to_add = []

h3_slope = (partial_h3_volt[start]-partial_h3_volt[end])/(partial_days[start]-partial_days[end])
h3_volt_to_add = []

for d in days_to_add:
    h1_voltage = h1_slope*(d-partial_days[start])+partial_h1_volt[start]
    h1_volt_to_add.append(h1_voltage)

    h2_voltage = h2_slope*(d-partial_days[start])+partial_h2_volt[start]
    h2_volt_to_add.append(h2_voltage)

    h3_voltage = h3_slope*(d-partial_days[start])+partial_h3_volt[start]
    h3_volt_to_add.append(h3_voltage)

# days need to add days_to_add array into it after index 53050
# h2_volt need to add h2_volt_to_add array into it after index 53050

days_temp = list(partial_days[:53051])
days_temp2 = list(partial_days[53051:])
days_to_add = list(days_to_add)
days = days_temp + days_to_add + days_temp2 

h1_volt_temp = list(partial_h1_volt[:53051])
h1_volt_temp2 = list(partial_h1_volt[53051:])
h1_volt_to_add = list(h1_volt_to_add)
h1_volt = h1_volt_temp + h2_volt_to_add + h1_volt_temp2

h2_volt_temp = list(partial_h2_volt[:53051])
h2_volt_temp2 = list(partial_h2_volt[53051:])
h2_volt_to_add = list(h2_volt_to_add)
h2_volt = h2_volt_temp + h2_volt_to_add + h2_volt_temp2

h3_volt_temp = list(partial_h3_volt[:53051])
h3_volt_temp2 = list(partial_h3_volt[53051:])
h3_volt_to_add = list(h3_volt_to_add)
h3_volt = h3_volt_temp + h3_volt_to_add + h3_volt_temp2

v2 = columns['v2']
v2_volt = []
for i in range(0, len(v2)):
    v2_volt.append(float(v2[i]))

# h3 = columns['v6']
# h3_volt = []
# for i in range(0, len(h3)):
#     h3_volt.append(float(h3[i]))

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

v2_power = []
for v in v2_volt:
    v2_power.append(v*(v/2000))

    
v1 = columns['Vertical 1']
v3 = columns['Vertical 3']
p1 = columns['Planar 1']
p2 = columns['Planar 2']
p3 = columns['Planar 3']

vertical_ave = []

planar_ave = []
v1_power = []
v3_power = []
p1_power = []
for v in h1_volt:
    p1_power.append(v*(v/2000))
p2_power = []
for v in h2_volt:
    p2_power.append(v*(v/2000))
p3_power = []
for v in h3_volt:
    p3_power.append(v*(v/2000))
for i in range(0, len(v3)):
    v1_power.append(float(v1[i]))
    v3_power.append(float(v3[i]))

for i in range(0, len(v3_power)):
    vertical_ave.append((v1_power[i] + v2_power[i] + v3_power[i])/3)
    planar_ave.append((p1_power[i] + p2_power[i] + p3_power[i])/3)

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
y4 = butter_lowpass_filter(p1_power, cutoff, fs, order)
y5 = butter_lowpass_filter(p2_power, cutoff, fs, order)
y6 = butter_lowpass_filter(p3_power, cutoff, fs, order)
v_ave = butter_lowpass_filter(vertical_ave, cutoff, fs, order)
p_ave = butter_lowpass_filter(planar_ave, cutoff, fs, order)

# # plot line
fig, ax = plt.subplots()
# ax.plot(days[:105102], v_ave[:105102], label = "Vertical Average", alpha = 1, color= (0,0.1,1))
# ax.plot(days[:105102], y1[:105102], label = "Vertical 1", alpha = 0.2, color= (0,0.2,0.5))
# # FOR TESTING plt.plot(days[:105102], v2_power[:105102], label = "Vertical 2", alpha = 0.2, color= (0,0.4,0.5))
# ax.plot(days[:105102], y2[:105102], label='Vertical 2', alpha = 1, color= (0,0.4,0.5))
# # ax.plot(days[:105102], h2_volt[:105102], label='Horizontal 2 Raw Voltage', alpha = 1, color= (1,0,0))
# ax.plot(days[:105102], y3[:105102], label = "Vertical 3", alpha = 0.2, color= (0,0.6,0.5))

# ax.plot(days[:105102], p_ave[:105102], label = "Horizontal Average", alpha = 1, color= (1,0.1,0))
ax.plot(days[:105102], y4[:105102], label = "Horizontal 1", alpha = 1, color= (0.5,0.2,0))
ax.plot(days[:105102], y5[:105102], label = "Horizontal 2", alpha = 1, color="red")
ax.plot(days[:105102], y6[:105102], label = "Horizontal 2", alpha = 1, color= (0.5,0.4,0))
# ax.plot(days[:105102], p3_power[:105102], label = "Horizontal 3", alpha = 0.2, color= (0.5,0.6,0))
ax.legend("upper left")

#example of vertical line plotting
# ax.axvspan(8, 14, alpha=0.5, color='red')
# started drying cells'
plt.axvline(x = 50.153796, alpha = 0.2, color = 'yellow')
# label = 'reflooded cells'
plt.axvspan(50, 58.886458, color = 'yellow', alpha = 0.2)
# label = 'started drying again'
plt.axvspan(74.551516, 85, color = 'yellow', alpha = 0.2)

#import custom font
from matplotlib import font_manager
font_path = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
my_font = font_manager.FontProperties(fname=font_path, size=12)  # get the font based on the font_path, set font size

#set font type of x and y axis
plt.ylabel('Power (µW)', fontproperties=my_font)
plt.xlabel('Variation 2 Timeline (Days)', fontproperties=my_font)

#set font type of tickmarks
for label in ax.get_xticklabels():
    label.set_fontproperties(my_font)
for label in ax.get_yticklabels():
    label.set_fontproperties(my_font)

#set font type of legend
plt.legend(prop=my_font)
plt.show()
