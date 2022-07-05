from Sensor import Sensor
import matplotlib.pyplot as plt
import numpy as np
from typing import List

#class for the capacative sensor. wont have too much functionality since 
#we only know of its data usage.
class CAP11NA(Sensor):
    def __init__(self, loop_rate, duration, time_step):
        self.loop_rate = loop_rate
        self.duration = duration
        self.time_step = time_step
        self.time = np.arange(0,self.duration,self.time_step)

    def runSim(self, active_times: List[tuple]) -> int:
        """
        Returns time, power, data vectors and plot.

        args:
            active_times (list): list of active time tuples in the form of 
            [(int(start1), int(end1), "mode1"), (int(start2), int(end2), "mode2")]
        returns:
            self.time, power, data. all vectors used in plotting
        """
        #active_times would be a list of tuples/list that would define the time at which the sensor was running
        # i.e. [[0,1],[4,5],[6,7]] would have the sensor running from time 0s to 1s,
        # 4s to 5s, 6s to 7s
        self.time = np.arange(0,self.duration,self.time_step) #time at which to collect data
        try:
            power, data = self.getVectors(active_times)
            self.plotData(power, data, self.time, active_times)
            return self.time, power, data
        except TypeError as e:
            print("A type error occurred. Your active times array may exceed the duration set in MPU6050 object.", e)
            return -1
    
    def getVectors(self, active_times: List[tuple]) -> tuple:
        """
        Returns time and data vectors used in plotting.

        args:
            active_times(list): list of active times tuples in the form
            [(int(start1), int(end1), "mode1"), (int(start2), int(end2), "mode2")].
        returns:
            power_arr, data_arr both numpy arrays representing power and data over time.
        """
        length = len(self.time)
        cap_estimated_power_usage = 1 #in mW
        powerarr = [0] * length # creating corresponding power array to time intervals, default values 
        dataarr = [0] * length
        # check if the given start and end time is a valid value in the time array and round to nearest value 
        for times in active_times:
            start_index = int(times[0] / self.time_step) # getting index of the closest value to active times 
            end_index = int(times[1] / self.time_step)
            if start_index < 0 or end_index > len(self.time): 
                print("Error. Index not valid.")
                return -1
            
            for i in range(start_index, length):
                powerarr[i] = cap_estimated_power_usage
                if i == 0:
                    dataarr[i] = self.getBytesPerSecond()
                else:
                    dataarr[i] = dataarr[i-1] + self.getBytesPerSecond()
            
        return np.array(powerarr), np.array(dataarr)

    
    def getBytesPerSecond(self):
        """
        Returns number of bytes per second based on loop rate.

        args:
            None
        returns:
            An integer representation of bytes per second.
        """
        cap_bytes_per_second = 2
        return self.loop_rate * cap_bytes_per_second

