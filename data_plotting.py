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
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k


x = columns['Date']
d0 = datetime.strptime(x[0], "%m/%d/%y")
days = []
day_counter = 0
start = d0.day
curr_mon = d0.month
for d in x:
    day = datetime.strptime(d, "%m/%d/%y")

    day_from_start = day-d0
    days.append(day_from_start.days)



p1 = columns['Vertical 1']
p2 = columns['Vertical 2']
p3 = columns['Vertical 3']
p4 = columns['Planar 1']
p5 = columns['Planar 2']
p6 = columns['Planar 3']

p1_min = int(min(p1))
p1_max = int(float(max(p1)))

plt.autoscale(enable=True, axis='y')
# # plot line
plt.plot(days, p1, label = "Vertical 1", alpha=0.4)
plt.plot(days, p2, label = "Vertical 2", alpha=0.4)
plt.plot(days, p3, label = "Vertical 3")


plt.ylabel('Power')
plt.xlabel('Day of Experiment')

plt.legend()
plt.show()
