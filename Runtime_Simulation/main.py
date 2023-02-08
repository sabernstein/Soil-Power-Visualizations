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

def simulate(t_list, v_list, C_h):
    # t_list: list of decimal time stamps in unit of days (e.g. 71.85893518518519 day), same length as v_list
    # v_list: list of voltage values from SFMC
    # C_h: capacitance of the capacitor being filled up by harvester
    on_Ambiq_list = []
    on_MARS_list = []
    on_MSP430_list = []

    #assume capacitor is completely discharged at start
    e_ambiq_init = 0 
    e_msp430_init = 0
    e_mars_init = 0

    #Initialize daily sensor reading count
    on_Ambiq = 0
    on_MSP430 = 0
    on_MARS = 0

    cap_energy_mars = []
    cap_energy_msp430 = []
    cap_energy_ambiq = []

    cap_v_mars = []
    cap_v_msp430 = []
    cap_v_ambiq = []

    #for each voltage data point
    for jj in range(1,len(t_list)): #last data point was at 71.85893518518519 day

        t = 24*60*60*(t_list[jj] - t_list[jj-1]) #dt is time since last measurement in seconds

        #update amount of energy in capacitor given v0 output
        E_Ambiq, v_ambiq = models.update_capEnergy(e_ambiq_init, V_applied=v_list[jj], R=models.internal_R_v0(), C=C_h, dt=t)
        E_MSP430, v_msp430 = models.update_capEnergy(e_msp430_init, V_applied=v_list[jj], R=models.internal_R_v0(), C=C_h, dt=t)
        E_MARS, v_mars = models.update_capEnergy(e_mars_init, V_applied=v_list[jj], R=models.internal_R_v0(), C=C_h, dt=t)

        
        #Check if we have enough power to turn things on
        if E_Ambiq > models.Ambiq_energy():
            on_Ambiq = on_Ambiq + round(E_Ambiq/models.Ambiq_energy())
            E_Ambiq = 0 #completely discharge, prob bad assumption will change based on matrix board stat
            v_ambiq = 0
            #
            
        if E_MSP430 > models.MSP430_energy():
            on_MSP430 = on_MSP430 + round(E_MSP430/models.MSP430_energy())
            E_MSP430 = 0 #completely discharge, prob bad assumption will change based on matrix board stat
            v_msp430 = 0
            #
            
        if E_MARS > models.MARS_energy():
            #print(E0_MARS, models.MARS_energy(), E0_MARS/models.MARS_energy())
            on_MARS = on_MARS + round(E_MARS/models.MARS_energy())
            
            E_MARS = 0 #completely discharge, prob bad assumption will change based on matrix board stat
            v_mars = 0
            
            #print("Discharging!! Now energy left: " + str(E0_MARS))

        cap_energy_mars.append(E_MARS)
        cap_energy_msp430.append(E_MSP430)
        cap_energy_ambiq.append(E_Ambiq)
        cap_v_mars.append(v_mars)
        cap_v_msp430.append(v_msp430)
        cap_v_ambiq.append(v_ambiq)

        #update start condition for next loop
        e_ambiq_init = E_Ambiq
        e_msp430_init = E_MSP430
        e_mars_init = E_MARS
        
        if math.trunc(days[jj-1]) != math.trunc(days[jj]): #if a day ended
            #record the number of sensor reading that day to their respective lists
            on_Ambiq_list.append(on_Ambiq)
            on_MSP430_list.append(on_MSP430)
            on_MARS_list.append(on_MARS)

            #Reset daily sensor reading count
            on_Ambiq = 0
            on_MSP430 = 0
            on_MARS = 0

    #Debugging print and plots
    print("# of readings by Ambiq: ", on_Ambiq_list)
    print("# of readings by MSP430: ", on_MSP430_list)
    print("# of readings by MARS: ", on_MARS_list)

    from matplotlib import pyplot as plt
    fig, axs = plt.subplots(3, 1, figsize=(12, 4), sharex=True)
    axs[0].plot(t_list[1:], cap_energy_ambiq, label="E in Ambiq Capacitor")
    axs[0].plot(t_list[1:], cap_energy_msp430, label="E in MSP430 Capacitor")
    axs[0].plot(t_list[1:], cap_energy_mars, label="E in MARS Capacitor")
    axs.flat[0].set(ylabel="Energy (J)")

    axs[1].plot(t_list[1:], cap_v_ambiq, label="V of Ambiq Capacitor")
    axs[1].plot(t_list[1:], cap_v_msp430, label="V of MSP430 Capacitor")
    axs[1].plot(t_list[1:], cap_v_mars, label="V of MARS Capacitor")
    axs.flat[1].set(ylabel="Voltage (V)")

    axs[2].plot(days[1:], v_list[1:], label="SMFC Voltage")
    axs.flat[2].set(ylabel="SMFC Voltage (V)")

    # specifying horizontal line type
    #plt.axhline(y = models.Ambiq_energy(), color = 'r', linestyle = '-')
    #plt.axhline(y = models.MARS_energy(), color = 'r', linestyle = '-.')

    plt.xlabel("Timeline (Days)")
    axs[0].legend()
    axs[1].legend()

    return on_Ambiq_list, on_MSP430_list, on_MARS_list
    

#Call simulate function
Ambiq0, MSP430_0, MARS0 = simulate(days, v0_avg_v, 1e-6)
Ambiq3, MSP430_3, MARS3 = simulate(days, v3_avg_v, 1e-6)

#generate bar graphs
bar_graphs.bar_subplots(Ambiq0, MSP430_0, MARS0, Ambiq3, MSP430_3, MARS3)