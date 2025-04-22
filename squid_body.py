import constants as c
import pyrosim.pyrosim as pyrosim

def Generate_Body(self):

        pyrosim.Start_URDF("body.urdf")

        torso_height = 0.6
        leg_offset = 0.25
        upper_leg_length = 0.4
        lower_leg_length = 0.4

        # Central torso (tall and narrow)
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 0.8 + torso_height / 2], size=[0.4, 0.4, torso_height])

        directions = {
            "Front": [0,  leg_offset],
            "Back":  [0, -leg_offset],
            "Left":  [-leg_offset, 0],
            "Right": [ leg_offset, 0],
        }

        for dir_name, (x, y) in directions.items():
            # Hip joint - connects torso to upper leg
            joint_name_1 = f"Torso_{dir_name}UpperLeg"
            upper_leg_name = f"{dir_name}UpperLeg"
            if dir_name == "Front" or dir_name == "Back":
                pyrosim.Send_Joint(
                    name=joint_name_1,
                    parent="Torso",
                    child=upper_leg_name,
                    type="revolute",
                    position=[x, y, 0.8],
                    jointAxis="1 0 0"
                )
            else:
                pyrosim.Send_Joint(
                    name=joint_name_1,
                    parent="Torso",
                    child=upper_leg_name,
                    type="revolute",
                    position=[x, y, 0.8],
                    jointAxis="0 1 0"
                )
            pyrosim.Send_Cube(
                name=upper_leg_name,
                pos=[0, 0, -upper_leg_length/2],
                size=[0.1, 0.1, upper_leg_length]
            )

            # Knee joint - extends leg further down
            joint_name_2 = f"{dir_name}UpperLeg_{dir_name}LowerLeg"
            lower_leg_name = f"{dir_name}LowerLeg"
            if dir_name == "Front" or dir_name == "Back":
                pyrosim.Send_Joint(
                    name=joint_name_2,
                    parent=upper_leg_name,
                    child=lower_leg_name,
                    type="revolute",
                    position=[0, 0, -upper_leg_length],
                    jointAxis="1 0 0"
                )
            else:
                pyrosim.Send_Joint(
                    name=joint_name_2,
                    parent=upper_leg_name,
                    child=lower_leg_name,
                    type="revolute",
                    position=[0, 0, -upper_leg_length],
                    jointAxis="0 1 0"
                )

            pyrosim.Send_Cube(
                name=lower_leg_name,
                pos=[0, 0, -lower_leg_length/2],
                size=[0.1, 0.1, lower_leg_length]
            )

        pyrosim.End()


def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        sensor_id = 0
        motor_id = c.numSensorNeurons

        for dir_name in ["Front", "Back", "Left", "Right"]:
            # Sensor on lower leg
            pyrosim.Send_Sensor_Neuron(name=sensor_id, linkName=f"{dir_name}LowerLeg")
            sensor_id += 1

        for dir_name in ["Front", "Back", "Left", "Right"]:
            # Hip motor
            pyrosim.Send_Motor_Neuron(name=motor_id, jointName=f"Torso_{dir_name}UpperLeg")
            motor_id += 1
            # Knee motor
            pyrosim.Send_Motor_Neuron(name=motor_id, jointName=f"{dir_name}UpperLeg_{dir_name}LowerLeg")
            motor_id += 1

        for i in range(c.numSensorNeurons):
            for j in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(
                    sourceNeuronName=i,
                    targetNeuronName=j + c.numSensorNeurons,
                    weight=self.weights[i][j]
                )

        pyrosim.End()