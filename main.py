from mapGenerator import MapGenerator
from tank import Tank,Bullet

from PyQt5.QtCore import QObject,Qt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore,QtSvg

import sys


class TanksWindow(QDialog):
    WINDOW_WIDTH = 620
    WINDOW_HEIGHT = 620
    SCENE_MARGIN = 20 #chroni przed wyświtlaniem scroll bar
    myTank = Tank()
    map = MapGenerator()



    def __init__(self):
        self.map.generate()
        QMainWindow.__init__(self)
        self.ui = loadUi('./gui.ui',self)
        self.setWindowTitle('pyTanksHEX')
        self.resize(self.WINDOW_WIDTH,self.WINDOW_HEIGHT)

    def drawMap(self):
        [startX,startY] = [-self.WINDOW_WIDTH/2,-self.WINDOW_HEIGHT/2]


        self.mapScene = QGraphicsScene(startX+self.SCENE_MARGIN,startY+self.SCENE_MARGIN,self.WINDOW_WIDTH-self.SCENE_MARGIN,self.WINDOW_HEIGHT-self.SCENE_MARGIN)
        self.map.startX = -self.mapScene.width()/2
        self.map.startY = -self.mapScene.height()/2


        self.ui.graphicsView.setGeometry(0,0,self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        self.map.graphicMap(self.mapScene)
        self.ui.graphicsView.setScene(self.mapScene)
        self.map.planeToGraphics(self.myTank)

    def keyPressEvent(self, event):
        self.myTank.oldTankPos = self.myTank.position # przepisz pozycje przed aktualizacja

        if event.key() == Qt.Key_W:
            self.myTank.move(1)
        elif event.key() == Qt.Key_S:
            self.myTank.move(-1)
        elif event.key() == Qt.Key_A:
            self.myTank.rotate(-1)
        elif event.key() == Qt.Key_D:
            self.myTank.rotate(1)
        elif event.key() == Qt.Key_X:
            # myTank.shoot()
            myBullet = Bullet()
            myBullet.position = myTank.position  # pozycja pocisku to pozycja czolgu
            myBullet.rotation = myTank.rotation
            myBullet.exist = True

            while myBullet.exist:
                myBullet.move(1)
                #jesli pocisk wychodzi za mape
                if myBullet.position[0] < 0 or myBullet.position[1] < 0 or \
                    myBullet.position[0] >= map.HEIGHT or myBullet.position[1] >= map.WIDTH:

                    myBullet.exist = False
                    continue


                onTile = map.plane[myBullet.position[0], myBullet.position[1]]  # co jest na danej plytce

                if onTile == map.ENEMY:
                    map.plane[myBullet.position[0], myBullet.position[1]] = 0
                    myBullet.exist = False
                elif onTile == map.DESTR:
                    map.plane[myBullet.position[0], myBullet.position[1]] = 0
                    myBullet.exist = False
                elif onTile == map.NONDESTR:
                    myBullet.exist = False


        # wychodzneie poza mapę
        if self.myTank.position[0] < 0 or self.myTank.position[1] < 0 or self.myTank.position[1] >= self.map.HEIGHT or self.myTank.position[
            0] >= self.map.WIDTH:
            self.myTank.position = self.myTank.oldTankPos

        onTile = self.map.plane[self.myTank.position[0], self.myTank.position[1]]  # co jest na danej plytce

        # jesli kolizja z przeszkoda
        if onTile != self.map.EMPTY:
            self.myTank.position =  self.myTank.oldTankPos


        self.map.plane[self.myTank.oldTankPos[0],  self.myTank.oldTankPos[1]] = self.map.EMPTY  # usuwanie czolgu ze starej pozycji
        self.map.plane[self.myTank.position[0], self.myTank.position[1]] = self.map.AGENT  # dodawanie czolgu

        print(self.myTank.position)

        # self.map.planeToGraphics(self.myTank)#aktualizacja grafiki
        self.map.myTankRefresh(self.myTank)



if (__name__ == "__main__"):

    qApp = QApplication(sys.argv)
    app = TanksWindow()
    app.drawMap()
    app.show()
    sys.exit(qApp.exec_())










