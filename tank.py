import numpy as np
from PyQt5.QtCore import  QTimer


class MovableObject:
    ID = 0
    REALISTIC_MOVES_TIMEOUT = 500
    REALISTIC_MOVES_ON = True
    position = np.array([0, 0])  # pozycja czolgu na mapie
    oldPos = np.array([0, 0])
    rotation = 1  # ktory ruch mozna wykonac znajdujacy sie w available 0-5
    motionCounter = 0 #wykorzystywany dla pocisku, za pierwszym ruchem nie można czyścić płytki(pozycja czołgu)
    blockMotion = False #pozwala na bardziej rzeczywiste ruchy tzn. ograniczone czasowo

    availableMoveForEven = np.array(
        [[-1, -1], [0, -2], [0, -1], [0, 1], [0, 2], [-1, 1]])  # dla przystych kolumn w tablicy
    availableMoveForOdd = np.array([[0, -1], [0, -2], [1, -1], [1, 1], [0, 2], [0, 1]])
    health = 100
    realisticMovesTimer = QTimer()

    def __init__(self,health,realisticMovesOn):
        self.health = health
        if realisticMovesOn:
            self.realisticMovesTimer.timeout.connect(self.realisticMoves)
            self.realisticMovesTimer.start(self.REALISTIC_MOVES_TIMEOUT)
        self.REALISTIC_MOVES_ON = realisticMovesOn

    def rotate(self, value):  # value 1 prawo, -1 lewo
        if not self.blockMotion:
            self.rotation += value
            if (self.rotation < 0): self.rotation = 5  # przekrecenie na drugą stronę
            self.rotation %= 6
            if self.REALISTIC_MOVES_ON: self.blockMotion = True

    def move(self, direction):  # direction 1-przód, -1 tył
        if not self.blockMotion:
            if direction == -1:
                self.rotate(3)  # rotacja w przeciwna strone gdy cofanie
                self.blockMotion = False #odblokowanie możliwości natychmiastowego skrętu, zablokowana po pierwszym skrecie
            if self.position[1] % 2 == 0:  # dla parzystych wierszy
                self.position = np.add(self.position, self.availableMoveForEven[self.rotation])
            else:
                self.position = np.add(self.position, self.availableMoveForOdd[self.rotation])
            if direction == -1: self.rotate(3)  # przywrócenie poczatkowego ustawienia dla cofania
            if self.REALISTIC_MOVES_ON: self.blockMotion = True

    def realisticMoves(self):
        self.blockMotion = False