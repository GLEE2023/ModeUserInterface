import matplotlib.pyplot as plt
import numpy as np
import difflib

def generateActiveList(total_time: float, modelist:list) -> list:
    """
        Returns list similar to the form of active_times, but based off of modedict.
        active_times: [(int(start1), int(end1), "mode1"), (int(start2), int(end2), "mode2")]
        
        Example:
            modes = {"low_power_wakeup_5": 10, "accelerometer_only": 20, "gyroscope_accelerometer_DMP":30}
            #low_power_wakeup_5 for 10 seconds, accelerometer_only for 20 seconds, and so on.
            #10 + 20 + 30 = 60, so the period for this configuration is 60 seconds.


            active_times_list = generateActiveList(total_time = 600, modedict = modes)
            #for 600 seconds, repeat the configuration set in modedict.
        

        args:
            total_time (float): total active time of the sensor, ie 10 seconds or 10 hours.
            modelist (list): numpy array describing scheduling period based off of modedict. See example.
            modedict form: {string(mode1):int(duration1), string(mode2):int(duration2), ...}

        returns:
            finalArr, list of active times of each mode
        """
    #modedict has different modes and times that add up to a single cycle.
    #for accelerometer:
    #modedict = {"gyroscope_accelerometer_DMP":15, "accelerometer_only":15,"low_power_wakeup_5":40}
    #total period is 70 seconds (15+15+40)
    keys = modelist[:,0]
    finalArr = []
    curTime = 0
    flag = False
    while curTime < total_time:
        #for val in values:
        for item in modelist:
            modeDuration = int(item[1])
            if curTime+modeDuration>total_time:
                flag = True
                break
            finalArr.append((curTime, curTime+modeDuration, item[0]))
            curTime += modeDuration
        if flag: 
            break
    mode = len(finalArr) % len(modelist)
    if finalArr[-1][1] > total_time:
        finalArr[-1] = (finalArr[-1][0], total_time, keys[mode])
    elif finalArr[-1][1] < total_time:
        finalArr.append((finalArr[-1][1], total_time, keys[mode]))
    return finalArr
    #finalArr is a list of tuples in the form (start, stop, mode): [(start,stop, mode), ...]

def plotTogether(time_tmp, time_acc, tp_time, cap_time, mag_time, tp_power, power_tmp, power_acc, mag_power, cap_power, data_tmp, data_acc, mag_data, cap_data, tp_data, total_pow, total_data, chip_pow): 
    plt.figure(figsize=(15, 7))

    plt.plot(time_tmp, power_tmp, label = "Power Temp Sensor")
    plt.plot(time_acc, power_acc, label = "Accelerometer Sensor")
    plt.plot(mag_time, mag_power, label = "Magnetometer Sensor")
    plt.plot(cap_time, cap_power, label = "Capacitive Sensor")
    plt.plot(tp_time, tp_power, label = "Thermopile Sensor")
    #atmega power
    plt.plot([0,mag_time[-1]],[chip_pow,chip_pow], label = "ATMega328P")

    plt.plot(mag_time, total_pow, label = "total pow")

    #plt.plot(time_thermo, power_thermo)
    plt.grid(visible=True)

    plt.xlabel("Time",fontsize=16)
    plt.ylabel("Power",fontsize=16)
    plt.title("Power vs Time All Sensors",fontsize=20)
    plt.legend()

    plt.figure(figsize=(15,7))
    plt.plot(time_tmp, data_tmp, label = "Power Temp Sensor")
    plt.plot(time_acc, data_acc, label = "Accelerometer Sensor")
    plt.plot(mag_time, mag_data, label = "Magnetometer Sensor")
    plt.plot(cap_time, cap_data, label = "Capacitive Sensor")
    plt.plot(tp_time, tp_data, label = "Thermopile Sensor")
    plt.plot(mag_time, total_data, label = "total data")

    plt.grid(visible=True)
    plt.xlabel("Time",fontsize=16)
    plt.ylabel("Data",fontsize=16)
    plt.title("Data vs Time All Sensors",fontsize=16)
    plt.legend();

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
        plt.grid(visible=True)
        power_plot, = plt.plot(time_vector, power_vector)
        plt.tick_params('x', labelbottom=False)
        #power_value_limit = [0,0.1]
        #ax1.set_ylim(power_value_limit)
        ax1.set_ylabel('Power (mW)')

        ax2 = f.add_subplot(313, sharex=ax3)
        plt.tick_params('x', labelsize=12)
        data_plot, = plt.plot(time_vector, data_vector)
        # make these tick labels invisible
        plt.tick_params('x', labelsize=12)
        #data_value_limit = [0,500]
        #ax2.set_ylim(data_value_limit)
        ax2.set_ylabel('Data (Bytes)')
        ax2.set_xlabel('Seconds')
        plt.show()

