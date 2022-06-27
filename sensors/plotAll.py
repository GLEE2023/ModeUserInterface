def generateActiveList(total_time: float, modedict:dict, **kwargs) -> list:
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

def plotAll():
    