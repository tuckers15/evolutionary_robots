import pyrosim.pyrosim as pyrosim
import random


length = 1
width = 1
height = 1

x = 0
y = 0
z = 0.5


def Create_World():
    pyrosim.Start_SDF("world.sdf")

    pyrosim.Send_Cube(name="Box1", pos=[x+5,y+5,z] , size=[length, width, height])
                

    pyrosim.End()

def Generate_Body():
    pyrosim.Start_URDF("body.urdf")

    pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[length, width, height])

    pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[length, width, height])


    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[length, width, height])

    

    pyrosim.End()

def Generate_Brain():
   
    pyrosim.Start_NeuralNetwork("brain.nndf")

    # Sensor Neurons
    sensor_neurons = {
        0: "Torso",
        1: "BackLeg",
        2: "FrontLeg"
    }
    
    # Motor Neurons
    motor_neurons = {
        3: "Torso_BackLeg",
        4: "Torso_FrontLeg"
    }

    # Create Sensor Neurons
    for name, link in sensor_neurons.items():
        pyrosim.Send_Sensor_Neuron(name=name, linkName=link)

    # Create Motor Neurons
    for name, joint in motor_neurons.items():
        pyrosim.Send_Motor_Neuron(name=name, jointName=joint)

    # Generate synapses using nested loops
    for sensor in sensor_neurons.keys():
        for motor in motor_neurons.keys():
            weight = random.random() * 2 - 1 #scales between -1 and 1
            pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight=weight)    



   
    


    pyrosim.End()



Create_World()
Generate_Body()
Generate_Brain()