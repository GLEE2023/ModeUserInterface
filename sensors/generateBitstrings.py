import itertools
from re import L
import numpy as np

def generateBitsTMP117(modedict: dict) -> list: # TMP - 6 bits to encode 48 different configurations
    possTimes = {'0.0155': "000", '0.125': "001", '0.25': "010", '0.5': "011", '1': "100", '4': "101", '8': "110", '16': "111"}
    possAveraging = {'0': "00", '8': "01", '32': "10", '64': "11"}
    possModes = {"OS": "10", "CC": "11", "OFF": "000000"}

    # error check
    bitstring = []

    for config in modedict:
        arr = config.split("_")
        mode = arr[0]
        averages = arr[1]
        convTime = arr[2]

        str = ""
        if mode == "OFF": 
            bitstring.append(int(possModes[mode],2))
        else:
            str += possModes[mode] + possTimes[convTime]+ possAveraging[averages]
            bitstring.append(int(str,2))

    return bitstring

def generateBitsMPU6050(modedict: dict) -> list:
    bitstring = []
    bitmodedict = {
        "low_power_wakeup_1.25": "0000", "low_power_wakeup_5": "0001", "low_power_wakeup_20": "0010", 
        "low_power_wakeup_40": "0011", "accelerometer_only": "0100", "gyroscope_only": "0101",
        "gyroscope_DMP": "0110", "gyroscope_accelerometer": "0111", "gyroscope_accelerometer_DMP": "1000" 
    }
    
    for mode in modedict.keys():
        temparray = []
        split_mode = mode.split("_")
        temparray.append(int(split_mode[-2]))
        temparray.append(int(split_mode[-1]))
        temparray.append(bitmodedict['_'.join(split_mode[0:-2])])
        bitstring.append(temparray)

    return bitstring

def generateBitsTP(modedict: dict) -> list:
    bitmodedict = {"TP_only": "1","TP_off": "0"}
    return [int(bitmodedict[mode], 2) for mode in modedict.keys()]

def generateBitsBM1422(modedict: dict) -> list:
    bitmodedict = {"1000":"11", "standby":"01", "10":"10", "off":"00"}
    return [int(bitmodedict[mode], 2) for mode in modedict.keys()]

def generateBitsCAP11NA(modedict: dict) -> list:
    bitmodedict = {"on": "1","off": "0"}
    return [int(bitmodedict[mode], 2) for mode in modedict.keys()]

def generateAll(TMPparams, MPUparam, BMparams, TPparams, CAPparams):
    TMPint = generateBitsTMP117(TMPparams)
    
    #MPUbitstring= generateBitsMPU6050(MPUparams)
    MPUint = generateBitsMPU6050(MPUparam)
    #ACCint = convertToInt()
    THERMOint = generateBitsTP(TPparams)
    CAPint = generateBitsCAP11NA(CAPparams)
    MAGint = generateBitsBM1422(BMparams)

    return TMPint, THERMOint, CAPint, MAGint

# bitstring order: tmp, acc, thermopile, cap, mag

TMPparams = {"CC_32_16":15, "OS_64_1":15, "OS_32_0.0155":40, "OFF_0_0": 10} 
MPUparams = {"low_power_wakeup_1.25_1_255":50, "gyroscope_accelerometer_0_75":40, "accelerometer_only_0_90": 20}
BMparams = {"1000":10, "standby":10,"10":40}
CAPparams = {"on":10, "off":10}
TPparams = {"TP_only":10, "TP_off":10}
TMPint, THERMOint, CAPint, MAGint = generateAll(TMPparams, MPUparams, BMparams, TPparams, CAPparams)
print(TMPint, THERMOint, CAPint, MAGint)
