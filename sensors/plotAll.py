import matplotlib.pyplot as plt
import numpy as np

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