def allConfigsTMP():
        possCCtimes = ['0.0155', '0.125', '0.25', '0.5', '1', '4', '8', '16']
        possOStimes = ['0.0155', '0.125', '0.5', '1']
        possAveraging = ['0', '8', '32', '64']

        CC_Configs = ["CC_"+av+"_"+time for time in possCCtimes for av in possAveraging]
        OS_Configs = ["OS_"+av+"_"+time for time in possOStimes for av in possAveraging]
        AllConfigs = CC_Configs + OS_Configs + ["OFF_0_0"]

        return AllConfigs

def validateInputs(configurations):
    configurations = np.array(configurations)
    # tmp_modes = configurations[:,0]
    # acc_modes = configurations[:,1]
    # thermopile_modes = configurations[:,2]
    # cap_modes = configurations[:,3]
    # mag_modes = configurations[:,4]

    allConfigsTemp = allConfigsTMP()
    #allConfigsAcc = []
    allConfigsThermo = ["TP_only", "TP_off"]
    allConfigsCap = ["on", "off"]
    allConfigsMag = ["1000", "standby", "10", "off"]

    # for mode in tmp_modes:
    #     if mode not in allConfigsTemp:
    #         print("Not a valid mode. Did you mean: {}".format(difflib.get_close_matches(mode, allConfigsTMP)))

    # # for mode in acc_modes:
    # #         print("Not a valid mode. Did you mean: {}".format(difflib.get_close_matches(mode, allConfigsAcc)))
    
    # for mode in thermopile_modes:
    #     if mode not in allConfigsThermo:
    #         print("Not a valid mode. Did you mean: {}".format(difflib.get_close_matches(mode, allConfigsTMP)))

    # for mode in cap_modes:
    #     if mode not in allConfigsCap:
    #         print("Not a valid mode. Did you mean:")

    # for mode in mag_modes:
    #     if mode not in allConfigsMag:
    #         print("Not a valid mode. Did you mean:")

# # CONFIGURATION 1:
# mode_duration_1 = 10 # seconds
# tmp_mode_1 = "C_32_16"
# acc_mode_1 = "low_power_wakeup_1.25_1_255"
# thermopile_mode_1 = "TP_only"
# capacitor_mode_1 = "off"
# magnetometer_mode_1 = "standby"
# config_1 = [tmp_mode_1, acc_mode_1, thermopile_mode_1, capacitor_mode_1, magnetometer_mode_1, mode_duration_1]

# # CONFIGURATION 2:
# mode_duration_2 = 10 # seconds
# tmp_mode2 = "CC_32_16"
# acc_mode2 = "accelerometer_only_0_90"
# thermopile_mode2 = "TP_off"
# capacitor_mode2 = "on"
# magnetometer_mode2 = "1000"
# config_2 = [tmp_mode2, acc_mode2, thermopile_mode2, capacitor_mode2, magnetometer_mode2, mode_duration_2]

# # CONFIGURATION 3:
# mode_duration_3 = 10 # seconds
# tmp_mode_3 = "CC_32_16"
# acc_mode_3 = "accelerometer_only_0_90"
# thermopile_mode_3 = "TP_off"
# capacitor_mode_3 = "on"
# magnetometer_mode_3 = "1000"
# config_3 = [tmp_mode_3, acc_mode_3, thermopile_mode_3, capacitor_mode_3, magnetometer_mode_3, mode_duration_3]

# # ADD CONFIGURATION ARRAYS HERE  
# configurations = [config_1, config_2, config_3]

# validateInputs(configurations)