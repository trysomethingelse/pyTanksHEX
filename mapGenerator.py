import numpy as np
import math

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtSvg,Qt
from xml.dom import minidom



class MapGenerator:
    WIDTH = 8  # liczba plytek
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
    svgHEX = None
    pngHEX = None
    startX = 0
    startY = 0

    allow = True

    doc = minidom.Document()
    root = doc.createElement("mapHistory")
    historyStep = 0

    TILES_TYPES = 5
    CLEAR_TILE = 0
    ENEMY_TILE = 1
    MYTANK_TILE = 2
    DESTRUCTABLE_TILE = 3
    NONdESTRTABLE_TILE = 4
    memTiles = []




    def __init__(self):
        print("init")


    def generate(self):
        self.plane[4, :7] = np.ones([1, 7]) * self.DESTR  # pas zniszczalnych plytek
        self.plane[3, 0:3] = np.ones([1, 3]) * self.NONDESTR

        self.plane[0, 0] = self.AGENT
        self.plane[7, 15] = self.ENEMY
        self.plane[3, 23] = self.ENEMY
    def saveHistory(self):
        print("zapisywanie_",self.historyStep)
        moment = self.doc.createElement("moment")
        moment.setAttribute("step",str(self.historyStep))


        for index,element in np.ndenumerate(self.plane):
            name = "hex_"+str(index[0])+","+str(index[1])
            change = self.doc.createElement(name)
            change.setAttribute("map",str(element))#zapis calej mapy
            moment.appendChild(change)
        self.root.appendChild(moment)
        self.doc.appendChild(self.root)
        self.historyStep += 1
    def saveDataToXML(self):
        self.doc.writexml(open('data.xml', 'w'),
                          indent="  ",
                          addindent="  ",
                          newl='\n')

        self.doc.unlink()
    def playHistory(self):
        doc = minidom.parse("data.xml")
    def toConsole(self):
        print(self.plane)
    # def graphicMap(self, handleScene):
    #     self.svgHEX = [[QtSvg.QSvgWidget() for i in range(0, self.HEIGHT)] for j in range(0, self.WIDTH)]
    #
    #     for index, element in np.ndenumerate(self.svgHEX):
    #         self.svgHEX[index[0]][index[1]] = self.memoryEmptyTile
    #
    #         offsetX = 3 / 2 * self.TILE_WIDTH * index[0]
    #
    #         if index[1] % 2 == 1:  # przesuniecie o staly offset
    #             offsetX += 3 / 4 * self.TILE_WIDTH
    #
    #         offsetY = index[1] * self.TILE_HEIGHT / 2
    #
    #         self.svgHEX[index[0]][index[1]].setGeometry(self.startX + offsetX,
    #                                                     self.startY + offsetY,
    #                                                     self.TILE_WIDTH,
    #                                                     self.TILE_HEIGHT)  # odpowiada za rysowanie płytki w odpowiednim miejscu
    #         self.svgHEX[index[0]][index[1]].setStyleSheet("background-color:transparent;")
    #         handleScene.addWidget(self.svgHEX[index[0]][index[1]])
    def graphicMap(self, handleScene):
        self.tilesToMemory()


        self.pngHEX = [[QLabel() for i in range(0, self.HEIGHT)] for j in range(0, self.WIDTH)]

        for index, element in np.ndenumerate(self.pngHEX):

            self.pngHEX[index[0]][index[1]].setPixmap(self.memTiles[self.CLEAR_TILE])

            #obliczenia pozycji
            offsetX = 3 / 2 * self.TILE_WIDTH * index[0]

            if index[1] % 2 == 1:  # przesuniecie o staly offset
                offsetX += 3 / 4 * self.TILE_WIDTH
            offsetY = index[1] * self.TILE_HEIGHT / 2

            self.pngHEX[index[0]][index[1]].setGeometry(self.startX + offsetX,
                                                        self.startY + offsetY,
                                                        self.TILE_WIDTH,
                                                        self.TILE_HEIGHT)  # odpowiada za rysowanie płytki w odpowiednim miejscu

            self.pngHEX[index[0]][index[1]].setStyleSheet("background:transparent;")

            handleScene.addWidget(self.pngHEX[index[0]][index[1]])

    def tilesToMemory(self):
        self.memTiles.append(QtGui.QPixmap("./images/hex.png"))





        self.memTiles[self.CLEAR_TILE] = self.memTiles[self.CLEAR_TILE].scaled(self.TILE_WIDTH, self.TILE_HEIGHT)





    def planeToGraphics(self, tank):  # odświeża całą mapę - wolne
        for index, element in np.ndenumerate(self.plane):
            fileName = "./images/hex.png"#jesli płytka pusta

            if element == self.AGENT:
                fileName = './images/myTank/hexMyTank' + str(tank.rotation) + '.png'
            if element == self.ENEMY:
                fileName = './images/enemy/hexEnemy' + str(tank.rotation) + '.png'
            if element == self.DESTR:
                fileName = './images/hexBrickDestr.png'
            if element == self.NONDESTR:
                fileName = './images/hexBrickNonDestr.png'
            self.pngHEX[index[0]][index[1]].setPixmap(QtGui.QPixmap(fileName))

    def tankRefresh(self, tank, isMy):

        if isMy==1:
            fileName = './images/hexMytank' + str(tank.rotation) + '.svg'
        else:
            fileName = './images/enemy/hexEnemy' + str(tank.rotation) + '.svg'

        self.svgHEX[tank.oldTankPos[0]][tank.oldTankPos[1]].load('./images/hex.svg')
        self.svgHEX[tank.position[0]][tank.position[1]].load(fileName)
        self.saveHistory()



    def tileRefresh(self, tile, newType):
        if (newType == self.EMPTY):  # tzn zniszczenie płytki
           self.svgHEX[tile[0]][tile[1]].load('./images/hex.svg')
        self.saveHistory()