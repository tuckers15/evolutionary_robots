import os
from paralellHillClimber import PARALLEL_HILL_CLIMBER


phcA = PARALLEL_HILL_CLIMBER(weight_dist=0)

phcA.Evolve()


phcB = PARALLEL_HILL_CLIMBER(weight_dist=1)

phcB.Evolve()

# phcC = PARALLEL_HILL_CLIMBER(weight_dist=2)
# phcC.Evolve()

phcA.Plot_Best_Fit_Per_Gen(filename="figures/phcA_best_by_gen")
phcB.Plot_Best_Fit_Per_Gen(filename="figures/phcB_best_by_gen")

phcA.Plot_Avg_Fit_Per_Gen(filename="figures/phcA_avg_by_gen")
phcB.Plot_Avg_Fit_Per_Gen(filename="figures/phcB_avg_by_gen")

phcA.Plot_Max_Z_Per_Gen(filename="figures/phcA_max_z_by_gen")
phcB.Plot_Max_Z_Per_Gen(filename="figures/phcB_max_z_by_gen")
# phcC.Plot_Max_Z_Per_Gen(filename="figures/phcC_max_z_by_gen")




cont = input("Show A?")
phcA.Show_Best()
cont = input("Show B?")
phcB.Show_Best()




    