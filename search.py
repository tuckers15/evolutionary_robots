import os
from paralellHillClimber import PARALLEL_HILL_CLIMBER


phc = PARALLEL_HILL_CLIMBER()

phc.Evolve()

cont = input("Show ?")
phc.Show_Best()
cont = input("Show Again?")
phc.Show_Best()


    