import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class MPU6050():


    def __init__ (self, time_step, duration, sample_rate_divisor=0, mode="accelerometer_only", low_power_wakeup=0, digital_low_pass=0, loop_rate=60):
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
        self.digital_low_pass = digital_low_pass
        #Digital low pass filter. Enabling this lowers the sampling rate by a factor of 8. See page 12 of the 
        #register map linked below. 
        self.loop_rate = loop_rate
        #how fast the arduino loop will run. This value is kind of up in the air, but we predict that it may have an
        #affect on how fast we can read from the sensors depending on how much code is run in the loop, in Hz.

    def runSim(self):
        #active_times would be a list of tuples/list that would define the time at which the sensor was running
        # i.e. [[0,1],[4,5],[6,7]] would have the sensor running from time 0s to 1s,
        # 4s to 5s, 6s to 7s
        time = np.arange(0,self.duration,self.time_step) #time at which to collect data
        #active_vec: we are assuming that the accelerometer will constantly be on, since the slowest it will update is
        #once every 0.8 seconds.
        power = self.getPowerUsage(time)
        data = self.getDataAccumulated()

        return time, power, data

    def getPowerUsage(self, time):
        #Calculates power when sensor is active. This value is used in conjunction with 
        power_used = 0
        if(self.low_power_wakeup == 1.25):
            accel_only_power_microamps = 10
        elif(self.low_power_wakeup == 5):
            accel_only_power_microamps = 20
        elif(self.low_power_wakeup == 20):
            accel_only_power_microamps = 70
        elif(self.low_power_wakeup == 40):
            accel_only_power_microamps = 140
        else:
            accel_only_power_microamps = 500
        gyroscope_only_power_milliamps = 3.6
        gyroscope_DMP_power_milliamps = 3.7
        gyroscope_accelerometer_power_milliamps = 3.8
        gyroscope_accelerometer_DMP_power_milliamps = 3.9
        voltage = 3.3
        if(self.mode == "accelerometer_only"):
            power_used = (accel_only_power_microamps * voltage) / 1000#converted to milliamps.
        elif(self.mode == "gyroscope_only"):
            power_used = gyroscope_only_power_milliamps * voltage
        elif(self.mode == "gyroscope_DMP"):
            power_used = gyroscope_DMP_power_milliamps * voltage
        elif(self.mode == "gyroscope_accelerometer"):
            power_used = gyroscope_accelerometer_power_milliamps * voltage
        elif(self.mode == "gyroscope_accelerometer_DMP"):
            power_used = gyroscope_accelerometer_DMP_power_milliamps * voltage
        else:
            print("Invalid mode entered.")
            return -1
        
        power_usage = np.where(time, power_used, time)
        return power_usage
        #returns a vector of when power is used. Units are in mW.

    def getDataAccumulated(self):
        #this function will be heavily influenced by sample_rate_divisor. See page 11 of the register map for the full equation.
        #https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf

        measure_rate = 0
        #calculate sample rate.
        gyroscope_output_rate = (8000, 1000)[self.digital_low_pass == 1]#ternary operator. like x==1 ? y : z
        sample_rate = gyroscope_output_rate / (1 + self.sample_rate_divisor) #how fast measurements are written to
        #accelerometer measurement registers, in Hz.

        if(self.low_power_wakeup > 0):
            measure_rate = self.low_power_wakeup
        else:
            measure_rate = (self.loop_rate, sample_rate)[self.loop_rate > sample_rate]#Whichever is lower is taken, in Hz. 
        
        
        bytes_per_second = 6 * measure_rate#6 is the number of bytes per measurement.
        bytes_over_duration = bytes_per_second*self.duration
        data_accumulated = np.linspace(0, bytes_over_duration, num=int(self.duration / self.time_step))
        return data_accumulated

    def getActiveTime(self, time):
        #this function should only matter when used in conjunction with low_power_wakeup. Otherwise the accelerometer
        #runs at 1kHz and can be assumed to be always on.
        period = 1 / self.low_power_wakeup
        standby_time = 1 - period
        active_times = []
        print(active_times)
        time = time.tolist()
        length = len(time)
        standby = 5 / 1000 # default power when off
        arr = [standby] * len(time) # creating corresponding power array to time intervals, default values 

        # check if the given start and end time is a valid value in the time array and round to nearest value 
        for times in active_times:
            start = times[0]
            end = times[1]
            if times[0] not in time:
                print("start or end time is invalid, rounding to nearest whole number")
                start = round(start)

            if times[1] not in time:
                print("start or end time is invalid, rounding to nearest whole number")
                end = round(end)

            start_index = time.index(start) 
            end_index = time.index(end) 

            # calculate power here for active conversion period
            # if statement for power vs data
            
            power = self.calculate_power(time)
            for i in range(start_index, end_index+1):
                arr[i] = power   
            
        return arr


dude = MPU6050(time_step=1, duration=10, mode="gyroscope_accelerometer", low_power_wakeup=1.25).runSim()

print(dude)
ax1 = plt.subplot(311)
plt.plot(dude[0], dude[1])
plt.tick_params('x', labelsize=6)

ax2 = plt.subplot(312, sharex=ax1)
plt.plot(dude[0], dude[2])
# make these tick labels invisible
plt.tick_params('x', labelbottom=False)

plt.show()