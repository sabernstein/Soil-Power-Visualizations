import models
import visualizations
import SMFC

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
Ambiq0, MSP430_0, MARS0 = models.simulate(days, v0_avg_v, 10e-6)
Ambiq3, MSP430_3, MARS3 = models.simulate(days, v3_avg_v, 10e-6)

#generate bar graphs
visualizations.bar_subplots(Ambiq0, MSP430_0, MARS0, Ambiq3, MSP430_3, MARS3)

#Find total sensor count
'''cap_list = []
for ii in range(500):
    cap_list.append(0.2-ii*0.0004)
print(cap_list)
ambiq0_exec_count = []
msp0_exec_count = []
mars0_exec_count = []
ambiq3_exec_count = []
msp3_exec_count = []
mars3_exec_count = []

for c in cap_list:
    Ambiq0, MSP430_0, MARS0 = models.simulate(days, v0_avg_v, c)
    Ambiq3, MSP430_3, MARS3 = models.simulate(days, v3_avg_v, c)
    ambiq0_exec_count.append(sum(Ambiq0))
    msp0_exec_count.append(sum(MSP430_0))
    mars0_exec_count.append(sum(MARS0))
    ambiq3_exec_count.append(sum(Ambiq3))
    msp3_exec_count.append(sum(MSP430_3))
    mars3_exec_count.append(sum(MARS3))

print(ambiq0_exec_count)
print(msp0_exec_count)
print(mars0_exec_count)
print(ambiq3_exec_count)
print(msp3_exec_count)
print(mars3_exec_count)

visualizations.count_vs_cap(cap_list, ambiq0_exec_count, msp0_exec_count, mars0_exec_count, ambiq3_exec_count, msp3_exec_count, mars3_exec_count)'''