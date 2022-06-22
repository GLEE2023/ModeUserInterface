# Modes for Thermopile
# Power Usage - 1 mode at 15 microA * 3.3V that we are running at

# Data Usage - 
# Presence detection - 8 bits
# Motion detection - 8 bits
# Ambient temperature shock detection = 8bits
# Over temperature detection -

# 17 bits and 15 buts 


#  TPobject is the thermopile raw value
#  



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from Sensor import Sensor
from typing import List


class TP(Sensor):

    #DEPRECATED! Thought I would keep around just in case.
    # def __init__ (self, time_step, duration, sample_rate_divisor=0, mode="accelerometer_only", low_power_wakeup=0, digital_low_pass=0, loop_rate=60):
    #     #mode tells the type of mode the sensor is in. Choices for accelerometer are "accelerometer_only", "gyroscope_only",
    #     #"gyroscope_DMP", "gyroscope_accelerometer", "gyroscope_accelerometer_DMP"

    #     #time_step would define at what intervals (and therefore time) the model
    #     # would return data at. A time_step o 1 second would have the model return
    #     # data at 0,1,2,3... seconds assuming start time of 0 seconds.
    #     #
    #     self.mode = mode
    #     self.time_step = time_step
    #     self.duration = duration

    #     self.low_power_wakeup = low_power_wakeup
    #     #In Hz, determines how fast the sensor wakes up when in low power mode. More wakeups means more power used.
    #     #Choices are 1.25, 5, 20, 40.
    #     self.sample_rate_divisor = sample_rate_divisor
    #     #Value between 0 and 255. Used as a divisor for sample rate equation, higher means slower sample rate meaning
    #     #presumably lower data collected per second.
    #     self.digital_low_pass = digital_low_pass
    #     #Digital low pass filter. Enabling this lowers the sampling rate by a factor of 8. See page 12 of the 
    #     #register map linked below. 
    #     self.loop_rate = loop_rate
    #     #how fast the arduino loop will run. This value is kind of up in the air, but we predict that it may have an
    #     #affect on how fast we can read from the sensors depending on how much code is run in the loop, in Hz.
    #     self.time = np.arange(0,self.duration,self.time_step)
    
    def __init__(self, **params):
        super(TP, self).__init__(**params)
        #All params configured in parent function!

    def checkParams(self, params):
        pass

    def runSim(self, mode):
        #active_times would be a list of tuples/list that would define the time at which the sensor was running
        # i.e. [[0,1],[4,5],[6,7]] would have the sensor running from time 0s to 1s,
        # 4s to 5s, 6s to 7s
        time = np.arange(0,self.duration,self.time_step) #time at which to collect data
        #active_vec: we are assuming that the accelerometer will constantly be on, since the slowest it will update is
        #once every 0.8 seconds.
        #power = self.getPowerUsage(mode, time)
        data = self.getDataAccumulated()

        return time, data

    def getModePower(self, mode):
        #Calculates power when sensor is active. This value is used in conjunction with
        self.mode = mode
        power_used = 0
        if(mode == "always_on"):
            TP_only_power_microamps = 15
        else:
            TP_only_power_microamps = 15
        voltage = 3.3
        if(mode == "TPOnly"):
            power_used = (TP_only_power_microamps * voltage) / 1000 #converted to milliamps.
        elif(mode[0:16] == "always_on"):
            pass
        else:
            print("Invalid mode entered.")
            return -1
        
        return power_used
        #returns a vector of when power is used. Units are in mW.

    def getPowerVector(self, active_times: List[tuple]) -> List:
        #active times is a list of tuples. First two elements are start and end times, third is 
        length = len(self.time)
        arr = [0] * length # creating corresponding power array to time intervals, default values 
        dataarr = [0] * length
        # check if the given start and end time is a valid value in the time array and round to nearest value 
        for times in active_times:
            start_index = int(times[0] / self.time_step) # getting index of the closest value to active times 
            end_index = int(times[1] / self.time_step)
            
            if start_index < 0 or end_index > len(self.time): 
                print("Error. Index not valid.")
                return -1
            
            for i in range(start_index, end_index):
                arr[i] = self.getModePower(times[2])
                if i == 0:
                    dataarr[i] = self.getBytesPerSecond(times[2])
                else:
                    dataarr[i] = dataarr[i-1] + self.getBytesPerSecond(times[2])
            
        return arr, dataarr
    
    def getDataAccumulated(self):
       
       
    def setSampleRate(self, samplerate):
        self.sample_rate_divisor = samplerate


    def getBytesPerSecond(self, mode):
        if(mode == "TPOnly" or mode[0:16] == "always_on"):
            return 6
        else:
            return 12



# f = plt.figure(figsize=(10,10))
# #print(dude)
# print(sensor.mode)
# ax1 = f.add_subplot(311)
# power_plot, = plt.plot(dude[0], dude[1])
# plt.tick_params('x', labelbottom=False)
# ax1.set_ylim([0, 50])
# ax1.set_ylabel('mW')

# ax2 = f.add_subplot(312, sharex=ax1)
# data_plot, = plt.plot(dude[0], dude[2])
# # make these tick labels invisible
# plt.tick_params('x', labelsize=6)
# ax2.set_ylim([0, 50000])
# ax2.set_ylabel('Bytes')
# ax2.set_xlabel('Seconds')

# def update_samplerate(val):
#     sensor.setSampleRate(val)
#     data_plot.set_ydata(sensor.getDataAccumulated())
#     f.canvas.draw_idle()

# axfreq = plt.axes([0.25, 0.1, 0.65, 0.03])
# freq_slider = Slider(
#     ax=axfreq,
#     label='Sample Rate Divisor',
#     valmin=1,
#     valmax=255,
#     valinit=0,
# )
# freq_slider.on_changed(update_samplerate)

# rax = plt.axes([0.05, 0.15, 0.3, 0.15])
# radio = RadioButtons(rax, ('Accelerometer only', 'Gyroscope only', 'Gyroscope and DMP', 'Gyroscope and accelerometer', 'Gyroscope, accelerometer, and DMP'))


# def hzfunc(label):
#     hzdict = {'Accelerometer only': sensor.getPowerUsage("accelerometer_only"), 'Gyroscope only': sensor.getPowerUsage("gyroscope_only"), 'Gyroscope and DMP': sensor.getPowerUsage("gyroscope_DMP"), 'Gyroscope and accelerometer': sensor.getPowerUsage("gyroscope_accelerometer"), 'Gyroscope, accelerometer, and DMP': sensor.getPowerUsage("gyroscope_accelerometer_DMP")}
#     ydata = hzdict[label]
#     power_plot.set_ydata(ydata)
#     plt.draw()
# radio.on_clicked(hzfunc)



# plt.show()



#np.join(getDataAccu(duration, params1), getDataAccu(duration, params2))
#setMode()

#REFACTORING:
#Generate mode: return a dictionary outlining the parameters of a mode. Doing this would make the parameters in the 
#constructor redundant.
#Have some function handle both the modes and times for each mode. Two corresponding arrays perhaps, like the vectors we have been using.
#Have a central sensor class, that handles these things plus some extra functionality. We can use inheritance to make each 
#individual sensor.


#mode = {"mode" : , "time step": , "duration": , "sample_rate_divisor": ,}
