import models
import visualizations
import SMFC

#STEP 1: Import voltage values from v3_Data.csv and get filtered average of v3 and v0 cells
days, v0_avg_v, v3_avg_v  = SMFC.getMFC_data('Final_Data/v3_Data.csv')
for ii in range(len(days)): #turn everything into unit of volts
    v0_avg_v[ii] = v0_avg_v[ii]/1000
    v3_avg_v[ii] = v3_avg_v[ii]/1000

MARS_on_0 = []
for v in v0_avg_v:
    if v > 0.2:
        MARS_on_0.append(1)
    else:
        MARS_on_0.append(0)

MARS_on_3 = []
for v in v3_avg_v:
    if v > 0.2:
        MARS_on_3.append(1)
    else:
        MARS_on_3.append(0)
#visualizations.bar_subplots_mars(days, MARS_on_0, MARS_on_3)

#Replace variable voltage with constant voltage for debugging
# v0_avg_v = []
# v3_avg_v = []
# for item in days:
#     v0_avg_v.append(0.18)
#     v3_avg_v.append(0.002)

#Call simulate function
C0 = [0.007000000000000006, 0.007000000000000006, 0.007000000000000006]
C3 = [0.007000000000000006, 0.007000000000000006, 0.007000000000000006]
Ambiq0, MSP430_0, ignore = models.simulate(days, v0_avg_v, C0)
Ambiq3, MSP430_3, ignore = models.simulate(days, v3_avg_v, C3)

print(sum(Ambiq0))
print(sum(MSP430_0))
#print(sum(MARS0))
print(sum(MSP430_3))
print(sum(MSP430_3))
#print(sum(MARS3))

#generate bar graphs
#visualizations.bar_subplots2(Ambiq0, Ambiq3, MSP430_0, MSP430_3) # generate graph 1
visualizations.bar_subplots(Ambiq3, MSP430_3) # generate graph 2

#Find total sensor count
# cap_list = []
# for ii in range(1000):
#     cap_list.append(0.1-ii*1e-4)
# print(cap_list)
# for ii in range(10):
#     cap_list.append(0.01-ii*0.001)
# print(cap_list)

# ambiq0_exec_count = []
# msp0_exec_count = []
# mars0_exec_count = []
# ambiq3_exec_count = []
# msp3_exec_count = []
# mars3_exec_count = []

# for c in cap_list:
#     Ambiq0, MSP430_0, MARS0 = models.simulate(days, v0_avg_v, [c,c,c,c,c,c])
#     Ambiq3, MSP430_3, MARS3 = models.simulate(days, v3_avg_v, [c,c,c,c,c,c])
#     ambiq0_exec_count.append(sum(Ambiq0))
#     msp0_exec_count.append(sum(MSP430_0))
#     mars0_exec_count.append(sum(MARS0))
#     ambiq3_exec_count.append(sum(Ambiq3))
#     msp3_exec_count.append(sum(MSP430_3))
#     mars3_exec_count.append(sum(MARS3))

# print(ambiq0_exec_count)
# print(msp0_exec_count)
# print(mars0_exec_count)
# print(ambiq3_exec_count)
# print(msp3_exec_count)
# print(mars3_exec_count)
# print("these values: ")
# print(models.getMax(cap_list, ambiq0_exec_count))
# print(models.getMax(cap_list, msp0_exec_count))
# print(models.getMax(cap_list, mars0_exec_count))
# print(models.getMax(cap_list, ambiq3_exec_count))
# print(models.getMax(cap_list, msp3_exec_count))
# print(models.getMax(cap_list, mars3_exec_count))

# visualizations.count_vs_cap(cap_list, ambiq0_exec_count, msp0_exec_count, mars0_exec_count, ambiq3_exec_count, msp3_exec_count, mars3_exec_count)