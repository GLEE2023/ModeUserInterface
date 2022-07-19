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
    
    for index in range(len(params)):
        arr = params[index].split("_")
        mode = arr[0]
        averages = arr[1]
        convTime = arr[2]

        str = ""
        if mode == "OFF": 
            bitstring.append(int(possModes[mode],2))
        else:
            str += possModes[mode] + possTimes[convTime] + possAveraging[averages]
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
    bitstringArray = [bin(int(mode[0].split("_")[-2]))[2:] + format(int(mode[0].split("_")[-1]), '08b') + bitmodedict['_'.join(mode[0].split("_")[0:-2])] for mode in modelist]
    return [int(i, 2) for i in bitstringArray]

def generateBitsTP(paramList: list):
    bitmodedict = {"TP_only": "1","TP_off": "0"}

    paramList = np.array(paramList)
    params = paramList[:,0]

    return [int(bitmodedict[params[index]], 2) for index in range(len(params))]

def generateBitsBM1422(paramList: list):
    bitmodedict = {"1000":"11", "standby":"01", "10":"10", "off":"00"}
    bitstring = []
    paramList = np.array(paramList)
    params = paramList[:,0]

    return [int(bitmodedict[params[index]], 2) for index in range(len(params))]

def generateBitsCAP11NA(paramList: list):
    bitmodedict = {"on": "1","off": "0"}
    paramList = np.array(paramList)
    params = paramList[:,0]
    
    return [int(bitmodedict[params[index]], 2) for index in range(len(params))]

def generateAll(TMPparams, MPUparam, BMparams, TPparams, CAPparams):
    TMPint = generateBitsTMP117(TMPparams)
    ACCint= generateBitsMPU6050(MPUparams)
    THERMOint = generateBitsTP(TPparams)
    CAPint = generateBitsCAP11NA(CAPparams)
    MAGint = generateBitsBM1422(BMparams)

    #all_bitstrings = [TMPint, ACCint, THERMOint, CAPint, MAGint]
    #largest_list = (min(all_bitstrings, key=lambda k: -len(k))) # getting largest list in 2d list

    bit_lengths = {1:15, 2:1, 3:1, 4:2} # bitstring order: tmp, acc, thermopile, cap, mag
    all_configs = []
    for configurations in itertools.zip_longest(TMPint, ACCint, THERMOint, CAPint, MAGint): 
        #print(configurations)
        
        if configurations[0] == 0: 
            config_bitstring = 1 << 6
        else: config_bitstring = configurations[0]

        for index in range(1,len(configurations)):
            config_bitstring <<= bit_lengths[index] # shifting 
            if configurations[index] != None: # masking
                config_bitstring |= configurations[index]
        
        if configurations[0] == 0:
            config_bitstring &= 0b0111111111111111111111111


        all_configs.append(config_bitstring)
    for configurations in itertools.zip_longest(TMPint, ACCint, THERMOint, CAPint, MAGint): 
        for j in configurations:
            if j != None:
                print(bin(j))
            else: print("None")
        print("\n")

    return all_configs 

# CONFIGURATION 1:
mode1_duration = 100 #seconds
tmp_mode1 = "tmp mode"
acc_mode1 = "acc_mode"

TMPparams = [("CC_32_16", 15), ("OS_64_1", 15), ("OS_32_0.0155", 40), ("OFF_0_0", 10)]
MPUparams = np.array([("low_power_wakeup_1.25_1_255",50), ("gyroscope_accelerometer_0_75",40), ("accelerometer_only_0_90", 20), ("low_power_wakeup_1.25_1_255",50)])
BMparams = [("1000",10), ("standby",10), ("10",40)]
CAPparams = [("on",10), ("off",10)]
TPparams = [("TP_only",10), ("TP_off",10)]
res = generateAll(TMPparams, MPUparams, BMparams, TPparams, CAPparams)
