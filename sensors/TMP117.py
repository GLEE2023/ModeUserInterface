import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class TMP117():
    def __init__(self, time_step, duration, activeTimeParams): 
        self.time_step = time_step
        self.duration = duration
        self.time = np.arange(0, duration, time_step) #time at which to collect data
        self.activeTimeParams = activeTimeParams
        
#    def errorCheck():
#         for 
#             if convCycleTime == 0:
#                 print("error. conv cycle time cannot be zero, please check parameters again.")
                
    def computePower(self, num_averages, convCycleTime, mode):
        activeCurrentConsumption = 135 # micro amps
        activeConversionTime = num_averages*0.0155

        standByCurrentConsumption = 1.25 # micro amps
        standbyTime = convCycleTime - activeConversionTime
        
        SDcurrent = 250/ 1000000 # micro amps
        
        if mode == "CC":
            current = ((activeCurrentConsumption*activeConversionTime)+(standByCurrentConsumption*standbyTime))/convCycleTime

        elif mode == "OS":
            current = ((activeCurrentConsumption*activeConversionTime)+(SDcurrent*standbyTime))/convCycleTime
            
        power = (current * 3.3)/1000 # milli watts
        
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
            averages = self.activeTimeParams[times][0]
            convCycle = self.activeTimeParams[times][1]
            power = self.computePower(averages, convCycle, mode)
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
        
        bits_per_cycle = 16
        
        length = len(self.time)
        data_arr = [0] * length # creating corresponding power array to time intervals, default values 
        data_accumulated = 0
        
        for times in self.activeTimeParams: # for each active period
            start_index = int(times[0] / self.time_step) 
            end_index = int(times[1] / self.time_step)
            
            #calculating data per step in active time period
            convCycle = self.activeTimeParams[times][1]
            bits_per_second = bits_per_cycle / convCycle # bits per second
            activeTimeTotal = times[1]-times[0] # getting num of seconds of active period
            bits_total = bits_per_second * activeTimeTotal # total bits during that active period
            num_steps = end_index-start_index 
            bits_per_step = bits_total / num_steps
            #indexes[time] = bits_per_step
            
            for i in range(start_index, length):
                if i < end_index:
                    data_accumulated += bits_per_step
                    
                data_arr[i] = data_accumulated 
            
        return data_arr

    def Simulation(self):
        power = self.getAllModesPower()
        data = self.getAllModesData()

        return power, data, self.time