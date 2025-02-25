import math

"Constants to be used in simulate.py and other associated files"

#### Robot controls ####

AMPLITUDE = math.pi / 2
FREQUENCY = 20
PHASEOFFSET = 0

FRONTLEGAMPLITUDE = math.pi / 2
FRONTLEGFREQUENCY = 20
FRONTLEGPHASEOFFSET = 0

### Simulation Settings

BODY = "body.urdf" # Robot model
LOOP_LENGTH = 1000  # Number of simulation steps
PLANE = "plane.urdf"  # Floor plane
WORLD = "world.sdf"