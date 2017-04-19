import numpy as np
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore,QtSvg

class MapGenerator:
    WIDTH = 10
    HEIGHT = 10
    TILE_WIDTH = 50
    TILE_HEIGHT = 50

    ENEMIES = 1
    ENEMY = -10
    EMPTY = 0
    AGENT = 10
    DESTR = 9
    NONDESTR = -9
    BULLET = -1

    plane = np.zeros([WIDTH, HEIGHT])

    def generate(self):
        self.plane[4, :] = np.ones([1, self.WIDTH]) * self.DESTR  # pas zniszczalnych plytek
        self.plane[3, 0:3] = np.ones([1, 3]) * self.NONDESTR

        self.plane[5, 5] = self.AGENT
        self.plane[0, 0] = self.ENEMY

    def toConsole(self):
        print(self.plane)
    def graphicMap(self,handleScene):
        # svgHEX = np.empty([self.WIDTH,self.HEIGHT])
        svgHEX = [[QtSvg.QSvgWidget() for i in range(0,self.WIDTH)] for j in range(0,self.HEIGHT)]
        [startX,startY] = [-handleScene.width()/2,-handleScene.height()/2]
        # for i in range(0,self.WIDTH):
        #     for k in range(0,self.HEIGHT):

        for index,element in np.ndenumerate(svgHEX):
            svgHEX[index[0]][index[1]]=(QtSvg.QSvgWidget('./images/hex.svg'))
            svgHEX[index[0]][index[1]].setGeometry(startX+index[0]*self.TILE_WIDTH,startY+index[1]*self.TILE_HEIGHT,self.TILE_WIDTH,self.TILE_HEIGHT)
            handleScene.addWidget(svgHEX[index[0]][index[1]])
