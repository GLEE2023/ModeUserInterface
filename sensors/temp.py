import numpy as np
import matplotlib
import pandas as pd


def ContinuousConversion(): 
	activeConversionTime = float(convCycle[1])*0.0155
	standbyTime = float(convCycle[0]) - activeConversionTime
	amps = ((135*activeConversionTime) + (1.25*standbyTime))/float(convCycle[0])

#def OneShot():

def TMP117data(time, frequency, mode, standby, averaging=8):
	if mode == "CC": 
		power = ContinuousConversion()
		
	elif mode == "OS":
		power = OneShot()

	#else: # low limit stuff

	return power, time #returns data and time as functions of time

# code cell in jupyter notebook to call the functions
time = 1
frequency = 1
mode = 'OS'
averaging = 0
conversion = 0 #[000,001,010,011]
parameters = {'Conversionrate':conversion, 'averaging':averaging}


