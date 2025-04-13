import constants as c
import numpy as np
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

                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode("utf-8")

                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange

                self.motors[jointName].Set_Value(self, desiredAngle)


                # for motor in self.motors.values():
                #     motor.Set_Value(robot = self.robotId, desiredAngle = desiredAngle)

  
                    #print(f"Joint {jointName} commanded angle: {desiredAngle}")
                # print(neuronName + jointName)
                # print(desiredAngle)


        # for motor in self.motors.values(): 
        #     motor.Set_Value(robot = self.robotId, i = i)
    
    def Get_Fitness(self):
        
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        zPosition = basePosition[2]

        matrix = np.array(self.Get_Sensor_Touch_Values())

        time_steps = matrix.T

        longest_air_streak = 0
        current_air_streak = 0

        for timestep in time_steps:
            if 1 in timestep:
                current_air_streak = 0  # Touch detected
            else:
                current_air_streak += 1

                longest_air_streak = max(longest_air_streak, current_air_streak)
                
    
        total_ground_contacts = np.count_nonzero(matrix == 1)


        fitness = longest_air_streak - 0.01*(total_ground_contacts)

        tmpFileName = "tmp"+ self.solutionId +".txt"
        finFileName = "fitness"+ self.solutionId +".txt"

        f = open(tmpFileName, "w")
        f.write(str(fitness))
        f.close()


        os.system("mv " + tmpFileName + " " + finFileName)

        print(fitness)


    def Get_Sensor_Touch_Values(self):
        sensor_names = [name for name in self.sensors if "Lower" in name]
        sensor_count = len(sensor_names)
        self.matrix = [[0] * sensor_count for _ in range(c.LOOP_LENGTH)]

        for i in range(0, c.LOOP_LENGTH - 1):
            for idx, name in enumerate(sensor_names):
                self.matrix[i][idx] = self.sensors[name].values[i]

        return self.matrix


        