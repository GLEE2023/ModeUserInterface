def generateBitsTMP117(mode): # TMP - 6 bits to encode 48 different configurations
    possTimes = {'0.0155': "000", '0.125': "001", '0.25': "010", '0.5': "011", '1': "100", '4': "101", '8': "110", '16': "111"}
    possAveraging = {'0': "00", '8': "01", '32': "10", '64': "11"}
    possModes = {"OS": "10", "CC": "11", "OFF": "000000"}

    # "OS_8_0" : 1001000, mode, conv bits, averaging

    # do error check

    arr = mode.split("_")
    mode = arr[0]
    averages = arr[1]
    convTime = arr[2]

    if mode == "OFF": 
        return int(possModes[mode],2)
    else:
        return int(possModes[mode] + possTimes[convTime] + possAveraging[averages], 2)

def generateBitsMPU6050(mode):
    """
        modelist must be a numpy array. returns a list of integers representing the configuration bits.
    """
    bitmodedict = {
        "Off":"0000","low_power_wakeup_1.25": "0001", "low_power_wakeup_5": "0010", "low_power_wakeup_20": "0011", 
        "low_power_wakeup_40": "0100", "accelerometer_only": "0101", "gyroscope_only": "0110",
        "gyroscope_DMP": "0111", "gyroscope_accelerometer": "1000", "gyroscope_accelerometer_DMP": "1001" 
    }
    #dont ask how this works.
    #bitstring is digital low pass (3 bit), then sample rate divisor (8 bits), then mode (4 bits) - 15 bits
    bitstring = bin(int(mode.split("_")[-2]))[2:] + format(int(mode.split("_")[-1]), '08b') + bitmodedict['_'.join(mode.split("_")[0:-2])] 
    return int(bitstring, 2)

def generateBitsTP(mode):
    bitmodedict = {"TP_only": "1","TP_off": "0"}
    return int(bitmodedict[mode], 2)

def generateBitsBM1422(mode):
    bitmodedict = {"1000":"11", "standby":"01", "10":"10", "off":"00"}
    return int(bitmodedict[mode], 2)

def generateBitsCAP11NA(mode):
    bitmodedict = {"on": "1","off": "0"}
    return int(bitmodedict[mode], 2)

def generateAllBitstrings(allConfigs): # takes in a 2d array
    configurationsInt = []
    for config in allConfigs:
        TMPint = generateBitsTMP117(config[0])
        ACCint= generateBitsMPU6050(config[1])
        THERMOint = generateBitsTP(config[2])
        CAPint = generateBitsCAP11NA(config[3])
        MAGint = generateBitsBM1422(config[4])
        configurationsInt.append([TMPint, ACCint, THERMOint, CAPint, MAGint, config[5]])

    bit_lengths = {1:15, 2:1, 3:1, 4:2} # bitstring order: tmp, acc, thermopile, cap, mag
    allConfigsFullBitstrings = []
    for bits in configurationsInt:
        config_bitstring = 1 << 7 # need 1 as the MSB to keep the leading zeroes
        config_bitstring |= bits[0] # masking to get tmp bits

        for index in range(1,len(bits)-1):
            config_bitstring <<= bit_lengths[index] # shifting
            if bits[index] != None: # masking
                config_bitstring |= bits[index]

        duration = bits[5]
        allConfigsFullBitstrings.append((config_bitstring, duration))
        
    return allConfigsFullBitstrings

def ArduinoConfig(allConfigs, team_name):
    file_name = team_name + '.txt'
    f = open(file_name, 'w+')  # create file if doesn't exists otherwise open in overwrite mode
    allBitstrings = generateAllBitstrings(allConfigs)
    for index, config in enumerate(allBitstrings):
        bitstring = config[0]
        duration = config[1]
        f.write("#DEFINE MODE_" + str(index) + " " + str(bitstring) + "\n")
        f.write("#DEFINE DURATION_" + str(index) + " " + str(duration)+ "\n\n")
    f.close()

def readArduinoConfigs(team_name):
    file_name = team_name + '.txt'
    f = open(file_name, 'r') 
    print(f.read())

# # CONFIGURATION 1:
# mode1_duration = 10 # seconds
# tmp_mode1 = "C_32_16"
# acc_mode1 = "low_power_wakeup_1.25_1_255"
# thermopile_mode1 = "TP_only"
# capacitor_mode1 = "off"
# magnetometer_mode1 = "standby"
# config1 = [tmp_mode1, acc_mode1, thermopile_mode1, capacitor_mode1, magnetometer_mode1, mode1_duration]

# # CONFIGURATION 2:
# mode2_duration = 10 # seconds
# tmp_mode2 = "CC_32_16"
# acc_mode2 = "accelerometer_only_0_90"
# thermopile_mode2 = "TP_off"
# capacitor_mode2 = "on"
# magnetometer_mode2 = "1000"
# config2 = [tmp_mode2, acc_mode2, thermopile_mode2, capacitor_mode2, magnetometer_mode2, mode2_duration]

# res = generateAllBitstrings([config1, config2, config1])
# print(res)