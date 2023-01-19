import csv
from collections import defaultdict
# importing package
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import rc

#Steps to install custom fonts:
'''
1. Download font from sources and unzip, should get .ttf files in File Explorer
2. Right click all .ttf files you want to install (one per font) and click "Install"
3. Go to terminal and check if matplotlib have access to the new fonts now:

# from matplotlib import font_manager
# font_manager.findSystemFonts(fontpaths=None, fontext="ttf")

4. Find the font name in the list (for Libertine (https://www.dafont.com/linux-libertine.font) it's LinLibertine_R), and check if the specific font can be accessed:

# font_manager.findfont("LinLibertine_R", rebuild_if_missing=True)

5. Now that you know it's downloaded, do this to use it:

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

'''

# import required modules
import numpy as np
import matplotlib.pyplot as plt


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
fig, ax = plt.subplots()
ax.plot(days[:105102], vertical_ave[:105102], label = "Vertical Average", alpha = 1, color= (0,0.1,1))
ax.plot(days[:105102], v1_power[:105102], label = "Vertical 1", alpha = 0.2, color= (0,0.2,0.5))
ax.plot(days[:105102], v2_power[:105102], label = "Vertical 2", alpha = 0.2, color= (0,0.4,0.5))
ax.plot(days[:105102], v3_power[:105102], label = "Vertical 3", alpha = 0.2, color= (0,0.6,0.5))

ax.plot(days[:105102], planar_ave[:105102], label = "Horizontal Average", alpha = 1, color= (1,0.1,0))
ax.plot(days[:105102], p1_power[:105102], label = "Horizontal 1", alpha = 0.2, color= (0.5,0.2,0))
ax.plot(days[:105102], p2_power[:105102], label = "Horizontal 2", alpha = 0.2, color= (0.5,0.4,0))
ax.plot(days[:105102], p3_power[:105102], label = "Horizontal 3", alpha = 0.2, color= (0.5,0.6,0))
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
