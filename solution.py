import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
import sys
import time


class SOLUTION:

    length = 1
    width = 1
    height = 1

    x = 0
    y = 0
    z = 0.5

    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID

        self.weights = np.random.rand(3, 2) * 2 - 1  # 3x2 matrix of random weights in range [-1, 1]
        #print(self.weights)

    
        #exit()

    def Print(self):
        for row in self.weights:
            print(row)

    def Evaluate(self, directOrGui):
        pass

    def Start_Simulation(self, directOrGui):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()

        os.system("python3 simulate.py " + directOrGui +" " + str(self.myID) + " 2&>1 &")

    
    def Wait_For_Simulation_To_End(self):

        fitnessFileName = "fitness"+str(self.myID)+".txt"

        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        f = open(fitnessFileName)
        self.fitness = float(f.read())
        f.close()

        #print("solution: " + str(self.myID)+ " fitness: " + str(self.fitness))

        os.system("rm fitness"+str(self.myID)+".txt")
        


    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        pyrosim.Send_Cube(name="Box1", pos=[self.x+5,self.y+5, self.z] , size=[self.length, self.width, self.height])
                    

        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[self.length, self.width, self.height])

        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[self.length, self.width, self.height])


        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[self.length, self.width, self.height])

        

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")

        pyrosim.Send_Motor_Neuron(name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_FrontLeg")

        sensor_neuron_names = list(range(0,3))
        motor_neuron_names = list(range(0,2))

        for currentRow in sensor_neuron_names:
            for currentColumn in motor_neuron_names:
    
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + 3, weight = self.weights[currentRow][currentColumn])
            

        pyrosim.End()

    def Get_Fitness():
        pass #TODO: come back a build get fitness
    
    def Mutate(self):
        randomRow = random.randint(0,2)
        randomCol = random.randint(0,1)

        self.weights[randomRow,randomCol] = random.random() * 2 - 1

 
    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID
        