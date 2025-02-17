import numpy
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time

LOOP_LENGTH = 500

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #adding data path for plane.urdf

p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) #optional (commented out for now)

p.setGravity(0,0,-9.8) #gravity force

planeId = p.loadURDF("plane.urdf") #floor plane
robotId = p.loadURDF("body.urdf") #floor plane

p.loadSDF("world.sdf") #importing world stored in box.sdf

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(LOOP_LENGTH)
frontLegSensorValues = numpy.zeros(LOOP_LENGTH)
# print(backLegSensorValues) 
# exit()

for i in range(LOOP_LENGTH):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    time.sleep(1/60)


# print(backLegSensorValues) 

print("Saving Data")

numpy.save('data/backLegValues', backLegSensorValues)
numpy.save('data/frontLegValues', frontLegSensorValues)

print("Closing simulation")

p.disconnect()