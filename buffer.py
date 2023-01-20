import csv
from collections import defaultdict
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from datetime import datetime

columns = defaultdict(list) # each value in each column is appended to a list

with open('Final_Data/v2_Data.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            if v != '':
                columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

x2 = columns['unix_time']
d0 = datetime.fromtimestamp(int(x2[0]))
days = []

unix_time = []
for t in x2:
    unix_time.append(int(t))

for d in x2:
    day = datetime.fromtimestamp(int(d))
    day_from_start = day-d0
    decimal_day = day_from_start.total_seconds()/(24 * 3600)
    days.append(decimal_day)

v2 = columns['v2']
v2_volt = []
for i in range(0, len(v2)):
    v2_volt.append(float(v2[i]))

# for i in range(0, len(v2_volt)):
#     if v2_volt[i] < 0:
#         v2_volt[i] = v2_volt[i]
#     if v2_volt[i] < -200:
#          v2_volt[i] = (v2_volt[i-1]+v2_volt[i+1])/2

# 1: 1655413184 to 1655414787 (about 27 minutes)
i = 9731
start = 9731
slope = (v2_volt[9757]-v2_volt[9731])/(days[9757]-days[9731])
for v in v2_volt[9731:9758]:
    v2_volt[i] = slope*(days[i]-days[start]) + v2_volt[9757]
    i += 1

# # 2
i = 60599
start = 60599
slope = (v2_volt[60604]-v2_volt[60599])/(days[60604]-days[60599])
for v in v2_volt[60599:60605]:
    v2_volt[i] = slope*(days[i]-days[start]) + v2_volt[60604]
    i += 1

# # 3
i = 64557
start = 64557
slope = (v2_volt[64572]-v2_volt[64557])/(days[64572]-days[64557])
for v in v2_volt[64557:64573]:
    v2_volt[i] = slope*(days[i]-days[start]) + v2_volt[64572]
    i += 1

# # 4
i = 70057
start = 70057
slope = (v2_volt[70078]-v2_volt[70057])/(days[70078]-days[70057])
for v in v2_volt[70079:64573]:
    v2_volt[i] = slope*(days[i]-days[start]) + v2_volt[70078]
    i += 1

v2_power = []
for v in v2_volt:
    v2_power.append(v*(v/2000))

# x2 = columns['unix_time']
# d0 = datetime.fromtimestamp(int(x2[0]))
# days = []

# unix_time = []
# for t in x2:
#     unix_time.append(int(t))

# for d in x2:
#     day = datetime.fromtimestamp(int(d))
#     day_from_start = day-d0
#     decimal_day = day_from_start.total_seconds()/(24 * 3600)
#     days.append(decimal_day)

# i = 0
# slope = (v2_power[9757]/v2_power[9731])/()
# for p in v2_power[9731:9758]:


# for i,t in enumerate(unix_time):
#     while t >= 1655413184 or t <= 1655414787:
#         print(i)


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
p2_power = []
p3_power = []
for i in range(0, len(v3)):
    v1_power.append(float(v1[i]))
    v3_power.append(float(v3[i]))

    p1_power.append(float(p1[i]))
    p2_power.append(float(p2[i]))
    p3_power.append(float(p3[i]))


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

# plt.plot(days[:105102], v2_power[:105102], 'b-', label='data')
# plt.plot(days[:105102], y[:105102], 'g-', linewidth=2, label='filtered data')



# # plot line
fig, ax = plt.subplots()
ax.plot(days[:105102], v_ave[:105102], label = "Vertical Average", alpha = 1, color= (0,0.1,1))
ax.plot(days[:105102], y1[:105102], label = "Vertical 1", alpha = 0.2, color= (0,0.2,0.5))
# plt.plot(days[:105102], v2_power[:105102], label = "Vertical 2", alpha = 0.2, color= (0,0.4,0.5))
ax.plot(days[:105102], y2[:105102], label='Vertical 2', alpha = 0.2, color= (0,0.4,0.5))
ax.plot(days[:105102], y3[:105102], label = "Vertical 3", alpha = 0.2, color= (0,0.6,0.5))

ax.plot(days[:105102], p_ave[:105102], label = "Horizontal Average", alpha = 1, color= (1,0.1,0))
ax.plot(days[:105102], y4[:105102], label = "Horizontal 1", alpha = 0.2, color= (0.5,0.2,0))
ax.plot(days[:105102], y5[:105102], label = "Horizontal 2", alpha = 0.2, color= (0.5,0.4,0))
ax.plot(days[:105102], y6[:105102], label = "Horizontal 3", alpha = 0.2, color= (0.5,0.6,0))
ax.legend("upper left")

#example of vertical line plotting
# ax.axvspan(8, 14, alpha=0.5, color='red')
# started drying cells'
plt.axvline(x = 50.153796, alpha = 0.2, color = 'yellow')
# label = 'reflooded cells'
plt.axvspan(50, 58.886458, color = 'yellow', alpha = 0.2)
# label = 'started drying again'
plt.axvspan(74.551516, 85, color = 'yellow', alpha = 0.2)

## PROBLEMS!
# 1. We don't need the lines to show up in legend
# 2. We want to label or even maybe shade in regions on the graphs (e.g. between the vertical lines)

#import custom font
from matplotlib import font_manager
font_path = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
my_font = font_manager.FontProperties(fname=font_path, size=12)  # get the font based on the font_path, set font size

#set font type of x and y axis
plt.ylabel('Power (µW)', fontproperties=my_font)
plt.xlabel('Timeline (Days)', fontproperties=my_font)

#set font type of tickmarks
for label in ax.get_xticklabels():
    label.set_fontproperties(my_font)
for label in ax.get_yticklabels():
    label.set_fontproperties(my_font)

#set font type of legend
plt.legend(prop=my_font)
plt.show()
