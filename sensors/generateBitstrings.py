import itertools
from re import L
import numpy as np

def generateBitsTMP117(modedict: dict) -> list: # TMP - 6 bits to encode 48 different configurations
    possCCtimes = {'0.0155': "000", '0.125': "001", '0.25': "010", '0.5': "011", '1': "100", '4': "101", '8': "110", '16': "111"}
    possOStimes = {'0.0155': "000", '0.125': "001", '0.5': "011", '1': "100"}
    possAveraging = {'0': "00", '8': "01", '32': "10", '64': "11"}
    possModes = {"OS": "10", "CC": "11", "OFF": "000000" }

    # error check
    bitstring = []

    for config in modedict:
        arr = config.split("_")
        mode = arr[0]
        averages = arr[1]
        convTime = arr[2]

        str = ""
        if mode == "CC":

            print()
            str += possModes[mode] + possCCtimes[convTime]+ possAveraging[averages]
            bitstring.append(str)
            # s = [possModes[mode], possCCtimes[convTime],possAveraging[averages]]
            # bitstring.append(s)
            # bitstring.append(possModes[mode])
            # bitstring.append(possCCtimes[convTime])
            # bitstring.append(possAveraging[averages])
        elif mode == "OS":
            str += possModes[mode] + possCCtimes[convTime]+ possAveraging[averages]
            bitstring.append(str)
            # s = [possModes[mode], possCCtimes[convTime],possAveraging[averages]]
            # bitstring.append(s)
            # bitstring.append(possModes[mode])
            # bitstring.append(possOStimes[convTime])
            # bitstring.append(possAveraging[averages])
        elif mode == "OFF": 
            bitstring.append(possModes[mode])
            # bitstring.append(0b0)

    return bitstring

def generateBitsMPU6050(modedict: dict) -> list:
    
    bitstring = []
    bitmodedict = {
        "low_power_wakeup_1.25":0b0000, "low_power_wakeup_5":0b0001, "low_power_wakeup_20":0b0010, 
        "low_power_wakeup_40":0b0011, "accelerometer_only":0b0100, "gyroscope_only":0b0101,
        "gyroscope_DMP":0b0110, "gyroscope_accelerometer":0b0111, "gyroscope_accelerometer_DMP":0b1000
    }
    
    for mode in modedict.keys():
        temparray = []
        split_mode = mode.split("_")
        temparray.append(int(split_mode[-2]))
        temparray.append(int(split_mode[-1]))
        temparray.append(bitmodedict['_'.join(split_mode[0:-2])])
        bitstring.append(temparray)

    return bitstring

def convertToInt(string):
    return [int(str, 2) for str in string]

def generateAll(TMPparams, MPUparams):
    TMPbitstring= generateBitsTMP117(TMPparams)
    MPUbitstring= generateBitsMPU6050(MPUparams)

    TMPint = convertToInt(TMPbitstring)
    # MPUint = convertToInt(MPUbitstring)
    # ACCint = convertToInt()
    # THERMOint = convertToInt()
    # CAPint = convertToInt()
    # magint = convertToInt()

    return TMPint, MPUint

# bitstring order: tmp, acc, thermopile, cap, mag

TMPparams = {"CC_32_16":15, "OS_64_1":15, "OS_32_0.0155":40, "OFF_0_0": 10} 
MPUparams = {"low_power_wakeup_1.25_1_255":50, "gyroscope_accelerometer_0_75":40, "accelerometer_only_0_90": 20}

TMPint, MPUint = generateAll(TMPparams, MPUparams)
print(TMPint)
