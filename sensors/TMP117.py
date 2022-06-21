import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class TMP117():
    def __init__(self, time_step, duration, activeTimeParams): 
        self.time_step = time_step
        self.duration = duration
        self.time = np.arange(0, duration, time_step) #time at which to collect data
        self.activeTimeParams = activeTimeParams
        
    def computePower(self, num_averages, conv_cycle):
        standby = 1.25 / 1000 # default power when active conversion is off
        power = 0
    
        standByCurrentConsumption = 1.25
        activeCurrentConsumption = 135
        convCycleTime = conv_cycle
        num_averages = num_averages
        activeConversionTime = num_averages*0.0155
        standbyTime = convCycleTime - activeConversionTime
        
        if convCycleTime == 0:
            current = convCycleTime
        else: current = ((activeCurrentConsumption*activeConversionTime)+(standByCurrentConsumption*standbyTime))/convCycleTime
        power = (current * 3.3) / 1000
        
        return power
    
    def getAllModesPower(self):
        length = len(self.time)
        power_arr = [0] * length # creating corresponding power array to time intervals, default values

        # check if the given start and end time is a valid value in the time array and round to nearest value 
        for times in self.activeTimeParams:
            start_index = int(times[0] / self.time_step) # getting index of the closest value to active times 
            end_index = int(times[1] / self.time_step)

            if start_index < 0 or end_index > len(self.time): # not valid time
                print("Error. Index not valid.")
                return -1

            mode = self.activeTimeParams[times][2]
            power = self.computePower(self.activeTimeParams[times][0], self.activeTimeParams[times][1])
            for i in range(start_index, end_index):
                power_arr[i] = power
        
        return power_arr
            
    def getAllModesData(self):
        '''
        The data in the result register is in two's complement format, 
        has a data width of 16 bits and a resolution of 7.8125 m°C.
        
        Changing the conversion cycle period also affects the temperature result update rate because the temperature 
        result register is updated at the end of every active conversion. 
        
        Storing 16-bit value at the end of each conversion cycle
        '''
        
        #bits_per_cycle = 16
        
        #how_many_timesteps_in_active_period = active_period/timestep
        
        #bits_per_timestep = active_period/16
        
        length = len(self.time)
        data_arr = [0] * length # creating corresponding power array to time intervals, default values 
        increment = 16
        data = 0

        for index, mode in enumerate(arr):
            # first time sensor is turned on
            
            if mode == 0:
                data_arr[index] = data

            elif mode == "OS":
                data = data + 16
                data_arr[index] = data
            
            elif mode == "CC":
                pass
            
        return data_arr

    def Simulation(self):
        power = self.getAllModesPower()
        data = self.getAllModesData()

        return power, data