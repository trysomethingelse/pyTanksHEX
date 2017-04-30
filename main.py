import numpy as np

from random import randint

from mapGenerator import MapGenerator
from tank import MovableObject, Bullet

from PyQt5.QtCore import QObject, Qt, QTimer
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtSvg

import sys


class TanksWindow(QDialog):
    WINDOW_WIDTH = 620
    WINDOW_HEIGHT = 620
    SCENE_MARGIN = 20  # chroni przed wyświtlaniem scroll bar

    myTank = MovableObject()
    myEnemies = []  # tablica wrogów
    map = MapGenerator()
    timer = QTimer()

    def __init__(self):

        self.map.generate()
        QMainWindow.__init__(self)
        self.ui = loadUi('./gui.ui', self)
        self.setWindowTitle('pyTanksHEX')
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.actualizeStatesFromMap()
        self.drawMap()

        # timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.randomMove)
        self.timer.start(90000)

    def actualizeStatesFromMap(self):  # aktualizuje pozycję obiektów na podstawie rozmieszczenia ich na mapie
        enemies = 0  # liczba wrogów
        for position, element in np.ndenumerate(self.map.plane):
            if element == self.map.AGENT:
                self.myTank.position = position
            elif element == self.map.ENEMY:
                self.myEnemies.append(MovableObject())  # dodanie kolejnego obiektu wroga
                self.myEnemies[enemies].position = position  # przypisz pozycje z mapy do zmiennych w obiekcie
                enemies += 1

    def drawMap(self):
        [startX, startY] = [-self.WINDOW_WIDTH / 2, -self.WINDOW_HEIGHT / 2]

        self.mapScene = QGraphicsScene(startX + self.SCENE_MARGIN, startY + self.SCENE_MARGIN,
                                       self.WINDOW_WIDTH - self.SCENE_MARGIN, self.WINDOW_HEIGHT - self.SCENE_MARGIN)
        self.map.startX = -self.mapScene.width() / 2
        self.map.startY = -self.mapScene.height() / 2

        self.ui.graphicsView.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.map.graphicMap(self.mapScene)
        self.ui.graphicsView.setScene(self.mapScene)


        self.map.planeToGraphics(self.myTank)

    def keyPressEvent(self, event):
        self.myTank.oldTankPos = self.myTank.position  # przepisz pozycje przed aktualizacja

        if event.key() == Qt.Key_W:
            self.myTank.move(1)
        elif event.key() == Qt.Key_S:
            self.myTank.move(-1)
        elif event.key() == Qt.Key_A:
            self.myTank.rotate(-1)
        elif event.key() == Qt.Key_L:#zapisanie gry
            self.map.saveDataToXML()
        elif event.key() == Qt.Key_D:
            self.myTank.rotate(1)
        elif event.key() == Qt.Key_X:
            # myTank.shoot()
            myBullet = Bullet()
            myBullet.position = self.myTank.position  # pozycja pocisku to pozycja czolgu
            myBullet.rotation = self.myTank.rotation
            myBullet.exist = True

            while myBullet.exist:
                myBullet.move(1)
                # jesli pocisk wychodzi za self.mape
                if myBullet.position[0] < 0 or myBullet.position[1] < 0 or \
                                myBullet.position[1] >= self.map.HEIGHT or myBullet.position[0] >= self.map.WIDTH:
                    myBullet.exist = False
                    continue

                onTile = self.map.plane[myBullet.position[0], myBullet.position[1]]  # co jest na danej plytce

                if onTile == self.map.ENEMY:
                    for enemy in self.myEnemies:  # poszukiwanie właściwego wroga w tablicy
                        if enemy.position[0] == myBullet.position[0] and enemy.position[1] == myBullet.position[1]:
                            enemy.health -= myBullet.health
                            if enemy.health <= 0:  # jesli wrog nie ma życia to usuwanie go z mapy
                                self.map.plane[myBullet.position[0], myBullet.position[1]] = 0
                                self.map.tileRefresh(myBullet.position, self.map.EMPTY)  # aktualizacja mapy
                    myBullet.exist = False

                elif onTile == self.map.DESTR:
                    self.map.plane[myBullet.position[0], myBullet.position[1]] = 0
                    myBullet.exist = False
                    self.map.tileRefresh(myBullet.position, self.map.EMPTY)
                elif onTile == self.map.NONDESTR:
                    myBullet.exist = False

        # wychodzneie poza mapę
        if self.myTank.position[0] < 0 or self.myTank.position[1] < 0 or self.myTank.position[1] >= self.map.HEIGHT or \
                        self.myTank.position[
                            0] >= self.map.WIDTH:
            self.myTank.position = self.myTank.oldTankPos

        onTile = self.map.plane[self.myTank.position[0], self.myTank.position[1]]  # co jest na danej plytce

        # jesli kolizja z przeszkoda
        if onTile != self.map.EMPTY:
            self.myTank.position = self.myTank.oldTankPos

        self.map.plane[
            self.myTank.oldTankPos[0], self.myTank.oldTankPos[1]] = self.map.EMPTY  # usuwanie czolgu ze starej pozycji
        self.map.plane[self.myTank.position[0], self.myTank.position[1]] = self.map.AGENT  # dodawanie czolgu

        # self.map.planeToGraphics(self.myTank)#aktualizacja grafiki
        self.map.tankRefresh(self.myTank, 1)

    def randomMove(self):

        for index, enemy in enumerate(self.myEnemies):
            if enemy.health > 0:  # gdy przeciwnik jeszcze żyje
                self.myEnemies[index].oldTankPos = self.myEnemies[index].position  # przepisuje starą pozycje
                if randint(1, 10) > 5: self.myEnemies[index].rotation = randint(0, 5)  # zmiana kierunku w x% przypadków
                direction = randint(0, 7)
                if direction == 0:
                    direction = -1  # wartosc do tyłu to -1 w metodzie czołgu
                else:
                    direction = 1

                self.myEnemies[index].move(direction)

                # wychodzneie poza mapę----------------------------------------------------------------
                if self.myEnemies[index].position[0] < 0 or self.myEnemies[index].position[1] < 0 or \
                                self.myEnemies[index].position[1] >= self.map.HEIGHT or \
                                self.myEnemies[index].position[0] >= self.map.WIDTH:
                    self.myEnemies[index].position = self.myEnemies[index].oldTankPos

                onTile = self.map.plane[
                    self.myEnemies[index].position[0], self.myEnemies[index].position[1]]  # co jest na danej plytce

                # jesli kolizja z przeszkoda
                if onTile != self.map.EMPTY:
                    self.myEnemies[index].position = self.myEnemies[index].oldTankPos
                else:  # aktualizuj tylko gdy zmiana
                    self.map.plane[self.myEnemies[index].oldTankPos[0], self.myEnemies[index].oldTankPos[
                        1]] = self.map.EMPTY  # usuwanie czolgu ze starej pozycji
                    self.map.plane[self.myEnemies[index].position[0], self.myEnemies[index].position[
                        1]] = self.map.ENEMY  # dodawanie czolgu
                    # wychodzneie poza mapę----------------------------------------------------------------
                    self.map.tankRefresh(self.myEnemies[index], 0)  # odświeża nową pozycję czołgu


if (__name__ == "__main__"):
    qApp = QApplication(sys.argv)
    app = TanksWindow()
    # app.map.toConsole()
    app.show()

    sys.exit(qApp.exec_())
