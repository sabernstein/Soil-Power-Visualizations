import numpy as np

# Capacitance of the capacitor (in Farads)
C = 1e-6

# Initial voltage (in Volts)
V = 0

# Time step (in seconds)
dt = 0.001

# Final time (in seconds)
t_final = 1

# Total number of time steps
num_steps = int(t_final / dt)

# Charging constant
R = 1e3

# Array to store the energy at each time step
energies = np.zeros(num_steps)

for i in range(num_steps):
    # Update voltage
    V = V + dt * (1 / R) * V
    # Compute energy
    energies[i] = 0.5 * C * V ** 2

print(energies)