import numpy as np
import math
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore,QtSvg

class MapGenerator:
    WIDTH = 8 #liczba plytek
    HEIGHT = 24
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
    svgHEX =  None
    startX = 0; startY =0
    def generate(self):
        self.plane[4, :7] = np.ones([1, 7]) * self.DESTR  # pas zniszczalnych plytek
        self.plane[3, 0:3] = np.ones([1, 3]) * self.NONDESTR

        self.plane[5, 5] = self.AGENT
        self.plane[0, 0] = self.ENEMY

    def toConsole(self):
        print(self.plane)

    def graphicMap(self,handleScene):
        self.svgHEX = [[QtSvg.QSvgWidget() for i in range(0, self.HEIGHT)] for j in range(0, self.WIDTH)]

        for index,element in np.ndenumerate(self.svgHEX):
            self.svgHEX[index[0]][index[1]]=QtSvg.QSvgWidget('./images/hex.svg')

            offsetX = 3 / 2 * self.TILE_WIDTH * index[0]

            if index[1] % 2 == 1 : #przesuniecie o staly offset
                offsetX += 3/4*self.TILE_WIDTH

            offsetY = index[1] * self.TILE_HEIGHT/2

            self.svgHEX[index[0]][index[1]].setGeometry(self.startX+offsetX,
                                                   self.startY+offsetY,
                                                   self.TILE_WIDTH,
                                                   self.TILE_HEIGHT)#odpowiada za rysowanie płytki w odpowiednim miejscu
            self.svgHEX[index[0]][index[1]].setStyleSheet("background-color:transparent;")
            handleScene.addWidget(self.svgHEX[index[0]][index[1]])
     

    def planeToGraphics(self):
        for index, element in np.ndenumerate(self.plane):
            if element == self.EMPTY:
                self.svgHEX[index[0]][index[1]].load('./images/hex.svg')
            if element == self.AGENT:
                self.svgHEX[index[0]][index[1]].load('./images/hexMyTank.svg')
            if element == self.DESTR:
                self.svgHEX[index[0]][index[1]].load('./images/hexBrickDestr.svg')
            if element == self.NONDESTR:
                self.svgHEX[index[0]][index[1]].load('./images/hexBrickNonDestr.svg')









