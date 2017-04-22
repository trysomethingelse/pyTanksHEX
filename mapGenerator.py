import numpy as np
import math
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
        # startX = -200
        # startY = -50
        # for i in range(0,self.WIDTH):
        #     for k in range(0,self.HEIGHT):

        # pal = QPalette(widget.palette())
        # pal.setColor(QPalette.Window, QColor('white'))
        # widget.setPalette(pal)

        for index,element in np.ndenumerate(svgHEX):
            svgHEX[index[0]][index[1]]=(QtSvg.QSvgWidget('./images/hex.svg'))
            if index[1] % 2 == 0 :
                offset =  2 * self.WIDTH
            else:
                offset = self.WIDTH*2 +  2 * self.WIDTH

            # svgHEX[index[0]][index[1]].setGeometry(startX+index[0]*self.TILE_WIDTH+offset,startY+index[1]*self.TILE_HEIGHT+index[1]*math.sqrt(3)/2,self.TILE_WIDTH,self.TILE_HEIGHT)
            svgHEX[index[0]][index[1]].setGeometry(startX,startY,self.TILE_WIDTH,self.TILE_HEIGHT)
            svgHEX[index[0]][index[1]].setStyleSheet("background-color:transparent;")
            handleScene.addWidget(svgHEX[0][0])

        # svgHEX[1][3].setStyleSheet("background-color:red;")

