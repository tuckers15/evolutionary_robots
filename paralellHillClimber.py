import constants as c
import copy
import os
from solution import SOLUTION
import matplotlib.pyplot as plt
import datetime

class PARALLEL_HILL_CLIMBER:

    def __init__(self, weight_dist):

        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")

        self.nextAvailableID = 0

        #self.parent = SOLUTION()
        self.parents = {}

        self.weight_dist = weight_dist

        for i in range(c.POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID, weight_dist=self.weight_dist)
            self.nextAvailableID += 1

        self.best_fitness_per_gen = []
        self.avg_fitness_per_gen = []
        self.max_z_over_time = []


  


    def Evolve(self):
        # self.parent.Evaluate("GUI")

        # for currentGeneration in range(c.NUMBER_OF_GENERATIONS):
        #     self.Evolve_For_One_Generation()
        
        self.Evaluate(self.parents)

        for currentGeneration in range(c.NUMBER_OF_GENERATIONS):
            self.Evolve_For_One_Generation()
        

 

    
    def Evolve_For_One_Generation(self):
        self.Spawn()

        # self.child.Set_ID(self.nextAvailableID)
        # self.nextAvailableID += 1

        self.Mutate()
        self.Evaluate(self.children)

        best_z = max(child.max_z for child in self.children.values() if child.max_z is not None)
        self.max_z_over_time.append(best_z)

        
        self.Print()
    
        self.Select()

        

    def Spawn(self):
        #self.child = copy.deepcopy(self.parent)
        self.children = {}

        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
        
        # print(self.children)
        # exit()

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()
        #print(self.parent.weights)
        #print(self.child.weights)
        # exit()

    def Evaluate(self, solutions):
        
        for i in solutions.values():
            # print(f"Evaluating parent {i}...")
            i.Start_Simulation(directOrGui = "DIRECT")
        
        for i in solutions.values():
            i.Wait_For_Simulation_To_End()

      
        


    def Select(self):

        for key in self.parents:
            if self.children[key].fitness > self.parents[key].fitness:
       
                self.parents[key] = self.children[key]
                
        best_fitness = max(parent.fitness for parent in self.parents.values())
        self.best_fitness_per_gen.append(best_fitness)

        avg_fitness = sum(parent.fitness for parent in self.parents.values()) / len(self.parents)
        self.avg_fitness_per_gen.append(avg_fitness)


                
       
    def Show_Best(self):
        
        best_fitness = float(-10000000000.0)  # Start with an impossibly low number
        best_parent_id = None

        for key, parent in self.parents.items():
            fitness_value = float(parent.fitness)  # Convert to float

            # Update lowest fitness
            if fitness_value > best_fitness:
                best_fitness = fitness_value
                best_parent_id = key
                best_parent = parent

        self.Max_Z()

        print("Best parent id was: " + str(best_parent_id))

        best_parent.Start_Simulation("GUI")

        
    def Max_Z(self):
        max_z = -float("inf")
        best_id = None

        for key, parent in self.parents.items():
            if parent.max_z is not None and parent.max_z > max_z:
                max_z = parent.max_z
                best_id = key

        print(f"Max Z achieved: {max_z} by Parent {best_id}")
        
    def Print(self):
        for key, parent in self.parents.items():
            print(f"Parent {key} fitness: {parent.fitness} Child {key} fitness: {self.children[key].fitness}")

        print("\n")



    def Plot_Best_Fit_Per_Gen(self, filename):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{filename}{timestamp}.png"
    
        plt.plot(self.best_fitness_per_gen, label="Best Fitness")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Best Fitness Over Generations")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    def Plot_Avg_Fit_Per_Gen(self, filename):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{filename}{timestamp}.png"
    
        plt.plot(self.best_fitness_per_gen, label="Average Fitness")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Average Fitness Over Generations")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
       
   
    def Plot_Max_Z_Per_Gen(self, filename):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{filename}{timestamp}.png" 

        plt.figure()
        plt.plot(self.max_z_over_time, label="Max Z (Jump Height)", color="purple")
        plt.xlabel("Generation")
        plt.ylabel("Max Z")
        plt.title("Maximum Jump Height Over Generations")
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.savefig(filename)
        plt.close()
