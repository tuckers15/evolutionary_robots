import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

length = 1
width = 1
height = 1

x = 0
y = 0
z = 1.25

#pyrosim.Send_Cube(name="Box", pos=[x,y, z] , size=[length, width, height])


#Outest loop to make five rows
for i in range(5):
    x = 0
    #Outer loop to make five stacks in a row
    for i in range(5):
        z = 1.25
        length = 1
        width = 1
        height = 1
        #For loop for creating a stack of ten boxes getting 10% smaller at each iteration
        for i in range (10):
            pyrosim.Send_Cube(name="Box"+str(i), pos=[x,y,z] , size=[length, width, height])
            z = z + 1
            length = length * .9
            width = width * .9 
            height = height * .9
        x = x + 1
    y = y + 1


pyrosim.End()