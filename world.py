import constants as c
import pybullet as p

class WORLD:
    def __init__(self):
        self.planeId = p.loadURDF(c.PLANE)  # Floor plane
        p.loadSDF(c.WORLD)  # Import world stored in world.sdf