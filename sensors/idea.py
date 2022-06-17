def getActiveTimes(): # RETURNS ACTIVE VEC, WORKS FOR ALL SENSORS 
    pass

class TMP:
    def getPower():
        pass
    def getData():
        pass
    def runSim():
        pass

class ACC:
    def getPower():
        pass
    def getData():
        pass
    def runSim():
        pass

class MAG:
    def getPower():
        pass
    def getData():
        pass
    def runSim():
        pass

class THERMO:
    def getPower():
        pass
    def getData():
        pass
    def runSim():
        pass


TMP_object = TMP()
power1, data1 = TMP_object.runSim()

ACC_object = ACC()
power2, data2 = ACC_object.runSim()

MAG_object = MAG()
power3, data3 = MAG_object.runSim()

THERMO_object = THERMO()
power4, data4 = THERMO_object.runSim()


def PLOT(): # PLOTS POWER AND DATA FOR ALL SENSORS
    pass