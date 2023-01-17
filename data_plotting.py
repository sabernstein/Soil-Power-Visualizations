import csv
from collections import defaultdict
# importing package
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import date
import numpy as np

# import required modules
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter,filtfilt
import math

columns = defaultdict(list) # each value in each column is appended to a list

with open('v2_Data1.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            if v != '':
                columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

x2 = columns['unix_time']
d0 = datetime.fromtimestamp(int(x2[0]))
days = []

for d in x2:
    day = datetime.fromtimestamp(int(d))
    day_from_start = day-d0
    decimal_day = day_from_start.total_seconds()/(24 * 3600)
    days.append(decimal_day)


v1 = columns['Vertical 1']
v2 = columns['Vertical 2']
v3 = columns['Vertical 3']
p1 = columns['Planar 1']
p2 = columns['Planar 2']
p3 = columns['Planar 3']
v_ave = columns['V Average']
vertical_ave = []
p_ave = columns['P Average']
planar_ave = []
v1_power = []
v2_power = []
v3_power = []
p1_power = []
p2_power = []
p3_power = []
for i in range(0, len(v3)):
    v1_power.append(float(v1[i]))
    v2_power.append(float(v2[i]))
    v3_power.append(float(v3[i]))
    vertical_ave.append(float(v_ave[i]))
    p1_power.append(float(p1[i]))
    p2_power.append(float(p2[i]))
    p3_power.append(float(p3[i]))
    planar_ave.append(float(p_ave[i]))
    
for i in range(0, len(v2_power)):
    if v2_power[i] > 200 or v2_power[i] < 0:
        v2_power[i] = v2_power[i-1]

for i in range(0, len(vertical_ave)):
    if vertical_ave[i] > 200 or vertical_ave[i] < 0:
        vertical_ave[i] = vertical_ave[i-1]
# planar_ave = ['P Average']

# # plot line
# plt.plot(days, vertical_ave, label = "Vertical Average", alpha = 1)
# plt.plot(days, v1_power, label = "Vertical 1", alpha = 0.2)
plt.plot(days, v2_power, label = "Vertical 2", alpha = 0.2)
# plt.plot(days, v3_power, label = "Vertical 3", alpha = 0.2)

# plt.plot(days, planar_ave, label = "Planar Average", alpha = 1)
# plt.plot(days, p1_power, label = "Planar 1", alpha = 0.2)
# plt.plot(days, p2_power, label = "Planar 2", alpha = 0.2)
# plt.plot(days, p3_power, label = "Planar 3", alpha = 0.2)


plt.ylabel('Power (µW)')
plt.xlabel('Experiment Timeline (days)')

plt.legend()
plt.show()
