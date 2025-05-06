from simulation import SIMULATION
import sys

directOrGui = sys.argv[1]

if sys.argv[2]:
    solutionID = sys.argv[2]

if sys.argv[3]:
    weight_dist = sys.argv[3]

simulate = SIMULATION(directOrGui, solutionID, weight_dist)

simulate.Run()

simulate.Get_Fitness()

#simulate.Get_Touch_Sensor_Values()






