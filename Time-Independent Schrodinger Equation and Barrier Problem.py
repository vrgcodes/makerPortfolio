import math
import numpy as np
from matplotlib import pyplot as plt

electronMass = 0.0017
h_bar = 4.125*(10**-15)
v0 = 10**-6
eta_array_above = np.arange(1.00000000000001,2,0.0000001)
eta_array_below = np.arange(0.0000001,1,0.0000001)


def transmissibility_above(width):
    transmission_above = []
    reflection_above = []
    for eta in eta_array_above:
        k_above = ((2*electronMass*v0*(eta-1))**0.5)/(h_bar)
        transmissibility_factor_above = (1+(((math.sin(k_above*width))**2)/(4*eta*(eta-1))))**-1
        reflectivity_factor_above = 1-transmissibility_factor_above
        transmission_above.append(transmissibility_factor_above)
        reflection_above.append(reflectivity_factor_above)
    return transmission_above, reflection_above

def transmissibility_below(width):
    transmission_below = []
    reflection_below = []
    for eta2 in eta_array_below:
        k_below = ((2*electronMass*v0*(1-eta2))**0.5)/(h_bar)
        try:
            transmissibility_factor_below = (1+(((math.sinh(k_below*width))**2)/(4*eta2*(1-eta2))))**-1
        except OverflowError:
            transmissibility_factor_below = math.inf
        reflectivity_factor_below = 1-transmissibility_factor_below
        transmission_below.append(transmissibility_factor_below)
        reflection_below.append(reflectivity_factor_below)
    return transmission_below, reflection_below

a= float(input("Enter barrier width (in nm): "))

t_above, r_above = transmissibility_above(a*(10**-9))
t_below, r_below = transmissibility_below(a*(10**-9))


plt.plot(eta_array_above, t_above, label="T")
plt.plot(eta_array_above, r_above, label = "R")
plt.xlabel("η")
plt.ylabel("T, R")
plt.title("E<V\u2080")
plt.show()

plt.plot(eta_array_below, t_below, label="T")
plt.plot(eta_array_below, r_below, label = "R")
plt.xlabel("η")
plt.ylabel("T, R")
plt.title("E>V\u2080")
plt.show()