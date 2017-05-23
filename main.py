import numpy as np
from time import sleep
from random import randint

from mapGenerator import MapGenerator
from tank import MovableObject

from PyQt5.QtCore import QObject, Qt, QTimer,QElapsedTimer,QThread
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from xml.dom import minidom

import sys
import socket
import _thread
import time



class TanksWindow(QDialog):
    WINDOW_WIDTH = 620
    WINDOW_HEIGHT = 620
    SCENE_MARGIN = 20  # chroni przed wyświtlaniem scroll bar
    BULLET_HEALTH = 30
    TANK_HEALTH = 100
    REALISTIC_MOVES_ON = True
    REALISTIC_MOVES_OFF = False
    MY_TANK_ID = 1000

    myTank = MovableObject(TANK_HEALTH,REALISTIC_MOVES_ON)
    myEnemies = []  # tablica wrogów
    bullets = [] #tablica pociskow
    map = MapGenerator()
    randomMoveTimer = QTimer()
    bulletTimer = QTimer()
    globalTimer = QElapsedTimer() #czas od początku gry
    doc = minidom.Document()
    root = doc.createElement("mapHistory")
    sendThread = None


    #akcje:
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    SHOOT = 5



    def __init__(self,sendTcp):
        # while gamePause:
        #     pass
        self.map.generate()
        QMainWindow.__init__(self)
        self.ui = loadUi('./gui.ui', self)
        self.setWindowTitle('pyTanksHEX')
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.actualizeStatesFromMap()
        self.drawMap()

        # timery
        self.randomMoveTimer.timeout.connect(self.randomMove)
        self.randomMoveTimer.start(900)

        self.bulletTimer.timeout.connect(self.bulletMove)
        self.bulletTimer.start(30)

        self.globalTimer.start()
        self.sendThread = sendTcp #interfejs do wysyłania wiadomości na świat


    def actualizeStatesFromMap(self):  # aktualizuje pozycję obiektów na podstawie rozmieszczenia ich na mapie
        enemies = 0  # liczba wrogów
        for position, element in np.ndenumerate(self.map.plane):
            if int(element) == self.map.AGENT:
                self.myTank.oldPos = position
                self.myTank.position = position
                self.myTank.rotation = int((element%10)*10) #wyłuskanie dziesiętnych części
            elif int(element) == self.map.ENEMY:
                self.myEnemies.append(MovableObject(self.TANK_HEALTH,self.REALISTIC_MOVES_ON))  # dodanie kolejnego obiektu wroga
                self.myEnemies[enemies].position = position  # przypisz pozycje z mapy do zmiennych w obiekcie
                self.myEnemies[enemies].oldPos = position
                self.myEnemies[enemies].rotation = int((element%10)*10) #wyłuskanie dziesiętnych części
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


        self.map.planeToGraphics()#ładowanie układu płytek
        self.map.tankRefresh(self.myTank,self.map.MY_TANK)#ładowanie własnego czołgu
        for enemy in self.myEnemies: self.map.tankRefresh(enemy,self.map.NOT_MY_TANK)#ładowanie czołgów wroga

    def keyPressEvent(self, event):
        self.myTank.oldPos = self.myTank.position  # przepisz pozycje przed aktualizacja

        if event.key() == Qt.Key_W:
            self.myTank.move(1)
            self.addActionToHistory(self.FORWARD,self.MY_TANK_ID)
        elif event.key() == Qt.Key_S:
            self.myTank.move(-1)
            self.addActionToHistory(self.BACKWARD,self.MY_TANK_ID)
        elif event.key() == Qt.Key_A:
            self.myTank.rotate(-1)
            self.addActionToHistory(self.LEFT,self.MY_TANK_ID)
        elif event.key() == Qt.Key_L:#zapisanie gry
            self.saveDataToXML()
        elif event.key() == Qt.Key_O:  # odtworzenie zapisanej gry
            self.readHistory()
        elif event.key() == Qt.Key_D:
            self.myTank.rotate(1)
            self.addActionToHistory(self.RIGHT,self.MY_TANK_ID)
        elif event.key() == Qt.Key_X:#strzał
            self.bullets.append(MovableObject(self.BULLET_HEALTH,self.REALISTIC_MOVES_OFF))#ustawienie opóźnienia realistycznosci na 0
            self.bullets[-1].position = self.myTank.position  # pozycja pocisku to pozycja czolgu
            self.bullets[-1].rotation = self.myTank.rotation
            self.addActionToHistory(self.SHOOT, self.MY_TANK_ID)

        self.moveValidation(self.myTank)

        self.map.plane[
            self.myTank.oldPos[0], self.myTank.oldPos[1]] = self.map.EMPTY  # usuwanie czolgu ze starej pozycji
        self.map.plane[self.myTank.position[0], self.myTank.position[1]] = self.map.AGENT  # dodawanie czolgu

        self.map.tankRefresh(self.myTank, self.map.MY_TANK)
    def moveValidation(self,tank):
        # wychodzneie czołgu poza mapę
        if tank.position[0] < 0 or tank.position[1] < 0 or tank.position[1] >= self.map.HEIGHT or \
                        tank.position[
                            0] >= self.map.WIDTH:
            tank.position = tank.oldPos
        onTile = self.map.plane[tank.position[0], tank.position[1]]  # co jest na danej plytce
        # jesli kolizja z przeszkoda
        if onTile != self.map.EMPTY:
            tank.position = tank.oldPos

    def randomMove(self):

        for index, enemy in enumerate(self.myEnemies):
            if enemy.health > 0:  # gdy przeciwnik jeszcze żyje
                self.myEnemies[index].oldPos = self.myEnemies[index].position  # przepisuje starą pozycje

                #losowanie ruchi

                if randint(1, 10) > 3: #obrót
                    rotation = randint(-1,1)
                    rotationDone = self.LEFT #potrzebne do przekazania odpowiedniego obrotu do XML
                    self.myEnemies[index].rotate(rotation)
                    if rotation == -1: rotationDone = self.LEFT
                    elif rotation == 1: rotationDone = self.RIGHT
                    if rotation != 0 : #jesli wykonano jakikolwiek obrot to go zapisz do XML
                        self.addActionToHistory(rotationDone,index)
                else: #ruch w przód lub tył
                    direction = randint(0, 7)
                    moveDone = self.FORWARD#potrzebne do przekazania odpowiedniego ruchu do XML
                    if direction == 0:
                        direction = -1  # wartosc do tyłu to -1 w metodzie czołgu
                    else:
                        direction = 1
                    self.myEnemies[index].move(direction)
                    if direction == -1 : moveDone = self.BACKWARD
                    elif direction == 1 : moveDone = self.FORWARD
                    self.addActionToHistory(moveDone, index)

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

                    if int(onTile) == self.map.ENEMY:
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
#obsluga XML ....................................................................................................
    def playHistory(self):
        doc = minidom.parse("data.xml")
    def saveDataToXML(self):
        self.doc.writexml(open('data.xml', 'w'),
                          indent="  ",
                          addindent="  ",
                          newl='\n')
    def addActionToHistory(self,action,tankID):
        if self.sendThread.connected:
            self.sendThread.sendMessage(str(action)+","+str(tankID))#wysyła wykonany ruch w sieć

        moment = self.doc.createElement("moment")
        moment.setAttribute("time",str(self.globalTimer.elapsed()))
        dataString = str(action) + " " +  str(tankID)
        nodeText = self.doc.createTextNode(dataString)
        moment.appendChild(nodeText)
        self.root.appendChild(moment)
        self.doc.appendChild(self.root)


    def readHistory(self):
        print("podróż w czasie")
        self.globalTimer.restart()#zerowanie globalnego timera
        doc = minidom.parse('data.xml')
        docNodes = doc.childNodes
        for element in docNodes[0].getElementsByTagName("moment"):
            timeRead = element.attributes["time"]
            print("Czas: ",timeRead.value)
            values = element.firstChild.nodeValue#weź tekst pomiędzy znacznikami
            values = values.split(' ')#rozdziel ten tekst na osobne komórki
            values[0] = int(values[0])#akcja
            values[1] = int(values[1])#swój czy wróg

            print("wartosci: ",values)

            while int(self.globalTimer.elapsed()) < int(timeRead.value):#dopóki nie ma czasu który był zapisany w pliku to czekaj na ten czas
                sleep(0.001)
            if values[1] == self.MY_TANK_ID:#swój
                 if values[0] == self.FORWARD: self.myTank.move(1)
                 elif values[0] == self.BACKWARD: self.myTank.move(-1)
                 elif values[0] == self.LEFT:
                     self.myTank.rotate(-1)
                 elif values[0] == self.RIGHT:
                     self.myTank.rotate(1)
                 self.moveValidation(self.myTank)
                 self.map.plane[
                    self.myTank.oldPos[0], self.myTank.oldPos[1]] = self.map.EMPTY  # usuwanie czolgu ze starej pozycji
                 self.map.plane[self.myTank.position[0], self.myTank.position[1]] = self.map.AGENT  # dodawanie czolgu

                 # self.myTank.position = [3,3]
                 self.map.tankRefresh(self.myTank, self.map.MY_TANK)
                 self.mapScene.update()
                 self.ui.graphicsView.update()

