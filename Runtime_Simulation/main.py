import models
import bar_graphs
import SMFC
import math

#STEP 1: Import voltage values from v3_Data.csv and get filtered average of v3 and v0 cells
days, v0_avg_v, v3_avg_v  = SMFC.getMFC_data('Final_Data/v3_Data.csv')

#STEP 3:
# For each day:
#   on_MSP430, on_Ambiq, on_MARS = 0
#   For each time step (like every 60 s given our logging freq):
#       - Update the energy in our capacitor (put fcn in models.py) given (1) input voltage, (2) time step, (3) capacitance (prob 10 uF), this will be an integral
#       - Check if energy is enough to turn on (1) 1 uJ load, (2) 10 uJ load, and (3) 20 uJ load (will tweak later to reflect real energy cost of each system)
#       - If so, add to on_MSP430, on_Ambiq, and on_MARS and reset capacitor energy to 0 J (might tweak this value)
#   Append on_MSP430, on_Ambiq, on_MARS to on_MSP430_list, on_Ambiq_list, on_MARS_list. This will be a list of how many sensor readings we are able to take with each of these systems every day given the energy we got
#STEP 4: Visualize the daily # of readings with 3 bar graphs, y axis is # of readings and x axis is days.
#   - Given 3 lists of integer values, plot them on bar graphs

on_Ambiq_list0 = []
on_MSP430_list0 = []
on_MARS_list0 = []

on_Ambiq_list3 = []
on_MSP430_list3 = []
on_MARS_list3 = []

#assume capacitor is completely discharged at start
e0_ambiq_init = 0 
e0_msp430_init = 0
e0_mars_init = 0

e3_ambiq_init = 0 
e3_msp430_init = 0
e3_mars_init = 0

#Initialize daily sensor reading count
on_Ambiq_0 = 0
on_MSP430_0 = 0
on_MARS_0 = 0
on_Ambiq_3 = 0
on_MSP430_3 = 0
on_MARS_3 = 0

cap_energy = []

#for each voltage data point
for jj in range(1,len(days)): #last data point was at 71.85893518518519 day

    t = 24*60*60*(days[jj] - days[jj-1]) #dt is time since last measurement in seconds
    #update amount of energy in capacitor given v0 and v3 cell output
    
    E0_Ambiq = models.update_capEnergy(e0_ambiq_init, V_applied=v0_avg_v[jj], R=models.internal_R_v0(), C=10e-6, dt=t)
    E0_MSP430 = models.update_capEnergy(e0_msp430_init, V_applied=v0_avg_v[jj], R=models.internal_R_v0(), C=10e-6, dt=t)
    E0_MARS = models.update_capEnergy(e0_mars_init, V_applied=v0_avg_v[jj], R=models.internal_R_v0(), C=10e-6, dt=t)
    
    #print(E0_MARS, models.MARS_energy(), E0_MARS > models.MARS_energy())
    E3_Ambiq = models.update_capEnergy(e3_ambiq_init, V_applied=v3_avg_v[jj], R=models.internal_R_v3(), C=10e-6, dt=t)
    E3_MSP430 = models.update_capEnergy(e3_msp430_init, V_applied=v3_avg_v[jj], R=models.internal_R_v3(), C=10e-6, dt=t)
    E3_MARS = models.update_capEnergy(e3_mars_init, V_applied=v3_avg_v[jj], R=models.internal_R_v3(), C=10e-6, dt=t)

    #Check if we have enough power to turn things on
    if E0_Ambiq > models.Ambiq_energy():
        E0_Ambiq = 0 #completely discharge, prob bad assumption will change based on matrix board stat
        on_Ambiq_0 = on_Ambiq_0 + 1
    if E0_MSP430 > models.MSP430_energy():
        E0_MSP430 = 0 #completely discharge, prob bad assumption will change based on matrix board stat
        on_MSP430_0 = on_MSP430_0 + 1
    if E0_MARS > models.MARS_energy():
        E0_MARS = 0 #completely discharge, prob bad assumption will change based on matrix board stat
        on_MARS_0 = on_MARS_0 + 1
        #print("Discharging!! Now energy left: " + str(E0_MARS))

    if E3_Ambiq > models.Ambiq_energy():
        E3_Ambiq = 0 #completely discharge, prob bad assumption will change based on matrix board stat
        on_Ambiq_3 = on_Ambiq_3 + 1
    if E3_MSP430 > models.MSP430_energy():
        E3_MSP430 = 0 #completely discharge, prob bad assumption will change based on matrix board stat
        on_MSP430_3 = on_MSP430_3 + 1
    if E3_MARS > models.MARS_energy():
        E3_MARS = 0 #completely discharge, prob bad assumption will change based on matrix board stat
        on_MARS_3 = on_MARS_3 + 1

    #update start condition for next loop
    e0_ambiq_init = E0_Ambiq
    e0_msp430_init = E0_MSP430
    e0_mars_init = E0_MARS

    e3_ambiq_init = E3_Ambiq
    e3_msp430_init = E3_MSP430
    e3_mars_init = E3_MARS

    
    
    if math.trunc(days[jj-1]) != math.trunc(days[jj]): #if a day ended
        #record the number of sensor reading that day to their respective lists
        on_Ambiq_list0.append(on_Ambiq_0)
        on_MSP430_list0.append(on_MSP430_0)
        on_MARS_list0.append(on_MARS_0)
        on_Ambiq_list3.append(on_Ambiq_3)
        on_MSP430_list3.append(on_MSP430_3)
        on_MARS_list3.append(on_MARS_3)

        #Reset daily sensor reading count
        on_Ambiq_0 = 0
        on_MSP430_0 = 0
        on_MARS_0 = 0
        on_Ambiq_3 = 0
        on_MSP430_3 = 0
        on_MARS_3 = 0
        #print(jj)

print(on_Ambiq_list0)
print(on_MSP430_list0)
print(on_MARS_list0)

#from matplotlib import pyplot as plt
#plt.plot(days[1:], cap_energy)
#plt.show()

bar_graphs.bar_subplots(on_Ambiq_list0, on_MSP430_list0, on_MARS_list0)
