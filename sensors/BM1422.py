from Sensor import Sensor
import matplotlib.pyplot as plt
import numpy as np
from typing import List


#Magnetometer class. has code from accelerometer, doesnt work at the moment.
class BM1422(Sensor):
    """
        modes: continuous mode, single mode
        averaging: register0x40 [000]:4times [001]:1times [010]:2times [011]:8times [100]:16times
        average current during measurements: typ-150ua max-300ua
        sample size, rate:
        timing: 10hz, 20hz, 100hz, 1000hz

        foo = BM1422(loop_rate=20, duration=360, time_step=1)
        #for magnetometer, the certain mode is the timing specification, or standby.
        modedict = {"1000":10, "standby":10,"10":40}
        mag_activetimes = generateActiveList(total_time=360, modedict=modedict)
        foo.runSim(mag_activetimes)
    """
    def __init__(self, duration, time_step, loop_rate, averaging=4, timing=10):
        self.averaging = averaging
        self.timing = timing
        self.duration = duration
        self.time_step = time_step
        self.loop_rate = loop_rate

    def runSim(self, active_times: List[tuple]) -> int:
        """
            This function will call the errorCheck(), getAllModesPower(), getAllModesData() functions. It first checks if the params
            for this sensor are valid and then calls the functions to get the power and data info.

            Args: none

            Returns: 
                power (numpy array)
                data (numpy array)
                time (numpy array)
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

    def getModePower(self, mode):
        power_used = 0
        if mode == "standby":
            standby_current = 5
            voltage = 3.3
            power_used = (standby_current * voltage) / 1000 #conversion to mW
        else:
            power_used = 1 #in mW, overestimation.
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
            
        return np.array(powerarr), np.array(dataarr)


    def getBytesPerSecond(self, timing):
        time_limit = 0
        if timing == "standby":
            return 0
        if int(timing) < self.loop_rate:
            time_limit = int(timing)
        else:
            time_limit = self.loop_rate
        measurement_bits = 6
        return measurement_bits * time_limit