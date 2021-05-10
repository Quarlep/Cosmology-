# Cosmology Calculator

import matplotlib.pyplot as plt
import PySimpleGUI as sg
from numpy import arange, sin, sinh, sqrt

# constant parameters
N = 10**6  # step-size
c = 299792.458  # speed of light in km/s

# input parameters
sg.change_look_and_feel('SandyBeach')

layout = [
    [sg.Text('Please Enter the Cosmological Parameters')],
    [sg.Text('H\N{SUBSCRIPT ZERO}', size=(5, 1)), sg.InputText()],
    [sg.Text('Ω_b', size=(5, 1)), sg.InputText()],
    [sg.Text('Ω_dm', size=(5, 1)), sg.InputText()],
    [sg.Text('Ω_Λ', size=(5, 1)), sg.InputText()],
    [sg.Text('Ω_r', size=(5, 1)), sg.InputText()],
    [sg.Text('z', size=(5, 1)), sg.InputText()],
    [sg.Text('w_Λ', size=(5, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('CoSmoS', layout)
event, values = window.read()
window.close()

H_0, Omega_b, Omega_dm, Omega_l, Omega_r, z, w_Λ = float(values[0]), float(values[1]), float(
    values[2]), float(values[3]), float(values[4]), float(values[5]), float(values[6])


# derived parameteres
hubble_time = (((1 / H_0) * (3.086e+19)) / (3.154e+7)) / 10**9  # in Gyr
a_emit = 1 / (1 + z)

# curvature density parameter
Omega_k = 1 - (Omega_b + Omega_dm + Omega_l + Omega_r)
q_0 = Omega_r + Omega_b / 2 + Omega_dm / 2 - Omega_l
hubble_dis = c / H_0  # in Mpc


####  Calculating the age of the Universe ####

def H(a):
    """
    The function of hubble parameter in terms of scale factor a(t)
    """
    return hubble_time / sqrt((Omega_b * (a)**(-1)) + (Omega_r * a**(-2)) + (Omega_dm * a**(-1)) + Omega_l*a**(-1-3*w_Λ) + (Omega_k))


def Time(a, b):
    """
    a is the time at the emission (t_e), b is the time at the observation (t_0). 
    I used the Simpsons rule
    """
    h = (b - a) / N
    S1 = 4 * sum([H(a + (2 * i - 1)*h) for i in range(1, N//2 + 1)])
    S2 = 2 * sum([H(a + (2 * i * h)) for i in range(1, N//2)])
    return 1/3 * h * (H(a) + H(b) + S1 + S2)


age_of_universe = Time(10**(-16), 1)
age_of_universe_at_z = age_of_universe - Time(a_emit, 1)
lookback_time = age_of_universe - age_of_universe_at_z

#### Calculating Distances ####

def H_z(z):
    """
    the function of hubble parameter in terms of redshift (z)
    """
    return hubble_dis / (sqrt((Omega_b * (1+z)**(3)) + (Omega_r * (1+z)**(4)) + (Omega_dm * (1+z)**(3)) + (Omega_l * ((1+z)**(3+3*w_Λ))) + Omega_k * (1+z)**2))


def distance(a, b):
    """
    measuring distance for a given z value
    """
    h = (b - a) / N
    S1 = 4 * sum([H_z(a + (2 * i - 1)*h) for i in range(1, N//2 + 1)])
    S2 = 2 * sum([H_z(a + (2 * i * h)) for i in range(1, N//2)])
    return 1/3 * h * (H_z(a) + H_z(b) + S1 + S2)


def S_k(r):
    if Omega_k < 0:
        return (hubble_dis / sqrt(abs(Omega_k))) * sin((sqrt(abs(Omega_k)) * r) / hubble_dis)
    if Omega_k == 0:
        return r
    if Omega_k > 0:
        return (hubble_dis / sqrt(Omega_k)) * sinh((sqrt(Omega_k) * r) / hubble_dis)


comoving_distance = distance(0, z)
luminosity_distance = (1 + z) * S_k(comoving_distance)
angular_distance = S_k(comoving_distance) / (1 + z)


#### Plotting a(t) vs t ####

da = 10**(-5)  # differential scale factor element

apoints = arange(10**(-6), 10, da)
tpoints = []
t = 0

# I am using dt = H(a)da

for a in apoints:
    t += H(a) * da
    tpoints.append(t)

plt.plot(apoints, tpoints, 'b-')
plt.ylabel('$a(t)$')
plt.xlabel('$t$ (Gyr)')
plt.axhline(y=1, color='r', linestyle='--', label='Today')
plt.legend()
plt.title('Scale Factor vs Time')
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.show()

#### plotting the distances ####

dz = 10**(-5)  # differential redshift element

zpoints = arange(0, 15, dz)
distance_points = []
angular_dis_points = []
lumin_dist_points = []
dis_point = 0


for z in zpoints:
    dis_point += H_z(z) * dz
    distance_points.append(dis_point)
    angular_dis_points.append(S_k(dis_point) / (1 + z))
    lumin_dist_points.append(S_k(dis_point) * (1 + z))


plt.plot(zpoints, distance_points, 'r', label='Comoving Distance')
plt.ylabel('Comoving Distance (Mpc)')
plt.xlabel('z')
plt.title('Comoving Distance vs Redshift')
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.show()

plt.plot(zpoints, angular_dis_points, 'b--', label='Angular diameter distance')
plt.ylabel('Angular Diameter Distance (Mpc)')
plt.xlabel('z')
plt.title('Angular Diameter Distance vs Redshift')
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.show()

plt.plot(zpoints, lumin_dist_points, 'g-.', label='Luminosity Distance')
plt.ylabel('Luminosity Distance (Mpc)')
plt.xlabel('z')
plt.title('Luminosity Distance vs Redshift')
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.show()

sg.popup('Results:\nAge of The Universe Today : {0:0.4f} Gyr\nAge of The Universe at z: {1:0.4f} Gyr\nLookback Time: {2:0.4f} Gyr\nComoving Distance at z: {3:0.4f} Mpc\nAngular Diameter Distance at  z: {4:0.4f} Mpc\nLuminosity Distance at z: {5:0.4f} Mpc'.format(
    age_of_universe, age_of_universe_at_z, lookback_time, comoving_distance, angular_distance, luminosity_distance), title="CoSmoS")
