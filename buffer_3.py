import csv
from collections import defaultdict
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from datetime import datetime

columns = defaultdict(list) # each value in each column is appended to a list

with open('Final_Data/V3SensorData.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            if v != '':
                columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

x2 = columns['unix_time']

unix_time = []
for t in x2:
    unix_time.append(int(float(t)))

# for t in unix_time:
#     if datetime.fromtimestamp(t).day == 30 and datetime.fromtimestamp(t).month == 1:
#         print(datetime.fromtimestamp(t))
#         print(unix_time.index(t))


d0 = datetime.fromtimestamp(unix_time[0])
days = []
for d in unix_time:
    day = datetime.fromtimestamp(d)
    day_from_start = day-d0
    decimal_day = day_from_start.total_seconds()/(24 * 3600)
    days.append(decimal_day)

v1 = columns['v0']
v2 = columns['v1']
v3 = columns['v2']
p1 = columns['v3']
p2 = columns['v4']
p3 = columns['v5']

v1_volt = []
v2_volt = []
v3_volt = []
p1_volt = []
p2_volt = []
p3_volt = []
for i in range(0, len(v3)):
    v1_volt.append(float(v1[i]))
    v2_volt.append(float(v2[i]))
    v3_volt.append(float(v3[i]))
    p1_volt.append(float(p1[i]))
    p2_volt.append(float(p2[i]))
    p3_volt.append(float(p3[i]))


v1_power = []
for v in v1_volt:
    v1_power.append(v*(v/2000))

v2_power = []
for v in v2_volt:
    v2_power.append(v*(v/2000))

v3_power = []
for v in v3_volt:
    v3_power.append(v*(v/2000))

p1_power = []
for v in p1_volt:
    p1_power.append(v*(v/2000))

p2_power = []
for v in p2_volt:
    p2_power.append(v*(v/2000))

p3_power = []
for v in p3_volt:
    p3_power.append(v*(v/2000))

vertical_ave = []
planar_ave = []

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
ax.plot(days, v_ave, label = "Vertical Average", alpha = 1, color= (0,0.1,1))
ax.plot(days, y1, label = "Vertical 1", alpha = 0.2, color= (0,0.2,0.5))
ax.plot(days, y2, label='Vertical 2', alpha = 0.2, color= (0,0.4,0.5))
ax.plot(days, y3, label = "Vertical 3", alpha = 0.2, color= (0,0.6,0.5))

ax.plot(days, p_ave, label = "Horizontal Average", alpha = 1, color= (1,0.1,0))
ax.plot(days, y4, label = "Horizontal 1", alpha = 0.2, color= (0.5,0.2,0))
ax.plot(days, y5, label = "Horizontal 2", alpha = 0.2, color= (0.5,0.4,0))
ax.plot(days, y6, label = "Horizontal 3", alpha = 0.2, color= (0.5,0.6,0))
# ax.plot(days[:115102], v_ave[:115102],  alpha = 1, color= (0,0.1,1))
# ax.plot(days[:115102], y1[:115102],  alpha = 0.2, color= (0,0.2,0.5))
# ax.plot(days[:115102], y2[:115102], alpha = 0.2, color= (0,0.4,0.5))
# ax.plot(days[:115102], y3[:115102],  alpha = 0.2, color= (0,0.6,0.5))

# ax.plot(days[:115102], p_ave[:115102],  alpha = 1, color= (1,0.1,0))
# ax.plot(days[:115102], y4[:115102],  alpha = 0.2, color= (0.5,0.2,0))
# ax.plot(days[:115102], y5[:115102],  alpha = 0.2, color= (0.5,0.4,0))
# ax.plot(days[:115102], y6[:115102],  alpha = 0.2, color= (0.5,0.6,0))
# ax.legend(loc='upper left')
# ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
# fig.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
ax.legend("upper left")

# print(days[35048])
# print(days[64603])
#example of vertical line plotting
# ax.axvspan(8, 14, alpha=0.5, color='red')
# started drying cells'
# plt.axvline(x = 25.536006944444445, alpha = 0.2, color = 'yellow')
# # label = 'reflooded cells'
plt.axvspan(0, 25.536006944444445, color = 'blue', alpha = 0.1)
plt.axvspan(25.536006944444445, 46.53662037037037, color = 'yellow', alpha = 0.2)
plt.axvspan(46.53662037037037, 67.1998263888889, color = 'blue', alpha = 0.1)
plt.axvspan(67.1998263888889, 69.89245370370371, color = 'yellow', alpha = 0.2)


# # label = 'started drying again'
# plt.axvspan(74.551516, 85, color = 'yellow', alpha = 0.2)

#import custom font
from matplotlib import font_manager
font_path = './font/linux_libertine/LinLibertine_RB.ttf'  # the location of the font file
my_font = font_manager.FontProperties(fname=font_path, size=13)  # get the font based on the font_path, set font size

font_path2 = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
my_font2 = font_manager.FontProperties(fname=font_path2, size=13)  # get the font based on the font_path, set font size

#set font type of x and y axis
plt.ylabel('Power (µW)', fontproperties=my_font)
plt.xlabel('Timeline (Days)', fontproperties=my_font)

plt.text(11.17, 226.7, 'Flooded', size=18,  fontproperties=my_font)
plt.text(33.53, 226.7, 'Drying',  size=18, fontproperties=my_font)
plt.text(54.46, 226.7, 'Flooded',  size=18, fontproperties=my_font)

#set font type of tickmarks
for label in ax.get_xticklabels():
    label.set_fontproperties(my_font2)
for label in ax.get_yticklabels():
    label.set_fontproperties(my_font2)

#set font type of legend
plt.legend(loc="upper left", prop=my_font)
plt.show()