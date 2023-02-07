def internal_R_v3(): #return internal resistance of v3 cells in ohms
    return (1000 + 1000 + 1000)/3

def internal_R_v0(): #return internal resistance of v0 cells in ohms
    return (1000 + 1000 + 1000)/3

def SMFC_current(v, R):
    return v/R

def cap_leakage(insul_R=1000, rated_V=4):
    return rated_V/insul_R

def update_capVoltage(v0, V_applied, R, C, dt):
    #equation source: https://electronics.stackexchange.com/questions/264180/deriving-the-formula-from-scratch-for-charging-a-capacitor
    import math
    #assume constant current in this timestep
    if V_applied > v0: #only charge if applied voltage is greater than cap voltage
        V_new = V_applied * (1-math.exp(-dt/(R*C)))
    else:
        V_new = v0 #assume we won't discharge if voltage is lower
    return V_new

def update_capEnergy(v0, V_applied, R, C, dt):
    v_cap = update_capVoltage(v0, V_applied, R, C, dt)
    e_cap = 0.5*C*v_cap**2
    e_leak = v_cap*cap_leakage()*dt
    return e_cap-e_leak

def MSP430_energy():
    pass

def Ambiq_energy():
    pass

def MARS_energy():
    pass