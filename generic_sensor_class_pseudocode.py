class genericSensor():


    def __init__ (self, mode, time_step, duration, parameter1_related_to_mode, parameter2_related_to_mode,on_and_on):
        #mode tells the type of mode the sensor is in (i.e. for temp sensor, one
        # shot, continuous conversion)
        #time_step would define at what intervals (and therefore time) the model
        # would return data at. A time_step o 1 second would have the model return
        # data at 0,1,2,3... seconds assuming start time of 0 seconds.
        #
        self.mode = mode
        self.time_step = time_step
        self.duration = duration

        self.param1= parameter1_related_to_mode #have as many variables as needed
        self.param2= parameter2_related_to_mode #have as many variables as needed


    def runSim(self, active_times):
        #active_times would be a list of tuples/list that would define the time at which the sensor was running
        # i.e. [[0,1],[4,5],[6,7]] would have the sensor running from time 0s to 1s,
        # 4s to 5s, 6s to 7s
        time = np.arrange([0,self.duration],self.time_step) #time at which to collect data
        active_vec = #get vector of when sensor is active
        power = getPowerUsage(time,mode,parameters_related_to_mode)
        data = getDataUsage(time,mode,parameters_related_to_mode)

        return time, power, data

    def getPowerUsage(self,time,mode,parameters_related_to_mode):
        #calc avg_power

        return power_usage

    def getDataAccumulated(self,time,mode,parameters_related_to_mode):

        return data_accumulated
