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

def cap_leakage(insul_R=1000, rated_V=4):
    #https://media.digikey.com/pdf/Data%20Sheets/Samsung%20PDFs/CL05X106MR5NUNC_Spec.pdf
    return rated_V/insul_R

def update_capVoltage(v0, V_applied, R, C, dt):
    #equation source: https://electronics.stackexchange.com/questions/264180/deriving-the-formula-from-scratch-for-charging-a-capacitor
    # v0: initial voltage
    # V_applied: voltage from SMFC
    # R: internal resistance of SMFC
    # C: capacitance of capacitor
    # dt: time step since last data point
    import math
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
    import math
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
    e_leak = 0#v_cap*cap_leakage()*dt
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
    return 1.9 * 15.8e-6*96 * 20e-6 #test value

def MSP430_energy():
    return 1.8 * 90e-6 * 20e-6 #test value for time

def MARS_energy():
    return 0.2 * 2.15e-6 * 20e-6 #test value for time