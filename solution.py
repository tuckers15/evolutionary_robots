import constants as c
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

        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1  # 3x2 matrix of random weights in range [-1, 1]
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

        os.system(f"python3 simulate.py {directOrGui} {int(self.myID)} 2>&1 &")

    
    def Wait_For_Simulation_To_End(self):


        fitnessFileName = "fitness"+str(self.myID)+".txt"

        print(fitnessFileName)

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

        pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[self.length, self.width, self.height])

        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-0.5,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0] , size=[0.2, 1, 0.2])


        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,0.5,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0] , size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name = "Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position= [-0.5, 0, 1], jointAxis= "0 1 0")
        pyrosim.Send_Cube(name = "LeftLeg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])
        
        pyrosim.Send_Joint(name = "Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position= [0.5,0,1], jointAxis= "0 1 0")
        pyrosim.Send_Cube(name = "RightLeg", pos=[0.5,0,0], size=[1, 0.2, 0.2])
        
        pyrosim.Send_Joint(name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [1,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5], size=[0.2, 0.2, 1])
        

        pyrosim.End()
      
    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "RightLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 3, linkName = "LeftLowerLeg")
        

        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 5 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 6 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name = 7 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name = 8 , jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 9 , jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 10, jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 11, jointName = "RightLeg_RightLowerLeg")

        sensor_neuron_names = list(range(0,c.numSensorNeurons))
        motor_neuron_names = list(range(0,c.numMotorNeurons))

        for currentRow in sensor_neuron_names:
            for currentColumn in motor_neuron_names:
    
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])
            

        pyrosim.End()
   

    def Get_Fitness():
        pass #TODO: come back a build get fitness
    
    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons-1)
        randomCol = random.randint(0,c.numMotorNeurons-1)

        self.weights[randomRow,randomCol] = random.random() * 2 - 1

 
    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID
        