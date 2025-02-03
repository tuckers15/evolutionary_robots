import pybullet as p
import pybullet_data
import time

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #adding data path for plane.urdf

p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) #optional (commented out for now)

p.setGravity(0,0,-9.8) #gravity force

planeId = p.loadURDF("plane.urdf") #floor plane
robotId = p.loadURDF("body.urdf") #floor plane

p.loadSDF("world.sdf") #importing world stored in box.sdf

for i in range(10000):
    print(i)
    p.stepSimulation()
    time.sleep(1/60)


p.disconnect()