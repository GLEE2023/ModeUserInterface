import numpy as np

class Sensor:
    def __init__(self, **config):
        self.__dict__.update(config)
        #config is a dictionary of variable length.
        #Initialization of the child sensors would be like this:
        #accelerometer(mode="accelerometer_only", sample_rate_divisor=142)

    def getPowerUsage(self,power_used,time):
        power = np.full_like(time, power_used)
        return power #things ready to be plotted

    def getDataAccumulated():
        return None
    
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
    
    #paramDict = {"mode":"cc","param1":nun,"param2"......}
    # modes options: "cc", "sleep",

    #parameters for "CC"
    #   param1: ""
    #   param2:""


    # paramaters for fjjsdjlkfsdfjklfdjkls

