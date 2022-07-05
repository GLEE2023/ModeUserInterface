def generateActiveList(total_time: float, modedict:dict) -> list:
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
            modedict (dict): dictionary describing scheduling period based off of modedict. See example.
            modedict form: {string(mode1):int(duration1), string(mode2):int(duration2), ...}

        returns:
            finalArr, list of active times of each mode
        """
    #modedict has different modes and times that add up to a single cycle.
    #for accelerometer:
    #modedict = {"gyroscope_accelerometer_DMP":15, "accelerometer_only":15,"low_power_wakeup_5":40}
    #total period is 70 seconds (15+15+40)
    finalArr = []
    curTime = 0
    flag = False
    while curTime < total_time:
        for key in modedict:
            if curTime+modedict[key]>total_time:
                flag = True
                break
            finalArr.append((curTime, curTime+modedict[key], key))
            curTime += modedict[key]
        if flag: 
            break
    mode = len(finalArr) % len(modedict)
    if finalArr[-1][1] > total_time:
        finalArr[-1] = (finalArr[-1][0], total_time, list(modedict.keys())[mode])
    elif finalArr[-1][1] < total_time:
        finalArr.append((finalArr[-1][1], total_time, list(modedict.keys())[mode]))
    return finalArr
    #finalArr is a list of tuples in the form (start, stop, mode): [(start,stop, mode), ...]