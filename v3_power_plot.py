import csv
from collections import defaultdict
import numpy as np
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
from datetime import datetime
#import custom font
from matplotlib import font_manager

columns = defaultdict(list) # each value in each column is appended to a list

with open('Final_Data/v3_Data.csv') as f:
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

d0 = datetime.fromtimestamp(unix_time[0])
days = []
for d in unix_time:
    day = datetime.fromtimestamp(d)
    day_from_start = day-d0
    decimal_day = day_from_start.total_seconds()/(24 * 3600)
    days.append(decimal_day)

soil = columns['soil_moisture']
vwc = []
for i in range(0, len(soil)):
    vwc.append(float(soil[i]))

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

#insert one last datapoint for day 74 to extend out flat lines for aesthetics purposes
y1 = np.insert(y1, len(y1), 0)
y2 = np.insert(y2, len(y2), 0)
y3 = np.insert(y3, len(y3), 0)
y4 = np.insert(y4, len(y4), 0)
y5 = np.insert(y5, len(y5), 0)
y6 = np.insert(y6, len(y6), 0)
v_ave = np.insert(v_ave, len(v_ave), 0)
p_ave = np.insert(p_ave, len(p_ave), 0)
days = np.insert(days, len(days), 74)

# # plot line
fig, ax = plt.subplots()
ax.plot(days, v_ave, label = "v3 Cell Avg.", alpha = 1, color= (0,0.1,1))
ax.plot(days, p_ave, label = "v0 Cell Avg.", alpha = 1, color= (1,0.1,0))

ax.plot(days, y1, label = "v3 Cell 1", alpha = 0.2, color= (0,0.2,0.5))
ax.plot(days, y4, label = "v0 Cell 1", alpha = 0.2, color= (0.5,0.2,0))

ax.plot(days, y2, label='v3 Cell 2', alpha = 0.2, color= (0,0.4,0.5))
ax.plot(days, y5, label = "v0 Cell 2", alpha = 0.2, color= (0.5,0.4,0))

ax.plot(days, y3, label = "v3 Cell 3", alpha = 0.2, color= (0,0.6,0.5))
ax.plot(days, y6, label = "v0 Cell 3", alpha = 0.2, color= (0.5,0.6,0))

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
plt.axvspan(67.1998263888889, 74, color = 'yellow', alpha = 0.2)
#plt.axvspan(67.1998263888889, 69.89245370370371, color = 'yellow', alpha = 0.2)

plt.axhline(y=20, color='green', linestyle="dashed") #number came from lowest MARS startup voltage (0.2V*0.2V)/2000 ohms = 20 uW
# # label = 'started drying again'
# plt.axvspan(74.551516, 85, color = 'yellow', alpha = 0.2)


font_path = './font/linux_libertine/LinLibertine_RB.ttf'  # the location of the font file
my_font = font_manager.FontProperties(fname=font_path, size=16)  # get the font based on the font_path, set font size

font_path2 = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
my_font2 = font_manager.FontProperties(fname=font_path2, size=22)  # get the font based on the font_path, set font size

#set font type of x and y axis
plt.ylabel('Power (µW)', fontproperties=my_font, size=22)
plt.xlabel('Timeline (Days)', fontproperties=my_font, size=22)

plt.text(1.02, 22, 'MARS', size=20,  color='green', fontproperties=my_font)
plt.text(9.17, 226.7, 'Flooded', size=20,  fontproperties=my_font)
plt.text(33.53, 226.7, 'Drying',  size=20, fontproperties=my_font)
plt.text(54.46, 226.7, 'Flooded',  size=20, fontproperties=my_font)
plt.text(67.5, 226.7, 'Drying',  size=20, fontproperties=my_font)

#set font type of tickmarks
for label in ax.get_xticklabels():
    label.set_fontproperties(my_font2)
for label in ax.get_yticklabels():
    label.set_fontproperties(my_font2)

#set font type of legend
# plt.legend(loc="lower left", bbox_to_anchor=(0.75,0.27), prop=my_font)
# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.18),
          fancybox=True, ncol=4, prop=my_font, frameon=False)

plt.show()