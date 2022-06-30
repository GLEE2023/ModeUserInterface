import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from Sensor import Sensor
from typing import List

class TP(Sensor):

    def __init__ (self, time_step, duration, loop_rate=60):
        #mode tells the type of mode the sensor is in. Choices for TP are "TP_only"
        #time_step would define at what intervals (and therefore time) the model will be running
        # data at 0,1,2,3... seconds assuming start time of 0 seconds.

        self.time_step = time_step
        self.duration = duration

        self.loop_rate = loop_rate
        #how fast the arduino loop will run. This value is kind of up in the air, but we predict that it may have an
        #affect on how fast we can read from the sensors depending on how much code is run in the loop, in Hz.
        self.time = np.arange(0,self.duration,self.time_step)
    

    def runSim(self, active_times: List[tuple]) -> int:
        #active_times would be a list of tuples/list that would define the time at which the sensor was running
        # i.e. [[0,1],[4,5],[6,7]] would have the sensor running from time 0s to 1s,
        # 4s to 5s, 6s to 7s
        self.time = np.arange(0,self.duration,self.time_step) #time at which to collect data
        try:
            power, data = self.getVectors(active_times)
            self.plotData(power, data, self.time, active_times)
            return self.time, power, data
        except TypeError as e:
            print("A type error occurred. Your active times array may exceed the duration set in TP object.", e)
            return -1

    def getModePower(self, mode):
        #Calculates power when sensor is active. This value is used in conjunction with
        self.mode = mode
        power_used = 0
        TP_power_microamps = 0
        voltage = 3.3
        if(mode == "TP_only"):
            TP_power_microamps = 15
            power_used = (TP_power_microamps * voltage) / 1000 #converted to milliamps.
        elif(mode == "TP_off"):
            TP_power_microamps = 0
            power_used = (TP_power_microamps * voltage) / 1000 #converted to milliamps.
        else:
            print("Invalid mode entered.")
            return -1
        return power_used
        #returns a vector of when power is used. Units are in mW.

    def getVectors(self, active_times: List[tuple]) -> tuple:
        #active times is a list of tuples. First two elements are start and end times, third is 
        length = len(self.time)
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
                powerarr[i] = self.getModePower(times[2])
                if i == 0:
                    dataarr[i] = self.getBytesPerSecond(times[2])
                else:
                    dataarr[i] = dataarr[i-1] + self.getBytesPerSecond(times[2])
            
        return powerarr, dataarr

    def getBytesPerSecond(self, mode):
        measure_rate = 0
        self.getModePower(mode)
        #calculate sample rate.
        sample_rate = 0.64 #how fast measurements are written to
        #TP measurement registers, in Hz.

        measure_rate = (self.loop_rate, sample_rate)[self.loop_rate > sample_rate]#Whichever is lower is taken, in Hz. 
        
        if(mode == "TP_only"):
            return 6*measure_rate
        else:
            return 12*measure_rate
