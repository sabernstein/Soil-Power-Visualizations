import csv
from collections import defaultdict
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from datetime import datetime

columns = defaultdict(list) # each value in each column is appended to a list

with open('Final_Data/Prelim_Studies_VWC_Data.csv') as f:
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

vwc = columns['raw_VWC']
vwc_data = []
for i in range(0, len(vwc)):
    vwc_data.append(float(vwc[i]))
# print(vwc_data)

fig, ax = plt.subplots()
ax.plot(days, vwc_data, label = "VMC", alpha = 1, color= (0,0.6,0.5))
ax.legend()
# ax.legend("upper left")

#import custom font
from matplotlib import font_manager
font_path = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
my_font = font_manager.FontProperties(fname=font_path, size=12)  # get the font based on the font_path, set font size

#set font type of x and y axis
plt.ylabel('Volumetric Water Content', fontproperties=my_font)
plt.xlabel('Timeline (Days)', fontproperties=my_font)

#set font type of tickmarks
for label in ax.get_xticklabels():
    label.set_fontproperties(my_font)
for label in ax.get_yticklabels():
    label.set_fontproperties(my_font)

#set font type of legend
# plt.legend(prop=my_font)
plt.show()