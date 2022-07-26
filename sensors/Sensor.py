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

    
    
    def plotData(self, power_vector, data_vector, time_vector, active_times):
        #basic function to plot power and data vs time. 
        f = plt.figure(figsize=(10,10))
        ax3 = f.add_subplot(311)
        plt.tick_params('x', labelbottom=False)
        ticks = {}
        colors = []
        for i in range(len(active_times)):
            color = "#%06x" % random.randint(0, 0xFFFFFF)
            colors.append(color)
        for i,v in enumerate(active_times):
            if v[2] not in ticks.keys():
                ticks[v[2]] = i
            plt.plot([v[0],v[1]],[ticks[v[2]],ticks[v[2]]],color=colors[ticks[v[2]]])
        plt.yticks(list(ticks.values()),list(ticks.keys()))
        
        line = np.full_like(time_vector, 1)
        
        ax1 = f.add_subplot(312, sharex=ax3)
        plt.grid(visible=True)
        power_plot, = plt.plot(time_vector, power_vector)
        plt.tick_params('x', labelbottom=False)
        #power_value_limit = [0,0.1]
        #ax1.set_ylim(power_value_limit)
        ax1.set_ylabel('Average Power (mW)', fontsize=15)

        ax2 = f.add_subplot(313, sharex=ax3)
        plt.plot(time_vector, data_vector)
        # make these tick labels invisible
        plt.tick_params('x', labelsize=12)
        #data_value_limit = [0,500]
        #ax2.set_ylim(data_value_limit)
        ax3.set_ylabel('Active Modes', fontsize=15)
        ax2.set_ylabel('Average Data (Bytes)', fontsize=15)
        ax2.set_xlabel('Time (s)', fontsize = 20)

        plt.show()