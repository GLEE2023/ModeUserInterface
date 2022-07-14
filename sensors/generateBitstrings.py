import numpy as np
import itertools 

def generateBitsTMP117(paramList): # TMP - 6 bits to encode 48 different configurations
    possTimes = {'0.0155': "000", '0.125': "001", '0.25': "010", '0.5': "011", '1': "100", '4': "101", '8': "110", '16': "111"}
    possAveraging = {'0': "00", '8': "01", '32': "10", '64': "11"}
    possModes = {"OS": "10", "CC": "11", "OFF": "000000"}

    # error check
    bitstring = []
    paramList = np.array(paramList)
    params = paramList[:,0]
    durations = [int(duration) for duration in paramList[:,1]]
    bit_durations = [format(duration,'07b') for duration in durations] # getting duration in 7 bit string format
    
    for index in range(len(params)):
        arr = params[index].split("_")
        mode = arr[0]
        averages = arr[1]
        convTime = arr[2]

        str = ""
        if mode == "OFF": 
            bitstring.append(int(possModes[mode] + bit_durations[index],2))
        else:
            str += possModes[mode] + possTimes[convTime] + possAveraging[averages] + bit_durations[index]
            bitstring.append(int(str,2))
    return bitstring

def generateBitsMPU6050(modelist: list) -> list:
    """
        modelist must be a numpy array. returns a list of integers representing the configuration bits.
    """
    
    bitmodedict = {
        "Off":"0000","low_power_wakeup_1.25": "0001", "low_power_wakeup_5": "0010", "low_power_wakeup_20": "0011", 
        "low_power_wakeup_40": "0100", "accelerometer_only": "0101", "gyroscope_only": "0110",
        "gyroscope_DMP": "0111", "gyroscope_accelerometer": "1000", "gyroscope_accelerometer_DMP": "1001" 
    }
    #dont ask how this works.
    #bitstring is digital low pass (3 bit), then sample rate divisor (8 bits), then mode (4 bits), then duration (7 bits) - 22 bits in total
    bitstringArray = [bin(int(mode[0].split("_")[-2]))[2:] + format(int(mode[0].split("_")[-1]), '08b') + bitmodedict['_'.join(mode[0].split("_")[0:-2])] + format(int(mode[1]), '07b') for mode in modelist]
    return [int(i, 2) for i in bitstringArray]

def generateBitsTP(paramList: list):
    bitmodedict = {"TP_only": "1","TP_off": "0"}

    bitstring = []
    paramList = np.array(paramList)
    params = paramList[:,0]
    durations = [int(duration) for duration in paramList[:,1]]
    bit_durations = [format(duration,'07b') for duration in durations] # getting duration in 7 bit string format

    return [int(bitmodedict[params[index]] + bit_durations[index], 2) for index in range(len(params))]

def generateBitsBM1422(paramList: list):
    bitmodedict = {"1000":"11", "standby":"01", "10":"10", "off":"00"}
    bitstring = []
    paramList = np.array(paramList)
    params = paramList[:,0]
    durations = [int(duration) for duration in paramList[:,1]]
    bit_durations = [format(duration,'07b') for duration in durations] # getting duration in 7 bit string format

    return [int(bitmodedict[params[index]] + bit_durations[index], 2) for index in range(len(params))]

def generateBitsCAP11NA(paramList: list):
    bitmodedict = {"on": "1","off": "0"}
    bitstring = []
    paramList = np.array(paramList)
    params = paramList[:,0]
    durations = [int(duration) for duration in paramList[:,1]]
    bit_durations = [format(duration,'07b') for duration in durations] # getting duration in 7 bit string format

    return [int(bitmodedict[params[index]] + bit_durations[index], 2) for index in range(len(params))]

def generateAll(TMPparams, MPUparam, BMparams, TPparams, CAPparams):
    TMPint = generateBitsTMP117(TMPparams)
    ACCint= generateBitsMPU6050(MPUparams)
    THERMOint = generateBitsTP(TPparams)
    CAPint = generateBitsCAP11NA(CAPparams)
    MAGint = generateBitsBM1422(BMparams)

    #all_bitstrings = [TMPint, ACCint, THERMOint, CAPint, MAGint]
    #largest_list = (min(all_bitstrings, key=lambda k: -len(k))) # getting largest list in 2d list

    bit_lengths = {0:6, 1:12, 2:1, 3:1, 4:2} # bitstring order: tmp 13, acc 22, thermopile 8, cap 8, mag 9
    for configurations in itertools.zip_longest(TMPint, ACCint, THERMOint, CAPint, MAGint): 
        config_bitstring = configurations[0] << 22 # tmp is the first configuration
        for index, sensor in configurations:
            if index == 0:
                # don't do anything, tmp doesn't need to be masked
            elif index == 1:
            elif index == 2:
            elif index == 3:
            elif index == 4:
            
    # for int in largest_list:
    #     int << 13

    return 

# CONFIGURATION 1:
mode1_duration = 100 #seconds
tmp_mode1 = "tmp mode"
acc_mode1 = "acc_mode"

TMPparams = [("CC_32_16", 15), ("OS_64_1", 15), ("OS_32_0.0155", 40), ("OFF_0_0", 10)]
MPUparams = [("low_power_wakeup_1.25_1_255",50), ("gyroscope_accelerometer_0_75",40), ("accelerometer_only_0_90", 20)]
BMparams = [("1000",10), ("standby",10), ("10",40)]
CAPparams = [("on",10), ("off",10)]
TPparams = [("TP_only",10), ("TP_off",10)]
res = generateAll(TMPparams, MPUparams, BMparams, TPparams, CAPparams)
