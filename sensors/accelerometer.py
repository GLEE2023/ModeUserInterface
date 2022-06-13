import numpy as np
import matplotlib
import pandas as pd

class MPU6050():


    def __init__ (self, time_step, duration, sample_rate_divisor=0, mode="accelerometer_only", low_power_wakeup=0):
        #mode tells the type of mode the sensor is in. Choices for accelerometer are "accelerometer_only", "gyroscope_only",
        #"gyroscope_DMP", "gyroscope_accelerometer", "gyroscope_accelerometer_DMP"

        #time_step would define at what intervals (and therefore time) the model
        # would return data at. A time_step o 1 second would have the model return
        # data at 0,1,2,3... seconds assuming start time of 0 seconds.
        #
        self.mode = mode
        self.time_step = time_step
        self.duration = duration

        self.low_power_wakeup = low_power_wakeup
        #In Hz, determines how fast the sensor wakes up when in low power mode. More wakeups means more power used.
        #Choices are 1.25, 5, 20, 40.
        self.sample_rate_divisor = sample_rate_divisor
        #Value between 0 and 255. Used as a divisor for sample rate equation, higher means slower sample rate meaning
        #presumably lower data collected per second.


    def runSim(self, active_times):
        #active_times would be a list of tuples/list that would define the time at which the sensor was running
        # i.e. [[0,1],[4,5],[6,7]] would have the sensor running from time 0s to 1s,
        # 4s to 5s, 6s to 7s
        time = np.arrange([0,self.duration],self.time_step) #time at which to collect data
        active_vec = #get vector of when sensor is active
        power = getPowerUsage(time,mode,parameters_related_to_mode)
        data = getDataUsage(time,mode,parameters_related_to_mode)

        return time, power, data

    def getPowerUsage(self,time,mode,low_power_wakeup):
        #Calculates power when sensor is active. This value is used in conjunction with 
        if(low_power_wakeup == 1.25):
            accel_only_power_microamps = 10
        elif(low_power_wakeup == 5):
            accel_only_power_microamps = 20
        elif(low_power_wakeup == 20):
            accel_only_power_microamps = 70
        elif(low_power_wakeup == 40):
            accel_only_power_microamps = 140
        else:
            accel_only_power_microamps = 500
        gyroscope_only_power_milliamps = 3.6
        gyroscope_DMP_power_milliamps = 3.7
        gyroscope_accelerometer_power_milliamps = 3.8
        gyroscope_accelerometer_DMP_power_milliamps = 3.9
        voltage = 3.3
        if(mode == "accelerometer_only"):
            power_usage = (accel_only_power_microamps * voltage) / 1000
        elif(mode == "gyroscope_only"):
            power_usage = gyroscope_only_power_milliamps * voltage
        elif(mode == "gyroscope_DMP"):
            power_usage = gyroscope_DMP_power_milliamps * voltage
        elif(mode == "gyroscope_accelerometer"):
            power_usage = gyroscope_accelerometer_power_milliamps * voltage
        elif(mode == "gyroscope_accelerometer_DMP"):
            power_usage = gyroscope_accelerometer_DMP_power_milliamps * voltage
        else:
            print("Invalid mode entered.")
            return -1
        return power_usage
        #unit is mW.

    def getDataAccumulated(self,time,mode,parameters_related_to_mode,active_vec):

        return data_accumulated

    def getActiveTime(self):
        