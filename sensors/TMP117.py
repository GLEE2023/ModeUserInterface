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
        """
            This function checks for valid inputs and prints out a statement displaying the given inputs if invalid. 
            It also checks if time intervals overlap with each other and will display to the user if invalid.
            It will also print the list of valid possible inputs for the user to choose from.

            Args: none
            Returns: none
        """

        possCCtimes = ['0.0155', '0.125', '0.25', '0.5', '1', '4', '8', '16']
        possOStimes = ['0.0155', '0.125', '0.5', '1']
        possAveraging = ['0', '8', '32', '64']
        possModes = ["OS", "CC", "OFF"]


        # checking if time intervals overlap
        sortedActiveTimes = sorted(self.activeTimeParams, key = lambda x: x[0])
        for index in range(len(sortedActiveTimes)-1):
            if sortedActiveTimes[index+1][0] < sortedActiveTimes[index][1]: # interval overlaps
                print("ERROR: Overlapping intervals {} and {}.".format(sortedActiveTimes[index], sortedActiveTimes[index+1]))

        for params in self.activeTimeParams:
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
        """
            This function will compute the average power for CC and OS mode in TMP117. It will return a floating point number.

            Args: 
                num_averages (string)
                convCycleTime (string)
                mode (string)
                * num_averages and convCycleTime are taken as strings but will be converted to int/float during conversion

            Returns: power (float)
        """

        activeCurrentConsumption = 135 # micro amps
        activeConversionTime = num_averages*0.0155

        standByCurrentConsumption = 1.25 # micro amps
        standbyTime = convCycleTime - activeConversionTime
        
        SDcurrent = 250/ 1000000 # micro amps
        current = 0
        if mode == "CC":
            current = ((activeCurrentConsumption*activeConversionTime)+(standByCurrentConsumption*standbyTime))/convCycleTime

        elif mode == "OS":
            current = ((activeCurrentConsumption*activeConversionTime)+(SDcurrent*standbyTime))/convCycleTime
        
        elif mode == "OFF":
            current = 0

        power = (current * 3.3)/1000 # milli watts
        
        return power
    
    def getAllModesPower(self):
        """
            This function computes and returns an array that contains the power at every index corresponding to active times.

            Args: none

            Returns: power_arr (array)
        """
 
        length = len(self.time)
        power_arr = [0] * length # creating corresponding power array to time intervals, default values

        for times in self.activeTimeParams: # check if the given start and end time is a valid value in the time array and round to nearest value 
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
            for i in range(start_index, end_index):
                power_arr[i] = power

        return power_arr
            
    def getAllModesData(self):
        """
            This function computes an array that contains the data at every index corresponding to active times.
            Since a 16-bit value is stored at the end of each conversion cycle, this data is accumulated over the active time 
            and then stored during the non-active time in this model. This function only computes the average data- it calculates the data per step in each active time period.

            Args: none

            Returns: data_arr (array)
        """
        
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
        """
            This function will take in the power, data, time, and active_times array in order to plot all the data for all the modes 
            on 3 separate sub-plots. The first sub-plot will display which modes for the TMP sensor are active. The second sub-plot
            displays power(mW) vs time(s) and the last sub-plot displays data(Bytes) vs time(s). 

            Args: 
                power_vector (array)
                data_vector (array)
                time_vector (array)
                active_times (array of tuples containing start, end, and mode params)

            Returns: none
        """
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
        ax1.set_ylabel('Average Power (mW)')

        ax2 = f.add_subplot(313, sharex=ax3)
        data_plot, = plt.plot(time_vector, data_vector)
        # make these tick labels invisible
        plt.tick_params('x', labelsize=12)
        #data_value_limit = [0,500]
        #ax2.set_ylim(data_value_limit)
        ax2.set_ylabel('Average Data (Bytes)')
        ax2.set_xlabel('Seconds')

        plt.show()
    
    def runSim(self, plot):
        """
            This function will call the errorCheck(), getAllModesPower(), getAllModesData() functions. It first checks if the params
            for this sensor are valid and then calls the functions to get the power and data info.

            Args: none

            Returns: 
                power (numpy array)
                data (numpy array)
                time (numpy array)
        """
        
        self.errorCheck()
        power = self.getAllModesPower()
        data = self.getAllModesData()
        if plot == True: 
            self.plotData(power, data, self.time, self.activeTimeParams)

        return np.array(power), np.array(data), np.array(self.time)

# time_step = 0.0155
# activeTimeParams = [(0, 15, "OS_8_0.0155"), (5, 45, "CC_32_16"), (70, 75, "OS_64_1"), (75,100, "OS_8_0.0155")]
# tmp = TMP117(time_step, 100, activeTimeParams, loop_rate = 20) # creating TMP117 class
# tmp.runSim(plot=True)