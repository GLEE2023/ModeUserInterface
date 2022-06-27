# SM141K.py
# Slightly modified by Luke Roberson from work by James Bohn and John Aldrete
import numpy as np
import plotly.graph_objects as go
from matplotlib import pyplot as plt
import sys as sys


class SM141K():
    def __init__(self, start_time_hrs, duration_hrs, time_step_seconds, latitude, solar_constant=1360, surface_area=.0008772, cell_efficiency=0.25):

        self.start_time         = start_time_hrs
        self.duration           = duration_hrs
        self.end_time           = start_time_hrs+duration_hrs
        self.time_step          = time_step_seconds/3600
        self.latitude           = latitude
        self.solar_constant     = solar_constant # W/m^2
        self.surface_area       = surface_area #m^2
        self.cell_efficiency    = cell_efficiency

# Assumptions:
    # Solar output is constant - real variance is ~.1% over 11 year cycles
    # Variance in moons distance to sun is negligable (constant 1 AU) - real daily variance is ~.5%, yearly ~3.5%
    # Solar panel power efficiency is not dependent on angle of incidence - not mentioned in datasheet
    # No effect on irradiance by moons atmosphere - atmosphere is practically non existant
    # No irradiance on the dark side - if there was any it would be EXTREMELY small

    # returns power in milliwatts as a function of psi
    def power(self, psi):
        return np.cos(psi) * self.solar_constant * self.surface_area * self.cell_efficiency * 1000

    # Analytical Equation for the Dayside Temperature (from Hurley et al, 2015)
    def temp(self, psi):
        return (262*(np.sqrt(np.cos(psi)))) + 130

    def psi(self, lat, time):

        # Bounds check latitude
        if (abs(lat)>90):
            sys.exit('Error. Latitude should be less than 90 degrees!')
        else:
            pass

        # Bounds check time
        if ((time < 6) or (time > 18)):
            sys.exit('Error. Time should be between dawn (0600) and dusk (1800) for the dayside!')
        else:
            pass

        time_angle_midnight = ((time/24)*(2*np.pi))%(2*np.pi)
        time_angle_noon = np.pi - time_angle_midnight

        # Define co-ordinate system
        # +z - out of the page (from the moon to the sun)
        # +y - from right to left in the page
        # +x - from bottom to top, in the page

        # Initial position vector - (x,y,z) triplet: [0,0,1]

        r = np.mat(np.array([[0],[0],[1]]))

        # 1. Latitudinal rotation

        # Given our co-ordinate system, latitudinal rotation is a rotation about the y-axis
        # Rotation matrix for rotation about the y-axis is:
        # [cos(theta), 0, sin(theta); 0, 1, 0; -sin(theta), 0, cos(theta)]

        lat_rad = (lat*np.pi/180)

        t11 = np.cos(lat_rad)
        t13 = np.sin(lat_rad)
        t31 = -t13
        t33 = t11

        R_y = np.mat(np.array([[t11,0,t13],[0,1,0],[t31,0,t33]]))

        r1 = R_y*r

        # 2. Longitudinal rotation

        # Rotate about the +x axis by the angle from noon.
        # R_x = [1, 0, 0; 0, cos(theta), -sin(theta); 0, sin(theta), cos(theta)]

        C = np.cos(time_angle_noon)
        S = np.sin(time_angle_noon)

        R_x = np.mat(np.array([[1,0,0],[0,C,-S],[0,S,C]]))
        r2 = R_x*r1

        # 3. Now taking the dot product, dividing by the square of the magnitudes of the vectors, and then taking cosine inverse.
        # Since we used unit vectors, we're basically only taking the cosine inverse.

        dot_product = r[0,0]*r2[0,0] + r[1,0]*r2[1,0] + r[2,0]*r2[2,0]
        psi = np.arccos(dot_product)

        return psi

    def model(self, start_time=None, end_time=None, time_step=None, latitude=None):
        if start_time==None: start_time = self.start_time
        if end_time==None: end_time = self.end_time
        if time_step==None: time_step = self.time_step
        if latitude==None: latitude = self.latitude

        times = np.arange(start_time, end_time, time_step)
        output = np.zeros(len(times))

        for i in range(len(times)):
            time = times[i]
            time %= 24
            if time < 6 or time > 18:
                continue

            output[i] = self.power(self.psi(latitude, time))

        return times, output

    def plotPowerAvailable(self):
        times,output = self.model()

        fig, ax = plt.subplots(figsize=(12,6))
        ax.plot(times, output, color="steelblue")
        ax.set_title("Solar Power Test", fontsize=20)
        ax.set_xlabel("Time", fontsize=16)
        ax.set_ylabel("incidince", fontsize=16)

        ax.grid(True, alpha=0.25)
        plt.show()



if __name__ == '__main__':
    solar_panel_model = SM141K(start_time_hrs=12,duration_hrs=1,time_step_seconds=1,latitude=0)
    solar_panel_model.plotPowerAvailable()
