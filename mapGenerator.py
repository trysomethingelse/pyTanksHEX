import numpy as np


class mapGenerator:
    WIDTH = 10
    HEIGHT = 10

    ENEMIES = 1
    ENEMY = -10
    EMPTY = 0
    AGENT = 10
    DESTR = 9
    NONDESTR = -9

    plane = np.zeros([WIDTH,HEIGHT])

    def generate(self):
        self.plane[5,5] = self.AGENT
        self.plane[0,0] = self.ENEMY

    def toConsole(self):
        print(self.plane)