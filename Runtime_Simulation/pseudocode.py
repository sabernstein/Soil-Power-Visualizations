#Initialize variables
t_list, v_list = getSMFC_voltage()
e0, v0, on_Count = 0
on_Count_list = []
E_thresh = V_DD * I_active * t_sense + V_startup * I_active * t_startup
for i in range(1,len(t_list)): #For each voltage data point
    dt = 24*60*60*(t_list[i]-t_list[i-1]) #Time since last measurement (s)
    if e0 > 0: #Calculate initial voltage using energy
        v0=math.sqrt(2*e0/C)
    else:
        v0=0
    if v_list[i] > v0: #Update amount of energy in capacitor given SMFC output
        v_new=v0+v_list[i]*(1-math.exp(-dt/(r*C))) #r is internal resistance
    #Capacitor voltage can't be bigger than applied
    if v_new > v[i]:
        v_new = v[i]
    #Calculate new energy from voltage
    E = 0.5*C*(v_new**2) - ((v_new**2)/R_insul)*dt
    if E < 0:
        E = 0 #Set lower bound of E assuming full discharge
    #Check if we have enough power to turn things on
    if E > E_thresh:
        #Add theoretical number of readings to on_Count
        on_Count = on_Count + round(E/E_thresh)
        E = 0 #Completely discharge
    if day_end(t_list[i], t_list[i-1]): #Check to see if day ended
        on_Count_list.append(on_Count)
        on_Count = 0 #Reset reading count
    e0 = E #Set start condition for next loop
return on_Count_list #Output final desired count list