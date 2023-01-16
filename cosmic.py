# ========== Cosmic ==========
import os.path

import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np
import PySimpleGUI as sg
from scipy.integrate import quad


N = 10**6   # step size
c = 299792.458   # speed of light [km/s]

# ==========  Important Cosmological Functions ==========

def H(a):
    """
    Hubble Parameter in terms of the scale factor

    Args:
        a [float]: The scale factor, a(t)
    """
    E_a = np.sqrt(Omega_m*(a)**(-1) + Omega_r*a**(-2) + Omega_l*a**(-1-3*w_l) + Omega_k)
    return hubble_time / E_a


def H_z(z):
    """
    Hubble Parameter in terms of the redshift

    Args:
        z [float]: The redshift, z
    """
    E_z = np.sqrt(Omega_m*(1+z)**(3) + Omega_r*(1+z)**(4) + Omega_l*(1+z)**(3+3*w_l) + Omega_k*(1+z)**2)
    return hubble_dis / E_z


def S_k(r):
    """
    Transverse comoving distance, given in terms of the comoving distance, r.

    Args:
        r [float]: The comoving distance
    """
    if Omega_k < 0:
        return (hubble_dis / np.sqrt(abs(Omega_k))) * np.sin((np.sqrt(abs(Omega_k)) * r) / hubble_dis)
    elif Omega_k == 0:
        return r
    elif Omega_k > 0:
        return (hubble_dis / np.sqrt(Omega_k)) * np.sinh((np.sqrt(Omega_k) * r) / hubble_dis)


def distancePlotter():
    """
    Plotting distances
    """
    dz = 10**(-5)  # differential redshift element
    z_values = np.arange(0, 14, dz)
    comoving_dist_points = []
    angular_dist_points = []
    luminosity_dist_points = []
    dis_point = 0
    for z in z_values:
        dis_point += H_z(z) * dz
        comoving_dist_points.append(dis_point)
        angular_dist_points.append(S_k(dis_point) / (1 + z))
        luminosity_dist_points.append(S_k(dis_point) * (1 + z))

    # Plotting Options
    fig, ax0 = plt.subplots()
    ax0.plot(z_values, comoving_dist_points, 'r')
    # Setting Limits
    ax0.set_xlim(0, 14)
    # Setting Labels
    ax0.set_xlabel('$z$')
    ax0.set_ylabel('$\chi$ (Mpc)')
    ax0.set_title('Comoving Distance vs Redshift')
    # Minor Ticks
    ax0.yaxis.set_ticks_position('both')
    ax0.xaxis.set_ticks_position('both')
    ax0.yaxis.set_minor_locator(tck.AutoMinorLocator())
    # Tick Options
    ax0.tick_params(which='major', width=1, size=7, direction='in')
    ax0.tick_params(which='minor', width=0.6, size=4, direction='in')
    plt.show()

    fig, ax1 = plt.subplots()
    ax1.plot(z_values, angular_dist_points, 'b')
    # Setting Limits
    ax1.set_xlim(0, 14)
    # Setting Labels
    ax1.set_xlabel('$z$')
    ax1.set_ylabel('$d_A$ (Mpc)')
    ax1.set_title('Angular Diameter Distance vs Redshift')
    # Minor Ticks
    ax1.yaxis.set_ticks_position('both')
    ax1.xaxis.set_ticks_position('both')
    ax1.yaxis.set_minor_locator(tck.AutoMinorLocator())
    # Tick Options
    ax1.tick_params(which='major', width=1, size=7, direction='in')
    ax1.tick_params(which='minor', width=0.6, size=4, direction='in')
    plt.show()

    fig, ax2 = plt.subplots()
    plt.plot(z_values, luminosity_dist_points, 'g')
    # Setting Limits
    ax2.set_xlim(0, 14)
    # Setting Labels
    ax2.set_xlabel('$z$')
    ax2.set_ylabel('$d_L$ (Mpc)')
    ax2.set_title('Luminosity Distance vs Redshift')
    # Minor Ticks
    ax2.yaxis.set_ticks_position('both')
    ax2.xaxis.set_ticks_position('both')
    ax2.yaxis.set_minor_locator(tck.AutoMinorLocator())
    # Tick Options
    ax2.tick_params(which='major', width=1, size=7, direction='in')
    ax2.tick_params(which='minor', width=0.6, size=4, direction='in')
    plt.show()