class ServerThread(QThread):
    toSend = "wysylanie"
    TCP_IP = '127.0.0.1'#''153.19.215.253'
    TCP_PORT = 50001
    BUFFER_SIZE = 1024

    def __init__(self,mainApp):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):

        sRx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sRx.bind((self.TCP_IP, self.TCP_PORT))
        sRx.listen(1)

        while 1:
            self.server(sRx)
            pass

    def server(self,s):
        print("Wątek serwera działa!")
        conn, addr = s.accept()
        print("Connection address:", addr)
        while 1:
            data = conn.recv(self.BUFFER_SIZE)
            if not data: break
            print("received data:", data.decode())

        conn.close()

    def send(data):
        TCP_IP_SEND = '127.0.0.1'#'153.19.215.253'
        TCP_PORT_SEND = 50001
        print("wysylanie")
        sTx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sTx.connect((TCP_IP_SEND, TCP_PORT_SEND))
        for elem in data:
            sTx.send(str.encode(elem))
            time.sleep(2)


class SendThread(QThread):
    TCP_IP_SEND = '127.0.0.1'#'153.19.215.253'
    TCP_PORT_SEND = 50002
    sTx = None
    connected = False

    def __init__(self):
        QThread.__init__(self)



    def __del__(self):
        self.wait()

    def run(self):

        # self.sTx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sTx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while not self.connected:
            try:
                self.sTx.connect((self.TCP_IP_SEND, self.TCP_PORT_SEND))
                self.connected = True
            except Exception as e:
                pass
        print("Wątek wysyłania działa!")
        while True:
            pass

    def sendMessage(self,message):
        self.sTx.send(str.encode(message))

if (__name__ == "__main__"):


    sendThread = SendThread()
    sendThread.start()

    qApp = QApplication(sys.argv)
    app = TanksWindow(sendThread)

    serverThread = ServerThread(app)
    serverThread.start()

    app.show()
    sys.exit(qApp.exec_())




