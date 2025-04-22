import math

"Constants to be used in simulate.py and other associated files"

### Robot features ###
numSensorNeurons = 4
numMotorNeurons = 8

#### Robot controls ####

AMPLITUDE = math.pi / 2
FREQUENCY = 20
PHASEOFFSET = 0

motorJointRange = 0.3

FRONTLEGAMPLITUDE = math.pi / 2
FRONTLEGFREQUENCY = 20
FRONTLEGPHASEOFFSET = 0

### Simulation Settings

BODY = "body.urdf" # Robot model
LOOP_LENGTH = 1000  # Number of simulation steps
PLANE = "plane.urdf"  # Floor plane
SLEEP_TIMER = 1/60
WORLD = "world.sdf"


### Search Variables
NUMBER_OF_GENERATIONS = 20
POPULATION_SIZE = 20