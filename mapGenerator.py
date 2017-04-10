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
    BULLET = -1

    plane = np.zeros([WIDTH,HEIGHT])

    def generate(self):
        self.plane[4,:] = np.ones([1,self.WIDTH]) * self.DESTR #pas zniszczalnych plytek
        self.plane[3,0:3] =np.ones([1,3]) * self.NONDESTR

        self.plane[5,5] = self.AGENT
        self.plane[0,0] = self.ENEMY

    def toConsole(self):
        print(self.plane)