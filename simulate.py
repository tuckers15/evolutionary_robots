from simulation import SIMULATION
import sys

directOrGui = sys.argv[1]

if sys.argv[2]:
    solutionID = sys.argv[2]

simulate = SIMULATION(directOrGui, solutionID)

simulate.Run()

simulate.Get_Fitness()






