import constants as c
import pyrosim.pyrosim as pyrosim

def Generate_Body(self):
    pyrosim.Start_URDF("body.urdf")

    # Torso
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 2.50], size=[self.length, self.width, self.height])

    # Back leg (right under torso, pointing downward)
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                    position=[0, -0.5, 2.50], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="BackLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1.0])

    pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute",
                    position=[0, 0, -1.0], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.75], size=[0.2, 0.2, 1.5])

    # Front leg (symmetric to back leg, for forward stability in jumping)
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                    position=[0, 0.5, 2.50], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1.0])

    pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute",
                    position=[0, 0, -1.0], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.75], size=[0.2, 0.2, 1.5])

    pyrosim.End()


      
def Generate_Brain(self):
    pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

    # Sensor neurons: lower legs (feet)
    pyrosim.Send_Sensor_Neuron(name=0, linkName="BackLowerLeg")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="FrontLowerLeg")

    # Motor neurons: 4 joints total
    pyrosim.Send_Motor_Neuron(name=2, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=3, jointName="BackLeg_BackLowerLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
    pyrosim.Send_Motor_Neuron(name=5, jointName="FrontLeg_FrontLowerLeg")

    sensor_neuron_names = list(range(0, c.numSensorNeurons))
    motor_neuron_names = list(range(0, c.numMotorNeurons))

    for currentRow in sensor_neuron_names:
        for currentColumn in motor_neuron_names:
            pyrosim.Send_Synapse(
                sourceNeuronName=currentRow,
                targetNeuronName=currentColumn + c.numSensorNeurons,
                weight=self.weights[currentRow][currentColumn]
            )

    pyrosim.End()