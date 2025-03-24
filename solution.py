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
        
        pyrosim.Start_NeuralNetwork("brain"+ str(self.myID) +".nndf")

        # Sensor Neurons
        self.sensor_neurons = {
            0: "Torso",
            1: "BackLeg",
            2: "FrontLeg"
        }
        
        # Motor Neurons
        self.motor_neurons = {
            3: "Torso_BackLeg",
            4: "Torso_FrontLeg"
        }

        # Create Sensor Neurons
        for name, link in self.sensor_neurons.items():
            pyrosim.Send_Sensor_Neuron(name=name, linkName=link)

        # Create Motor Neurons
        for name, joint in self.motor_neurons.items():
            pyrosim.Send_Motor_Neuron(name=name, jointName=joint)


        num_sensors, num_motors = self.weights.shape  # Automatically get dimensions

        # Generate synapses using nested loops
        for currentRow in range(num_sensors):  # 3 sensor neurons
            for currentColumn in range(num_motors):  # 2 motor neurons
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow,
                    targetNeuronName=currentColumn + 3,  # Ensure motor neurons are indexed correctly
                    weight=self.weights[currentRow][currentColumn]
            )

        pyrosim.End()

    def Get_Fitness():
        pass #TODO: come back a build get fitness
    
    def Mutate(self):
        #TODO: differing step 59 for sake of dictionary
        row_index = random.randint(0, 2) 
        chosen_motor_neuron = random.choice(list(self.motor_neurons.keys())) 
        column_index = list(self.motor_neurons.keys()).index(chosen_motor_neuron)  #corresponding column index

        self.weights[row_index][column_index] = random.random() * 2 - 1

 


    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID
        