import itertools
from re import L
import numpy as np

def generateBitsTMP117(modedict: dict) -> list: # TMP - 6 bits to encode 48 different configurations
    possCCtimes = {'0.0155': 0b000, '0.125': 0b001, '0.25': 0b010, '0.5': 0b011, '1': 0b100, '4': 0b101, '8': 0b110, '16': 0b111}
    possOStimes = {'0.0155': 0b000, '0.125': 0b001, '0.5': 0b011, '1': 0b100}
    possAveraging = {'0': 0b00, '8': 0b01, '32': 0b10, '64': 0b11}
    possModes = {"OS": 0b0, "CC": 0b1 }

    # error check
    allBitstrings = {}
    for config in modedict:
        arr = config.split("_")
        mode = arr[0]
        averages = arr[1]
        convTime = arr[2]

        bitstring = []
        i = 0
        if mode == "CC":
            i += possModes[mode] + possCCtimes[convTime]+ possAveraging[averages]
            print(i)
            bitstring.append(i)
            print(bitstring)
            # s = [possModes[mode], possCCtimes[convTime],possAveraging[averages]]
            # bitstring.append(s)
            # bitstring.append(possModes[mode])
            # bitstring.append(possCCtimes[convTime])
            # bitstring.append(possAveraging[averages])
        elif mode == "OS":
            i += possModes[mode] + possCCtimes[convTime]+ possAveraging[averages]
            bitstring.append(i)
            # s = [possModes[mode], possCCtimes[convTime],possAveraging[averages]]
            # bitstring.append(s)
            # bitstring.append(possModes[mode])
            # bitstring.append(possOStimes[convTime])
            # bitstring.append(possAveraging[averages])
        elif mode == "OFF": 
            bitstring.append(0b0)
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

def generateAll(TMPparams, MPUparams):
    TMPbitstring= generateBitsTMP117(TMPparams)
    MPUbitstring= generateBitsMPU6050(MPUparams)

    return TMPbitstring, MPUbitstring

TMPparams = {"CC_32_16":15, "OS_64_1":15, "OS_32_0.0155":40, "OFF_0_0": 10} 
MPUparams = {"low_power_wakeup_1.25_1_255":50, "gyroscope_accelerometer_0_75":40, "accelerometer_only_0_90": 20}

TMPbitstring, MPUbitstring = generateAll(TMPparams, MPUparams)
print(TMPbitstring)
