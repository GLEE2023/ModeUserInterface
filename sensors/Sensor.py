import numpy as np
import matplotlib.pyplot as plt
from typing import List

class Sensor:
    #array of all available modes for each sensor. We are planning on using it for error checking
    #in getActiveTimes.
    allSensorModes = [
        "OS","CC","accelerometer_only","gyroscope_only","gyroscope_DMP","gyroscope_accelerometer",
        "gyroscope_accelerometer_DMP"
    ]

    def __init__(self, **config):
        self.__dict__.update(config)
        #config is a dictionary of variable length.
        #Initialization of the child sensors would be like this:
        #accelerometer(mode="accelerometer_only", sample_rate_divisor=142, etc=etc)

    # def getPowerUsage(self,power_used,time):
    #     #Not working!
    #     power = np.full_like(time, power_used)
    #     return power #things ready to be plotted

    def getDataAccumulated(self, active_vector, bits_per_second):
        #in development!
        data_vector = []
        tracker = 0
        for i in active_vector:
            if i != 0:
                tracker += bits_per_second
            data_vector.append(tracker)
            
        return data_vector
    
    # def getActiveTimes(self, active_times: List[tuple]) -> List:
    #     #active times is a list of tuples. First two elements are start and end times, third is 
    #     length = len(self.time)
    #     arr = [0] * length # creating corresponding power array to time intervals, default values 

    #     # check if the given start and end time is a valid value in the time array and round to nearest value 
    #     for times in active_times:
    #         start_index = int(times[0] / self.time_step) # getting index of the closest value to active times 
    #         end_index = int(times[1] / self.time_step)
            
    #         if start_index < 0 or end_index > len(self.time): 
    #             print("Error. Index not valid.")
    #             return -1
            
    #         for i in range(start_index, end_index+1):
    #             arr[i] = times[2]
    #     return arr
    
    def plotData(self, power_vector, data_vector, time_vector, **params):
        #basic function to plot power and data vs time. 
        f = plt.figure(figsize=(10,10))
        ax1 = f.add_subplot(311)
        power_plot, = plt.plot(time_vector, power_vector)
        plt.tick_params('x', labelbottom=False)
        power_value_limit = [0,50]
        ax1.set_ylim(power_value_limit)
        ax1.set_ylabel('mW')

        ax2 = f.add_subplot(312, sharex=ax1)
        data_plot, = plt.plot(time_vector, data_vector)
        # make these tick labels invisible
        plt.tick_params('x', labelsize=6)
        #data_value_limit = [0,500]
        #ax2.set_ylim(data_value_limit)
        ax2.set_ylabel('Bytes')
        ax2.set_xlabel('Seconds')
        plt.show()

    def showParams(self):
        for k,v in self.__dict__.items():
            print(k,v)
