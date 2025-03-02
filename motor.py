import constants as c
import numpy
import pybullet as p
import pyrosim.pyrosim as pyrosim

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        #print(self.jointName)   #testing
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.AMPLITUDE

        if(self.jointName == b'Torso_BackLeg'):
            self.frequency = c.FREQUENCY/2
        else:
            self.frequency = c.FREQUENCY


        self.phaseOffset = c.PHASEOFFSET

        self.motorValues = self.amplitude * numpy.sin((2 * numpy.pi * self.frequency * numpy.arange(c.LOOP_LENGTH) / c.LOOP_LENGTH) + self.phaseOffset)
        #frontLegMotorValues = self.amplitude * numpy.sin((2 * numpy.pi * self.frequency * numpy.arange(c.LOOP_LENGTH) / c.LOOP_LENGTH) + self.phaseOffset)

    def Set_Value(self, robot, desiredAngle):

        pyrosim.Set_Motor_For_Joint(

                bodyIndex = robot,
                jointName = self.jointName,
                controlMode = p.POSITION_CONTROL,
                targetPosition = desiredAngle,
                maxForce = 10
            )
        
    def Save_Values(self):

        print("Saving motor values")

        numpy.save(f"data/{self.jointName}Values", self.motorValues)

        print("Saved motor values")
