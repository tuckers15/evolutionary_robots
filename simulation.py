import constants as c
import pybullet as p
import pybullet_data
import time

from robot import ROBOT
from world import WORLD


class SIMULATION:

    def __del__(self):
        print("Closing simulation")
        p.disconnect()

    def __init__(self):
       
        self.physicsClient = p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)  # close the gui
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # Adding data path for plane.urdf

        self.world = WORLD()
        self.robot = ROBOT()


        p.setGravity(0, 0, -9.8)  # Gravity force


    def Run(self):
        for i in range(c.LOOP_LENGTH):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Act(i)

        
            time.sleep(1/20)
          
