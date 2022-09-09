#---------- CoSmoS (GUI Based Cosmology Evolution Calculator) ----------#

import matplotlib.pyplot as plt
import PySimpleGUI as sg
from numpy import arange, sin, sinh, sqrt
from scipy.integrate import quad

N = 10**6   # step size
c = 299792.458   # speed of light [km/s]

#---------- Important Cosmological Functions ----------#


def H(a):
    """
    Hubble Parameter in terms of the scale factor (a(t)).

    Args:
        a [float]: The scale factor, a(t)
    """
    E_a = sqrt(Omega_m*(a)**(-1) + Omega_r*a**(-2) + Omega_l*a**(-1-3*w_Λ) + Omega_k)
    return hubble_time / E_a


def H_z(z):
    """
    The Hubble Parameter in terms of the redshift (z).

    Args:
        z [float]: The redshift, z
    """
    E_z = sqrt(Omega_m*(1+z)**(3) + Omega_r*(1+z)**(4) + Omega_l*(1+z)**(3+3*w_Λ) + Omega_k*(1+z)**2)
    return hubble_dis / E_z


def S_k(r):
    """
    Transverse co-moving distance, given in terms of the co-moving distance, r.

    Args:
        r [float]: The co-moving distance
    """
    if Omega_k < 0:
        return (hubble_dis / sqrt(abs(Omega_k))) * sin((sqrt(abs(Omega_k)) * r) / hubble_dis)
    elif Omega_k == 0:
        return r
    elif Omega_k > 0:
        return (hubble_dis / sqrt(Omega_k)) * sinh((sqrt(Omega_k) * r) / hubble_dis)


def distancePlotter():
    """
    Plotting distances
    """
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
    plt.plot(zpoints, distance_points, 'r', label='Co-moving Distance')
    plt.ylabel('Co-moving Distance (Mpc)')
    plt.xlabel('z')
    plt.title('Co-moving Distance vs Redshift')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.show()

    plt.plot(zpoints, angular_dis_points, 'b--',
             label='Angular diameter distance')
    plt.ylabel('Angular Diameter Distance (Mpc)')
    plt.xlabel('z')
    plt.title('Angular Diameter Distance vs Redshift')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.show()

    plt.plot(zpoints, luminosity_dist_points,
             'g-.', label='Luminosity Distance')
    plt.ylabel('Luminosity Distance (Mpc)')
    plt.xlabel('z')
    plt.title('Luminosity Distance vs Redshift')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.show()

#---------- GUI - CoSmoS  ----------#


# PySimpleGUI Theme Option
sg.change_look_and_feel('SandyBeach')


layout_input = [
    [sg.Frame(layout=[
        [sg.Image(r'GUI Images\H0.png'),
         sg.InputText(default_text='67.36', font=('Tahoma', 12))],
        [sg.Image(r'GUI Images\Omegam.png'),
         sg.InputText(default_text='0.3369', font=('Tahoma', 12))],
        [sg.Image(r'GUI Images\OmegaL.png'),
         sg.InputText(default_text='0.6847', font=('Tahoma', 12))],
        [sg.Image(r'GUI Images\Omegar.png'),
         sg.InputText(default_text='0.00009', font=('Tahoma', 12))],
        [sg.Image(r'GUI Images\z.png'),
         sg.InputText(default_text='3', font=('Tahoma', 12))],
        [sg.Image(r'GUI Images\wL.png'),
         sg.InputText(default_text='-1', font=('Tahoma', 12))]],
        title='Cosmological Parameters', font=('Georgia', 14))],
    [sg.Submit(button_color='blue'),
     sg.Exit(button_color='red')]
]

window_input = sg.Window('CoSmoS', layout_input)
event, values = window_input.read()
while True:
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Submit':
        H_0, Omega_m, Omega_l, Omega_r, z, w_Λ = [
            float(values[i]) for i in range(1, 13, 2)]

        # derived parameteres
        hubble_time = (((1 / H_0) * (3.086e+19)) /
                       (3.154e+7)) / 10**9  # in Gyr
        a_emit = 1 / (1 + z)
        Omega_k = 1 - (Omega_m + Omega_l + Omega_r)
        q_0 = Omega_r + Omega_m / 2 - Omega_l
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
                [sg.Text('Age of The Universe Today: {:.4f} Gyr'.format(
                    age_of_universe), font=('Tahoma', 12))],
                [sg.Text('Age of The Universe at Redshift {}:  {:.4f} Gyr'.format(
                    z, age_of_universe_at_z), font=('Tahoma', 12))],
                [sg.Text('Lookback Time: {:.4f} Gyr'.format(
                    lookback_time), font=('Tahoma', 12))],
                [sg.Text('Co-moving Distance at Redshift {}: {:.4f} Mpc'.format(
                    z, comoving_distance), font=('Tahoma', 12))],
                [sg.Text('Angular Diameter Distance at Redshift {}: {:.4f} Mpc'.format(
                    z, angular_distance), font=('Tahoma', 12))],
                [sg.Text('Luminosity Distance at Redshift {}: {:.4f} Mpc'.format(z, luminosity_distance),
                         font=('Tahoma', 12))]], title='Results',  font=('Georgia', 14))
             ]
        ]
        window_output = sg.Window('CoSmoS', layout_output)
        event, values = window_output.read()
        if event == sg.WIN_CLOSED:
            window_output.close()
