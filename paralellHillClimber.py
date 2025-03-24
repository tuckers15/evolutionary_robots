import constants as c
import copy
import os
from solution import SOLUTION

class PARALLEL_HILL_CLIMBER:

    def __init__(self):

        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")

        self.nextAvailableID = 0

        #self.parent = SOLUTION()
        self.parents = {}

        for i in range(c.POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

  


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
            if self.children[key].fitness < self.parents[key].fitness:
       
                self.parents[key] = self.children[key]
                
       
    def Show_Best(self):
        
        lowest_fitness = float("inf")  # Start with an infinitely large number
        best_parent_id = None

        for key, parent in self.parents.items():
            fitness_value = float(parent.fitness)  # Convert to float

            # Update lowest fitness
            if fitness_value < lowest_fitness:
                lowest_fitness = fitness_value
                best_parent_id = key
                best_parent = parent

        print("Best parent id was: " + str(best_parent_id))

        best_parent.Start_Simulation("GUI")

        

        
    def Print(self):
        for key, parent in self.parents.items():
            print(f"Parent {key} fitness: {parent.fitness} Child {key} fitness: {self.children[key].fitness}")

        print("\n")