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
        QMainWindow.__init__(self)
        self.ui = loadUi('./gui.ui',self)
        self.setWindowTitle('pyTanksHEX')
        self.resize(self.WINDOW_WIDTH,self.WINDOW_HEIGHT)

    def drawMap(self):
        [startX,startY] = [-self.WINDOW_WIDTH/2,-self.WINDOW_HEIGHT/2]


        mapScene = QGraphicsScene(startX+self.SCENE_MARGIN,startY+self.SCENE_MARGIN,self.WINDOW_WIDTH-self.SCENE_MARGIN,self.WINDOW_HEIGHT-self.SCENE_MARGIN)
        map.startX = -mapScene.width()/2
        map.startY = -mapScene.height()/2


        self.ui.graphicsView.setGeometry(0,0,self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        self.map.graphicMap(mapScene)
        self.ui.graphicsView.setScene(mapScene)
        map.planeToGraphics()

    def keyPressEvent(self, event):
        self.myTank.oldTankPos = self.myTank.position # przepisz pozycje przed aktualizacja

        if event.key() == Qt.Key_W:
            self.myTank.move(1)
            # map.changeTile(self.myTank.position[0],self.myTank.position[1])


        # wychodzneie poza mapę
        if self.myTank.position[0] < 0 or self.myTank.position[1] < 0 or self.myTank.position[0] >= self.map.HEIGHT or self.myTank.position[
            1] >= self.map.WIDTH:
            self.myTank.position = self.myTank.oldTankPos

        onTile = self.map.plane[self.myTank.position[0], self.myTank.position[1]]  # co jest na danej plytce

        # jesli kolizja z przeszkoda
        # if onTile != self.map.EMPTY:
        #     self.myTank.position =  self.myTank.oldTankPos


        self.map.plane[self.myTank.oldTankPos[0],  self.myTank.oldTankPos[1]] = self.map.EMPTY  # usuwanie czolgu ze starej pozycji
        self.map.plane[self.myTank.position[0], self.myTank.position[1]] = self.map.AGENT  # dodawanie czolgu

        print(self.myTank.position)

        map.planeToGraphics()
        # print("rotacja: ", myTank.rotation)



if (__name__ == "__main__"):


    map = MapGenerator()
    map.generate()

    # map.toConsole()
    #gui
    qApp = QApplication(sys.argv)
    app = TanksWindow()
    app.map = map
    svgTiles = app.drawMap()

    # map.planeToGraphics(svgTiles)


    app.show()
    sys.exit(qApp.exec_())
    #koniec gui






    myTank = Tank()
    print("rotacja: ", myTank.rotation)

    while False:

        oldTankPos = myTank.position

        key = input()
        if key == 'w':
            myTank.move(1)

        elif key == 's':
            myTank.move(-1)

        elif key == 'a':
            myTank.rotate(-1)

        elif key == 'd':
            myTank.rotate(1)

        elif key == 'x':
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







