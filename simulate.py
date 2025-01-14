import pybullet as p
import time

physicsClient = p.connect(p.GUI)
#p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) #optional (commented out for now)

for i in range(1000):
    print(i)
    p.stepSimulation()
    time.sleep(1/60)


p.disconnect()