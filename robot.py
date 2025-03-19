import constants as c
import pybullet as p
import pyrosim.pyrosim as pyrosim

from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
import os


class ROBOT:
    def __init__(self, solutionId):

        self.solutionId = solutionId

        self.robotId = p.loadURDF(c.BODY)  # Robot model
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain" + self.solutionId +".nndf")

        os.system("rm brain"+self.solutionId+".nndf")

    def Prepare_To_Sense(self):
        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors.values(): 
            sensor.Get_Value(t) 

    def Think(self):
        self.nn.Update()
       # self.nn.Print()
        
    def Prepare_To_Act(self):
        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, i):

        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):

                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)

                desiredAngle = self.nn.Get_Value_Of(neuronName)

                for motor in self.motors.values():
                    motor.Set_Value(robot = self.robotId, desiredAngle = desiredAngle)

  
                    #print(f"Joint {jointName} commanded angle: {desiredAngle}")
                # print(neuronName + jointName)
                # print(desiredAngle)


        # for motor in self.motors.values(): 
        #     motor.Set_Value(robot = self.robotId, i = i)
    
    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId,0)

        positionOfLink0 = stateOfLinkZero[0]

        xCoordinateOfLinkZero = positionOfLink0[0]
        yCoordinateOfLinkeZero = positionOfLink0[1]
        zCoordinateOfLinkZero = positionOfLink0[2]

        tmpFileName = "tmp"+ self.solutionId +".txt"
        finFileName = "fitness"+ self.solutionId +".txt"

        f = open(tmpFileName, "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()


        os.system("mv " + tmpFileName + " " + finFileName)

        print(xCoordinateOfLinkZero)

      