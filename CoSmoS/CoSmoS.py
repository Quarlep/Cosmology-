#### GUI based Cosmology Calculator ####

import matplotlib.pyplot as plt
import PySimpleGUI as sg
from numpy import arange, sqrt, sinh, sin


# constant parameters
N = 10**5  # step-size
c = 299792.458  # speed of light in km/s

#### Calculating the age of the Universe ####

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


# input parameters
sg.change_look_and_feel('SandyBeach')

layout_input = [
    [sg.Text('Cosmological Parameters', size=(
        35, 1), justification='center', font=('Inconsolota', 15), relief=sg.RELIEF_RIDGE)],
    [sg.Image(r'GUI Images\H0.png'), sg.InputText(default_text='69.36')],
    [sg.Image(r'GUI Images\Omegab.png'), sg.InputText(default_text='0.05')],
    [sg.Image(r'GUI Images\Omegac.png'), sg.InputText(default_text='0.25')],
    [sg.Image(r'GUI Images\OmegaL.png'), sg.InputText(default_text='0.7')],
    [sg.Image(r'GUI Images\Omegar.png'),
     sg.InputText(default_text='0.00009')],
    [sg.Image(r'GUI Images\z.png'), sg.InputText(default_text='3')],
    [sg.Image(r'GUI Images\wL.png'), sg.InputText(default_text='-1')],
    [sg.Submit(), sg.Cancel()]
]

window_input = sg.Window('CoSmoS', layout_input)
event, values = window_input.read()
if event == sg.WIN_CLOSED or event == 'Exit':
    window_input.close()
if event == 'Submit':
    H_0, Omega_b, Omega_dm, Omega_l, Omega_r, z, w_Λ = [float(values[i]) for i in range(1, 15, 2)]
    # derived parameteres

    hubble_time = (((1 / H_0) * (3.086e+19)) / (3.154e+7)) / 10**9  # in Gyr
    a_emit = 1 / (1 + z)
    
    # curvature density parameter
    Omega_k = 1 - (Omega_b + Omega_dm + Omega_l + Omega_r)
    q_0 = Omega_r + Omega_b / 2 + Omega_dm / 2 - Omega_l
    hubble_dis = c / H_0  # in Mpc
    age_of_universe = Time(10**(-16), 1)
    age_of_universe_at_z = age_of_universe - Time(a_emit, 1)
    lookback_time = age_of_universe - age_of_universe_at_z
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

    #### Plotting distances ####

    dz = 10**(-5)  # differential redshift element
    zpoints = arange(0, 15, dz)
    distance_points = []
    angular_dis_points = []
    luminosity_dist_points = []
    dis_point = 0
    for z in zpoints:
        dis_point += H_z(z) * dz
        distance_points.append(dis_point)
        angular_dis_points.append(S_k(dis_point) / (1 + z))
        luminosity_dist_points.append(S_k(dis_point) * (1 + z))
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

    plt.plot(zpoints, luminosity_dist_points, 'g-.', label='Luminosity Distance')
    plt.ylabel('Luminosity Distance (Mpc)')
    plt.xlabel('z')
    plt.title('Luminosity Distance vs Redshift')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.show()

    layout_output = [
        [sg.Text('Results', size = (35, 1), justification = 'center', 
        font = ('Inconsolota', 15), relief = sg.RELIEF_RIDGE)],
        [sg.Text('Age of The Universe Today: {:.4f} Gyr'.format(age_of_universe))],
        [sg.Text('Age of The Universe at z:  {:.4f} Gyr'.format(
            age_of_universe_at_z))],
        [sg.Text('Lookback Time: {:.4f} Gyr'.format(lookback_time))],
        [sg.Text('Comoving Distance at z: {:.4f} Mpc'.format(comoving_distance))],
        [sg.Text('Angular Diameter Distance at  z: {:.4f} Mpc'.format(
            angular_distance))],
        [sg.Text('Luminosity Distance at z: {:.4f} Mpc'.format(luminosity_distance))],
        [sg.Exit()]
    ]
    window_output = sg.Window('CoSmoS', layout_output)
    event, values = window_output.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        window_output.close()
