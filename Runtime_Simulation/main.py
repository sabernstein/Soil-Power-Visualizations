import models
import bar_graphs
import SMFC
import math

#STEP 1: Import voltage values from v3_Data.csv and get filtered average of v3 and v0 cells
days, v0_avg_v, v3_avg_v  = SMFC.getMFC_data('Final_Data/v3_Data.csv')
for ii in range(len(days)): #turn everything into unit of volts
    v0_avg_v[ii] = v0_avg_v[ii]/1000
    v3_avg_v[ii] = v3_avg_v[ii]/1000

#Replace variable voltage with constant voltage for debugging
'''v0_avg_v = []
v3_avg_v = []
for item in days:
    v0_avg_v.append(0.3)
    v3_avg_v.append(0.3)'''

#Call simulate function
Ambiq0, MSP430_0, MARS0 = models.simulate(days, v0_avg_v, 1e-6)
Ambiq3, MSP430_3, MARS3 = models.simulate(days, v3_avg_v, 1e-6)

#generate bar graphs
bar_graphs.bar_subplots(Ambiq0, MSP430_0, MARS0, Ambiq3, MSP430_3, MARS3)