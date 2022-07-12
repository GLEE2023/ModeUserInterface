# get all possible configs for tmp, 20 total modes 
# get all possible configs 

import itertools

def generateBitsTMP117(bit_count): # TMP - 6 bits to encode 48 different configurations
    binary_strings = []
    def generateBinary(n, bs=''):
        if len(bs) == n:
            binary_strings.append(bs)
        else:
            generateBinary(n, bs + '0')
            generateBinary(n, bs + '1')

    generateBinary(bit_count)
    return binary_strings

binary_strings = generateBitsTMP117(6)
print(binary_strings)