# ========== GUI ==========

# PySimpleGUI Theme Option
sg.change_look_and_feel('SandyBeach')

layout_input = [
    [sg.Frame(layout=[
        [sg.Image(os.path.normpath('res/h0.png')),
         sg.InputText(default_text='67.36', font=('Tahoma', 12))],
        [sg.Image(os.path.normpath('res/omega_matter.png')),
         sg.InputText(default_text='0.3369', font=('Tahoma', 12))],
        [sg.Image(os.path.normpath('res/omega_lambda.png')),
         sg.InputText(default_text='0.6847', font=('Tahoma', 12))],
        [sg.Image(os.path.normpath('res/omega_radiation.png')),
         sg.InputText(default_text='0.00009', font=('Tahoma', 12))],
        [sg.Image(os.path.normpath('res/z.png')),
         sg.InputText(default_text='3', font=('Tahoma', 12))],
        [sg.Image(os.path.normpath('res/w_lambda.png')),
         sg.InputText(default_text='-1', font=('Tahoma', 12))]],
        title='Cosmological Parameters', font=('Georgia', 14))],
    [sg.Submit(button_color='blue'),
     sg.Exit(button_color='red')]
]

window_input = sg.Window('Cosmic', layout_input)
event, values = window_input.read()
while True:
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Submit':
        H_0, Omega_m, Omega_l, Omega_r, z, w_l = [float(values[i]) for i in range(1, 13, 2)]

        # derived parameters
        hubble_time = (((1 / H_0) * (3.086e+19)) / (3.154e+7)) / 10**9  # in Gyr
        a_emit = 1 / (1 + z)
        Omega_k = 1 - (Omega_m + Omega_l + Omega_r)
        q_0 = Omega_r + (Omega_m / 2) - Omega_l
        hubble_dis = c / H_0   # in Mpc

        # calculated parameters
        age_of_universe = quad(H, 10**(-16), 1)[0]
        age_of_universe_at_z = age_of_universe - quad(H, a_emit, 1)[0]
        lookback_time = age_of_universe - age_of_universe_at_z
        comoving_distance = quad(H_z, 0, z)[0]
        luminosity_distance = (1 + z) * S_k(comoving_distance)
        angular_distance = S_k(comoving_distance) / (1 + z)

        # plotting distances
        distancePlotter()

        layout_output = [
            [sg.Frame(layout=[
                [sg.Text('Age of The Universe Today: {:.4f} Gyr'.format(age_of_universe), font=('Tahoma', 12))],
                [sg.Text('Age of The Universe at Redshift {}:  {:.4f} Gyr'.format(z, age_of_universe_at_z), font=('Tahoma', 12))],
                [sg.Text('Lookback Time: {:.4f} Gyr'.format(lookback_time), font=('Tahoma', 12))],
                [sg.Text('Comoving Distance at Redshift {}: {:.4f} Mpc'.format(z, comoving_distance), font=('Tahoma', 12))],
                [sg.Text('Angular Diameter Distance at Redshift {}: {:.4f} Mpc'.format(z, angular_distance), font=('Tahoma', 12))],
                [sg.Text('Luminosity Distance at Redshift {}: {:.4f} Mpc'.format(z, luminosity_distance),
                    font=('Tahoma', 12))]], title='Results',  font=('Georgia', 14))
             ]
        ]
        window_output = sg.Window('Cosmic', layout_output)
        event, values = window_output.read()
        if event == sg.WIN_CLOSED:
            window_output.close()
