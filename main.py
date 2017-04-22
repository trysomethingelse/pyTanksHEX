from mapGenerator import MapGenerator
from tank import Tank,Bullet

from PyQt5.QtCore import QObject
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore,QtSvg

import sys


class TanksWindow(QDialog):
    WINDOW_WIDTH = 620
    WINDOW_HEIGHT = 620
    SCENE_MARGIN = 20 #chroni przed wyświtlaniem scroll bar

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi('./gui.ui',self)
        self.setWindowTitle('pyTanksHEX')
        self.resize(self.WINDOW_WIDTH,self.WINDOW_HEIGHT)

    def drawMap(self,map):
        [startX,startY] = [-self.WINDOW_WIDTH/2,-self.WINDOW_HEIGHT/2]


        mapScene = QGraphicsScene(startX+self.SCENE_MARGIN,startY+self.SCENE_MARGIN,self.WINDOW_WIDTH-self.SCENE_MARGIN,self.WINDOW_HEIGHT-self.SCENE_MARGIN)
        self.ui.graphicsView.setGeometry(0,0,self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        map.graphicMap(mapScene)
        self.ui.graphicsView.setScene(mapScene)



if (__name__ == "__main__"):


    map = MapGenerator()
    map.generate()
    # map.toConsole()
    #gui
    qApp = QApplication(sys.argv)
    app = TanksWindow()
    app.drawMap(map)
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







        # wychodzneie poza mapę
        if myTank.position[0] < 0 or myTank.position[1] < 0 or myTank.position[0] >= map.HEIGHT or myTank.position[
            1] >= map.WIDTH:
            myTank.position = oldTankPos

        onTile = map.plane[myTank.position[0], myTank.position[1]]  # co jest na danej plytce

        # jesli kolizja z przeszkoda
        if onTile != map.EMPTY:
            myTank.position = oldTankPos


        map.plane[oldTankPos[0], oldTankPos[1]] = map.EMPTY  # usuwanie czolgu ze starej pozycji
        map.plane[myTank.position[0], myTank.position[1]] = map.AGENT  # dodawanie czolgu

        map.toConsole()

        print("rotacja: ", myTank.rotation)
