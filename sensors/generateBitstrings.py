import itertools
from re import L
import numpy as np

def generateBitsTMP117(modedict: dict) -> list: # TMP - 6 bits to encode 48 different configurations
    possCCtimes = {'0.0155': "000", '0.125': "001", '0.25': "010", '0.5': "011", '1': "100", '4': "101", '8': "110", '16': "111"}
    possOStimes = {'0.0155': "000", '0.125': "001", '0.5': "011", '1': "100"}
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

def generateBitsMPU6050(modelist: list) -> list:
    """
        modelist must be a numpy array. returns a list of integers representing the configuration bits.
    """
    
    bitmodedict = {
        "low_power_wakeup_1.25": "0000", "low_power_wakeup_5": "0001", "low_power_wakeup_20": "0010", 
        "low_power_wakeup_40": "0011", "accelerometer_only": "0100", "gyroscope_only": "0101",
        "gyroscope_DMP": "0110", "gyroscope_accelerometer": "0111", "gyroscope_accelerometer_DMP": "1000" 
    }
    #dont ask how this works.
    #bitstring is digital low pass (1 bit), then sample rate divisor (8 bits), then mode (4 bits), then duration (7 bits) - 20 bits in total
    bitstringArray = [bin(int(mode[0].split("_")[-2]))[2:] + format(int(mode[0].split("_")[-1]), '08b') + bitmodedict['_'.join(mode[0].split("_")[0:-2])] + format(int(mode[1]), '07b') for mode in modelist]
    return [int(i, 2) for i in bitstringArray]

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

#TMPint, MPUint = generateAll(TMPparams, MPUparams)
#print(TMPint)

modedict = np.array([("low_power_wakeup_1.25_1_255",50), ("gyroscope_accelerometer_0_75",40), ("accelerometer_only_0_90", 20), ("low_power_wakeup_1.25_1_255",50)])


print(generateBitsMPU6050(modedict))