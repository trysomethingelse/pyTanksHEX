import numpy as np

from random import randint

from mapGenerator import MapGenerator
from tank import MovableObject

from PyQt5.QtCore import QObject, Qt, QTimer
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtSvg

import sys


class TanksWindow(QDialog):
    WINDOW_WIDTH = 620
    WINDOW_HEIGHT = 620
    SCENE_MARGIN = 20  # chroni przed wyświtlaniem scroll bar
    BULLET_HEALTH = 30
    TANK_HEALTH = 100


    myTank = MovableObject(TANK_HEALTH)
    myEnemies = []  # tablica wrogów
    bullets = [] #tablica pociskow
    map = MapGenerator()
    randomMoveTimer = QTimer()
    bulletTimer = QTimer()

    def __init__(self):

        self.map.generate()
        QMainWindow.__init__(self)
        self.ui = loadUi('./gui.ui', self)
        self.setWindowTitle('pyTanksHEX')
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.actualizeStatesFromMap()
        self.drawMap()

        # timer
        self.randomMoveTimer.timeout.connect(self.randomMove)
        self.randomMoveTimer.start(900)

        self.bulletTimer.timeout.connect(self.bulletMove)
        self.bulletTimer.start(30)


    def actualizeStatesFromMap(self):  # aktualizuje pozycję obiektów na podstawie rozmieszczenia ich na mapie
        enemies = 0  # liczba wrogów
        for position, element in np.ndenumerate(self.map.plane):
            if element == self.map.AGENT:
                self.myTank.position = position
            elif element == self.map.ENEMY:
                self.myEnemies.append(MovableObject(self.TANK_HEALTH))  # dodanie kolejnego obiektu wroga
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
        self.myTank.oldPos = self.myTank.position  # przepisz pozycje przed aktualizacja

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
            self.bullets.append(MovableObject(self.BULLET_HEALTH))
            self.bullets[-1].position = self.myTank.position  # pozycja pocisku to pozycja czolgu
            self.bullets[-1].rotation = self.myTank.rotation


        # wychodzneie czołgu poza mapę
        if self.myTank.position[0] < 0 or self.myTank.position[1] < 0 or self.myTank.position[1] >= self.map.HEIGHT or \
                        self.myTank.position[
                            0] >= self.map.WIDTH:
            self.myTank.position = self.myTank.oldPos

        onTile = self.map.plane[self.myTank.position[0], self.myTank.position[1]]  # co jest na danej plytce

        # jesli kolizja z przeszkoda
        if onTile != self.map.EMPTY:
            self.myTank.position = self.myTank.oldPos

        self.map.plane[
            self.myTank.oldPos[0], self.myTank.oldPos[1]] = self.map.EMPTY  # usuwanie czolgu ze starej pozycji
        self.map.plane[self.myTank.position[0], self.myTank.position[1]] = self.map.AGENT  # dodawanie czolgu

        self.map.tankRefresh(self.myTank, self.map.MY_TANK)

    def randomMove(self):

        for index, enemy in enumerate(self.myEnemies):
            if enemy.health > 0:  # gdy przeciwnik jeszcze żyje
                self.myEnemies[index].oldPos = self.myEnemies[index].position  # przepisuje starą pozycje
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
                    self.myEnemies[index].position = self.myEnemies[index].oldPos

                onTile = self.map.plane[
                    self.myEnemies[index].position[0], self.myEnemies[index].position[1]]  # co jest na danej plytce

                # jesli kolizja z przeszkoda
                if onTile != self.map.EMPTY:
                    self.myEnemies[index].position = self.myEnemies[index].oldPos
                else:  # aktualizuj tylko gdy zmiana
                    self.map.plane[self.myEnemies[index].oldPos[0], self.myEnemies[index].oldPos[
                        1]] = self.map.EMPTY  # usuwanie czolgu ze starej pozycji
                    self.map.plane[self.myEnemies[index].position[0], self.myEnemies[index].position[
                        1]] = self.map.ENEMY  # dodawanie czolgu
                    # wychodzneie poza mapę----------------------------------------------------------------
                    self.map.tankRefresh(self.myEnemies[index], 0)  # odświeża nową pozycję czołgu

    def bulletMove(self):

        if self.bullets:#jesli pociski istnieja
            for index,bullet in enumerate(self.bullets):
                #jesli nie pierwszy ruch pocisku:
                if bullet.motionCounter != 0: self.map.tileRefresh(bullet.position, self.map.EMPTY)

                bullet.motionCounter += 1
                bullet.move(1)

                # jesli pocisk nie wychodzi za self.map
                if not (bullet.position[0] < 0 or bullet.position[1] < 0 or \
                                bullet.position[1] >= self.map.HEIGHT or bullet.position[0] >= self.map.WIDTH):


                    onTile = self.map.plane[bullet.position[0], bullet.position[1]]  # co jest na danej plytce

                    if onTile == self.map.ENEMY:
                        for enemy in self.myEnemies:  # poszukiwanie właściwego wroga w tablicy
                            if enemy.position[0] == bullet.position[0] and enemy.position[1] == bullet.position[1]:
                                enemy.health -= bullet.health
                                if enemy.health <= 0:  # jesli wrog nie ma życia to usuwanie go z mapy
                                    self.map.plane[bullet.position[0], bullet.position[1]] = self.map.EMPTY
                                    self.map.tileRefresh(bullet.position, self.map.EMPTY)  # usuwanie pocisku z mapy
                        self.bullets.pop(index)

                    elif onTile == self.map.DESTR:
                        self.map.plane[bullet.position[0], bullet.position[1]] = self.map.EMPTY
                        self.map.tileRefresh(bullet.position, self.map.EMPTY)  # usuwanie pocisku z mapy z miejsca ściany
                        self.bullets.pop(index)  # usuwanie obiektu z tablicy
                    elif onTile == self.map.NONDESTR:
                        self.bullets.pop(index)  # usuwanie obiektu z tablicy
                    else:#nic nie stoi na drodze pocisku
                        self.map.tileRefresh(bullet.position,self.map.BULLET)
                        self.map.tileRefresh(bullet.oldPos, self.map.EMPTY)  # usuwanie pocisku z mapy

                else:#wychodzenie pocisku za mapę
                    self.bullets.pop(index)

if (__name__ == "__main__"):
    qApp = QApplication(sys.argv)
    app = TanksWindow()
    # app.map.toConsole()
    app.show()

    sys.exit(qApp.exec_())
