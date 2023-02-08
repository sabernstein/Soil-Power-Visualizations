import math

def internal_R_v3(R=2000): #return internal resistance of v3 cells in ohms
    #https://www.jstage.jst.go.jp/article/jwet/20/1/20_21-087/_pdf
    v0_oc = 48.5e-3 #48.5 mV
    v0_cc = 4.8e-3
    v0_r = R*((v0_oc/v0_cc)-1)

    v1_oc = 43.8e-3
    v1_cc = 20.9e-3
    v1_r = R*((v1_oc/v1_cc)-1)

    v2_oc = 45.2e-3
    v2_cc = 23.5e-3
    v2_r = R*((v2_oc/v2_cc)-1)

    return (v0_r+v1_r+v2_r)/3

def internal_R_v0(R=2000): #return internal resistance of v0 cells in ohms
    v3_oc = 41.7e-3 #41.7mV
    v3_cc = 5.1e-3
    v3_r = R*((v3_oc/v3_cc)-1)

    v4_oc = 48.7e-3
    v4_cc = 16.8e-3
    v4_r = R*((v4_oc/v4_cc)-1)

    v5_oc = 39.1e-3
    v5_cc = 16.9e-3
    v5_r = R*((v5_oc/v5_cc)-1)

    return (v3_r+v4_r+v5_r)/3

def SMFC_current(v, R):
    return v/R

def cap_leakage(insul_R=1000e6, rated_V=4):
    #https://media.digikey.com/pdf/Data%20Sheets/Samsung%20PDFs/CL05X106MR5NUNC_Spec.pdf
    return rated_V/insul_R

def update_capVoltage(v0, V_applied, R, C, dt):
    #equation source: https://electronics.stackexchange.com/questions/264180/deriving-the-formula-from-scratch-for-charging-a-capacitor
    # v0: initial voltage
    # V_applied: voltage from SMFC
    # R: internal resistance of SMFC
    # C: capacitance of capacitor
    # dt: time step since last data point
    #assume constant current in this timestep
    if V_applied > v0: #only charge if applied voltage is greater than cap voltage
        V_new = v0 + V_applied * (1-math.exp(-dt/(R*C)))
        if V_new > V_applied: #cap voltage can't be bigger than applied
            V_new = V_applied
        #print("Charging V_new: " + str(V_new) + ", V_applied: " + str(V_applied))
    else:
        V_new = v0 #assume we won't discharge if voltage is lower
        #print("Not charging V_new: " + str(V_new) + ", V_applied: " + str(V_applied))
    return V_new #unit is volts

def update_capEnergy(e0, V_applied, R, C, dt):
    # e0: initial energy stored
    # V_applied: voltage from SMFC
    # R: internal resistance of SMFC
    # C: capacitance of capacitor
    # dt: time step since last data point
    if e0 > 0:
        v0 = math.sqrt(2*e0/C)
    else:
        v0 = 0
    v_cap = update_capVoltage(v0, V_applied, R, C, dt)
    e_cap = 0.5*C*v_cap**2
    e_leak = v_cap*cap_leakage(1000e6, v_cap)*dt
    e_final = e_cap-e_leak
    if e_final < 0: #Not charging if leakage is greater than energy
        e_final = 0
    #print("e_final: " + str(e_final))
    return e_final, v_cap #subtract leaked energy

def Ambiq_energy():
    #page 188 of Apollo4 SoC Datasheet
    #VDD = 1.9
    #15.8 uA/MHz
    #HFRC=96 MHz
    t = 0.8e-3 + 10e-6 + 10e-6
    return 1.9 * 15.8e-6*96 * t #test value

def MSP430_energy():
    t = 0.8e-3 + 10e-6 + 10e-6
    return 1.8 * 90e-6 * t #test value for time

def MARS_energy():
    return 0.2 * 2.15e-6 * 20e-3 #test value for time
    

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
        E_Ambiq, v_ambiq = update_capEnergy(e_ambiq_init, V_applied=v_list[jj], R=internal_R_v0(), C=C_h, dt=t)
        E_MSP430, v_msp430 = update_capEnergy(e_msp430_init, V_applied=v_list[jj], R=internal_R_v0(), C=C_h, dt=t)
        E_MARS, v_mars = update_capEnergy(e_mars_init, V_applied=v_list[jj], R=internal_R_v0(), C=C_h, dt=t)

        
        #Check if we have enough power to turn things on
        if E_Ambiq > Ambiq_energy():
            on_Ambiq = on_Ambiq + round(E_Ambiq/Ambiq_energy())
            E_Ambiq = 0 #completely discharge, prob bad assumption will change based on matrix board stat
            v_ambiq = 0
            #
            
        if E_MSP430 > MSP430_energy():
            on_MSP430 = on_MSP430 + round(E_MSP430/MSP430_energy())
            E_MSP430 = 0 #completely discharge, prob bad assumption will change based on matrix board stat
            v_msp430 = 0
            #
            
        if E_MARS > MARS_energy():
            #print(E0_MARS, models.MARS_energy(), E0_MARS/models.MARS_energy())
            on_MARS = on_MARS + round(E_MARS/MARS_energy())
            
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
        
        if math.trunc(t_list[jj-1]) != math.trunc(t_list[jj]): #if a day ended
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

    axs[2].plot(t_list[1:], v_list[1:], label="SMFC Voltage")
    axs.flat[2].set(ylabel="SMFC Voltage (V)")

    # specifying horizontal line type
    #plt.axhline(y = models.Ambiq_energy(), color = 'r', linestyle = '-')
    #plt.axhline(y = models.MARS_energy(), color = 'r', linestyle = '-.')

    plt.xlabel("Timeline (Days)")
    axs[0].legend()
    axs[1].legend()

    return on_Ambiq_list, on_MSP430_list, on_MARS_list
     