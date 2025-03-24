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

    def __init__(self, directOrGui, solutionId):

        self.solutionID = solutionId

        self.direcOrGui = directOrGui
        
        if directOrGui == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
            
        elif directOrGui == "GUI":
            self.physicsClient = p.connect(p.GUI)
        
        else:
            print("No physicsClient specified, default is DIRECT")
            self.physicsClient = p.connect(p.DIRECT)

        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)  # close the gui
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # Adding data path for plane.urdf

        self.world = WORLD()
        self.robot = ROBOT(self.solutionID)


        p.setGravity(0, 0, -9.8)  # Gravity force

            


    def Run(self):

        for i in range(c.LOOP_LENGTH):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)

            if self.direcOrGui == "GUI":
                time.sleep(c.SLEEP_TIMER)
            
    
    def Get_Fitness(self):
        self.robot.Get_Fitness()
        
