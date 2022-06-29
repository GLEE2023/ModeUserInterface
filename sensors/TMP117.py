import numpy as np
import matplotlib.pyplot as plt
import random 
from plotAll import generateActiveList

class TMP117():
    def __init__(self, time_step, duration, activeTimeParams, loop_rate): 
        self.time_step = time_step
        self.duration = duration
        self.time = np.arange(0, duration, time_step) #time at which to collect data
        self.activeTimeParams = activeTimeParams
        self.loop_rate = loop_rate
        
    def errorCheck(self):
        possCCtimes = ['0.0155', '0.125', '0.25', '0.5', '1', '4', '8', '16']
        possOStimes = ['0.0155', '0.125', '0.5', '1']
        possAveraging = ['0', '8', '32', '64']
        possModes = ["OS", "CC"]
        
        # checking if time intervals overlap
        sortedActiveTimes = sorted(self.activeTimeParams, key = lambda x: x[0])
        for index in range(len(sortedActiveTimes)-1):
            if sortedActiveTimes[index+1][0] < sortedActiveTimes[index][1]: # interval overlaps
                print("ERROR: Overlapping intervals {} and {}.".format(sortedActiveTimes[index], sortedActiveTimes[index+1]))

        for params in self.activeTimeParams:
            start = params[0]
            end = params[1]

            x = params[2].split("_")
            mode = x[0]
            num_averages = x[1]
            convCycleTime = x[2]
    
            if mode not in possModes:
                print("Invalid Mode of {} in {}. Possible inputs: {}".format(mode, params, possModes))
            else:
                if mode == "CC" and convCycleTime not in possCCtimes:
                    print("Invalid CC conv cycle time of {} in {}. Possible inputs: {}".format(convCycleTime, params, possCCtimes))
                if mode == "OS" and convCycleTime not in possOStimes:
                    print("Invalid OS conv cycle time of {} in {}. Possible inputs: {}".format(convCycleTime, params, possOStimes))
                if num_averages not in possAveraging:
                    print("Invalid Averaging {} in {}. Possible inputs: {}".format(num_averages, params, possAveraging))

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

            params = times[2]
            x = params.split("_")
            mode = x[0]
            averages = x[1]
            convCycleTime = float(x[2])
            if self.loop_rate > convCycleTime:
                convCycleTime = self.loop_rate
            
            power = self.computePower(int(averages), float(convCycleTime), mode)
            for i in range(start_index, length):
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
            
            #splitting string to get params
            params = times[2]
            x = params.split("_")
            convCycleTime = float(x[2])
            if self.loop_rate > convCycleTime:
                convCycleTime = self.loop_rate
            

            #calculating data per step in active time period
            # convCycle = self.activeTimeParams[times][1]
            bits_per_second = bits_per_cycle /convCycleTime # bits per second
            activeTimeTotal = times[1]-times[0] # getting num of seconds of active period
            bits_total = bits_per_second * activeTimeTotal # total bits during that active period
            num_steps = end_index-start_index 
            bits_per_step = bits_total / num_steps
            
            for i in range(start_index, length):
                if i < end_index:
                    data_accumulated += bits_per_step
                    
                data_arr[i] = data_accumulated 
            
        return data_arr
    
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
        power_plot, = plt.plot(time_vector, power_vector)
        plt.tick_params('x', labelbottom=False)
        #power_value_limit = [0,0.1]
        #ax1.set_ylim(power_value_limit)
        ax1.set_ylabel('mW')

        ax2 = f.add_subplot(313, sharex=ax3)
        data_plot, = plt.plot(time_vector, data_vector)
        # make these tick labels invisible
        plt.tick_params('x', labelsize=12)
        #data_value_limit = [0,500]
        #ax2.set_ylim(data_value_limit)
        ax2.set_ylabel('Bytes')
        ax2.set_xlabel('Seconds')

        plt.show()
    
    def Simulation(self):
        self.errorCheck()
        power = self.getAllModesPower()
        data = self.getAllModesData()
        return np.array(power), np.array(data), np.array(self.time)
        #self.plotData(power, data, self.time, self.activeTimeParams)

        # activeList = generateActiveList(self.totalTimePeriod, self.modedict)
        # self.plotData(power, data, self.time, activeList)

time_step = 0.0155
activeTimeParams = [(0, 15, "OS_8_0.0155"), (5, 45, "CC_32_16"), (70, 75, "OS_64_1"), (75,100, "OS_8_0.0155")]
tmp = TMP117(time_step, 100, activeTimeParams, loop_rate = 20) # creating TMP117 class
tmp.Simulation()