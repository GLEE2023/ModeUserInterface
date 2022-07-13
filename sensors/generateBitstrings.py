import itertools
from re import L
import numpy as np

def generateBitsTMP117(tmpParams): # TMP - 6 bits to encode 48 different configurations
    possCCtimes = {'0.0155': 0b000, '0.125': 0b001, '0.25': 0b010, '0.5': 0b011, '1': 0b100, '4': 0b101, '8': 0b110, '16': 0b111}
    possOStimes = {'0.0155': 0b000, '0.125': 0b001, '0.5': 0b011, '1': 0b100}
    possAveraging = {'0': 0b00, '8': 0b01, '32': 0b10, '64': 0b11}
    possModes = {"OS": 0b0, "CC": 0b1 }

    # error check
    allBitstrings = {}
    for config in tmpParams:
        arr = config.split("_")
        mode = arr[0]
        averages = arr[1]
        convTime = arr[2]

        bitstring = []
        if mode == "CC":
            bitstring.append(bin(possModes[mode]))
            bitstring.append(bin(possCCtimes[convTime]))
            bitstring.append(bin(possAveraging[averages]))
        elif mode == "OS":
            bitstring.append(bin(possModes[mode]))
            bitstring.append(bin(possOStimes[convTime]))
            bitstring.append(bin(possAveraging[averages]))
        elif mode == "OFF": 
            bitstring = bin(0b0)

        allBitstrings[config] = bitstring
    
    return allBitstrings

def generateAll(tmpParams, ):
    generateBitsTMP117(tmpParams)
    generateBitsMPU6050()






