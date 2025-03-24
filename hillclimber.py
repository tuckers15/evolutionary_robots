import constants as c
import copy
from solution import SOLUTION

class HILL_CLIMBER:

    def __init__(self):
        self.parent = SOLUTION()


    def Evolve(self):
        self.parent.Evaluate("GUI")

        for currentGeneration in range(c.NUMBER_OF_GENERATIONS):
            self.Evolve_For_One_Generation()

    
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
    
        self.Select()
  
    
    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()
        #print(self.parent.weights)
        #print(self.child.weights)
        # exit()

    def Select(self):
        # print("parent fit: " + self.parent.fitness)
        # print("child fit: " + self.child.fitness)
        if self.parent.fitness < self.child.fitness:
            self.parent = self.child
       
    def Show_Best(self):
        self.parent.Evaluate("GUI")

        
    def Print(self):
        print("parent: " + self.parent.fitness +", child: " + self.child.fitness)