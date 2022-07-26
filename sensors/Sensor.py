import numpy as np
import matplotlib.pyplot as plt
import random

class Sensor:
    #array of all available modes for each sensor. We are planning on using it for error checking
    #in getActiveTimes.

    def __init__(self, **config):
        self.__dict__.update(config)
        #config is a dictionary of variable length.
        #Initialization of the child sensors would be like this:
        #accelerometer(mode="accelerometer_only", sample_rate_divisor=142, etc=etc)

    
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
    
    def plotData(self, power_vector, data_vector, time_vector, active_times):
        #basic function to plot power and data vs time. 
        f = plt.figure(figsize=(10,10))
        ax3 = f.add_subplot(311)
        #plt.tick_params('x', labelbottom=False) 
        ticks = {}
        colors = []
        for i in range(len(active_times)):
            color = "#%06x" % random.randint(0, 0xFFFFFF)
            colors.append(color)
        for i,v in enumerate(active_times):
            if v[2] not in ticks.keys():
                ticks[v[2]] = i
            #Plotting mode active times. We move each end a bit inwards because line width is bugged.
            plt.plot([v[0] + time_vector[-1]*0.005,v[1]-time_vector[-1]*0.005], [ticks[v[2]],ticks[v[2]]], color=colors[ticks[v[2]]], linewidth=5)
        plt.yticks(list(ticks.values()),list(ticks.keys()))
        
        
        ax1 = f.add_subplot(312, sharex=ax3)
        plt.grid(visible=True)
        power_plot, = plt.plot(time_vector, power_vector)
        plt.tick_params('x', labelbottom=False)
        #power_value_limit = [0,0.1]
        #ax1.set_ylim(power_value_limit)
        ax1.set_ylabel('Power (mW)')

        ax2 = f.add_subplot(313, sharex=ax3)
        plt.tick_params('x', labelsize=12)
        data_plot, = plt.plot(time_vector, data_vector)
        # make these tick labels invisible
        plt.tick_params('x', labelsize=12)
        #data_value_limit = [0,500]
        #ax2.set_ylim(data_value_limit)
        ax2.set_ylabel('Data (Bytes)')
        ax2.set_xlabel('Seconds')

        plt.show()