import numpy as np
import math

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtSvg, Qt
from xml.dom import minidom


class MapGenerator:
    WIDTH = 8  # liczba plytek
    HEIGHT = 24
    TILE_WIDTH = 50
    TILE_HEIGHT = 50

    MY_TANK = 1
    NOT_MY_TANK = 0

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

    # wymienione typy płytek które nie są ruchome
    TILES_TYPES = 4
    CLEAR_TILE = 0
    DESTRUCTABLE_TILE = 1
    NONDESTRTABLE_TILE = 2
    BULLET_TILE = 3
    otherTiles = []

    # odpowiednia rotacja czołgu to odpowiedni indeks w tabeli
    enemyTiles = []
    myTankTiles = []

    def __init__(self):
        print("map init")

    def generate(self):
        self.plane[4, :7] = np.ones([1, 7]) * self.DESTR  # pas zniszczalnych plytek
        self.plane[3, 0:3] = np.ones([1, 3]) * self.NONDESTR

        self.plane[0, 0] = self.AGENT
        self.plane[7, 15] = self.ENEMY
        self.plane[3, 23] = self.ENEMY



    def playHistory(self):
        doc = minidom.parse("data.xml")

    def toConsole(self):
        print(self.plane)

    def graphicMap(self, handleScene):
        self.tilesToMemory()

        self.pngHEX = [[QLabel() for i in range(0, self.HEIGHT)] for j in range(0, self.WIDTH)]

        for index, element in np.ndenumerate(self.pngHEX):

            self.pngHEX[index[0]][index[1]].setPixmap(self.otherTiles[self.CLEAR_TILE])

            # obliczenia pozycji
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
        self.otherTiles.append(QtGui.QPixmap("./images/hex.png"))
        self.otherTiles.append(QtGui.QPixmap("./images/hexBrickDestr.png"))
        self.otherTiles.append(QtGui.QPixmap("./images/hexBrickNonDestr.png"))
        self.otherTiles.append(QtGui.QPixmap("./images/hexBullet.png"))
        for index in range(self.TILES_TYPES):  # ustawia odpowiednie rozmiary płytek
            self.otherTiles[index] = self.otherTiles[index].scaled(self.TILE_WIDTH, self.TILE_HEIGHT)

        # płytki czołgów
        for index in range(6):  # wszystkie możliwe ustawienia kąta
            self.myTankTiles.append(QtGui.QPixmap('./images/myTank/hexMyTank' + str(index) + '.png'))
            self.myTankTiles[index] = self.myTankTiles[index].scaled(self.TILE_WIDTH,
                                                                     self.TILE_HEIGHT)  # przestaw rozmiar

            self.enemyTiles.append(QtGui.QPixmap('./images/enemy/hexEnemy' + str(index) + '.png'))
            self.enemyTiles[index] = self.enemyTiles[index].scaled(self.TILE_WIDTH,
                                                                   self.TILE_HEIGHT)  # przestaw rozmiar

    def planeToGraphics(self, tank):  # odświeża całą mapę
        for index, element in np.ndenumerate(self.plane):
            tile = self.otherTiles[self.CLEAR_TILE]  # jesli płytka pusta

            if element == self.AGENT:
                tile = self.myTankTiles[tank.rotation]
            if element == self.ENEMY:
                tile = self.enemyTiles[tank.rotation]
            if element == self.DESTR:
                tile = self.otherTiles[self.DESTRUCTABLE_TILE]
            if element == self.NONDESTR:
                tile = self.otherTiles[self.NONDESTRTABLE_TILE]  # jesli płytka pusta
            if element == self.BULLET:
                tile = self.otherTiles[self.BULLET_TILE]  # jesli płytka pusta

            self.pngHEX[index[0]][index[1]].setPixmap(tile)
        self.mapChange()  # wywoływana w każdej zmianie mapy

    def tankRefresh(self, tank, isMy):

        if isMy == 1:
            tile = self.myTankTiles[tank.rotation]
        else:
            tile = self.enemyTiles[tank.rotation]

        self.pngHEX[tank.oldPos[0]][tank.oldPos[1]].setPixmap(self.otherTiles[self.CLEAR_TILE])
        self.pngHEX[tank.position[0]][tank.position[1]].setPixmap(tile)
        self.mapChange()  # wywoływana w każdej zmianie mapy

    def tileRefresh(self, tile, newType):  # używane do podmieniania płytki
        if (newType == self.EMPTY):
            self.pngHEX[tile[0]][tile[1]].setPixmap(self.otherTiles[self.CLEAR_TILE])
        if (newType == self.BULLET):
            self.pngHEX[tile[0]][tile[1]].setPixmap(self.otherTiles[self.BULLET_TILE])
        self.mapChange()  # wywoływana w każdej zmianie mapy

        self.saveHistory()

    def mapChange(self):# wywoływana w każdej zmianie mapy
        self.saveHistory()

    def saveHistory(self):
        print("zapisywanie_", self.historyStep)
        moment = self.doc.createElement("moment")
        moment.setAttribute("step", str(self.historyStep))

        for index, element in np.ndenumerate(self.plane):
            name = "hex_" + str(index[0]) + "," + str(index[1])
            change = self.doc.createElement(name)
            change.setAttribute("map", str(element))  # zapis calej mapy
            moment.appendChild(change)
        self.root.appendChild(moment)
        self.doc.appendChild(self.root)
        self.historyStep += 1
    def saveDataToXML(self):
        self.doc.writexml(open('data.xml', 'w'),
                          indent="  ",
                          addindent="  ",
                          newl='\n')
