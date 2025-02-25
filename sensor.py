import constants as c
import numpy
import pyrosim.pyrosim as pyrosim

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.LOOP_LENGTH)

    
    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)  
        if t == c.LOOP_LENGTH - 1:
            print(f"Sensor {self.linkName} values: {self.values}")
    
    def Save_Values(self):
        print("Saving Sensor Data")

        numpy.save(f"data/{self.linkName}Values", self.values)

        print("Sensor data saved")