import numpy as np
import matplotlib.pyplot as plt

class Sensor:
    def __init__(self, **config):
        self.__dict__.update(config)
        #config is a dictionary of variable length.
        #Initialization of the child sensors would be like this:
        #accelerometer(mode="accelerometer_only", sample_rate_divisor=142, etc=etc)

    def getPowerUsage(self,power_used,time):
        #Not working!
        power = np.full_like(time, power_used)
        return power #things ready to be plotted

    def getDataAccumulated(self, active_vector, bits_per_second):
        #in development!
        data_vector = []
        tracker = 0
        for i in active_vector:
            if i != 0:
                tracker += bits_per_second
            data_vector.append(tracker)
            
        return data_vector
    
    def getActiveTimes(self, active_times):
        #time = time.tolist()
        length = len(self.time)
        arr = [0] * length # creating corresponding power array to time intervals, default values 

        # check if the given start and end time is a valid value in the time array and round to nearest value 
        for times in active_times:
            start_index = int(times[0] / self.time_step) # getting index of the closest value to active times 
            end_index = int(times[1] / self.time_step)
            
            if start_index < 0 or end_index > len(self.time): 
                print("Error. Index not valid.")
                return -1
            
            for i in range(start_index, end_index+1):
                arr[i] = 1
        return arr
    
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
        data_value_limit = [0,500]
        ax1.set_ylim(data_value_limit)
        ax2.set_ylabel('Bytes')
        ax2.set_xlabel('Seconds')
        plt.show()

    def showParams(self):
        for k,v in self.__dict__.items():
            print(k,v)

#data acculumation testing stuff below
timearr = np.arange(0,0.5,0.0155)
dude = Sensor(time=timearr, time_step=0.0155)
active = dude.getActiveTimes([[0.05,0.1],[0.3,0.4]])
data = dude.getDataAccumulated(active, 16)

#print(active)
#print(data, len(data))
dude.showParams()
