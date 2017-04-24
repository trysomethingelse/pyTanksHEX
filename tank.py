import numpy as np


class MovableObject:
    position = np.array([0, 0])  # pozycja czolgu na mapie
    oldTankPos = np.array([0, 0])
    rotation = 1  # ktory ruch mozna wykonac znajdujacy sie w available 0-5

    availableMoveForEven = np.array(
        [[-1, -1], [0, -2], [0, -1], [0, 1], [0, 2], [-1, 1]])  # dla przystych kolumn w tablicy
    availableMoveForOdd = np.array([[0, -1], [0, -2], [1, -1], [1, 1], [0, 2], [0, 1]])
    health = 100


    def rotate(self, value):  # value 1 prawo, -1 lewo
        self.rotation += value
        if (self.rotation < 0): self.rotation = 5  # przekrecenie na drugą stronę
        self.rotation %= 6
        return True

    def move(self, direction):  # direction 1-przód, -1 tył
        if direction == -1: self.rotate(3)  # rotacja w przeciwna strone gdy cofanie
        if self.position[1] % 2 == 0:  # dla parzystych wierszy
            self.position = np.add(self.position, self.availableMoveForEven[self.rotation])
        else:
            self.position = np.add(self.position, self.availableMoveForOdd[self.rotation])
        if direction == -1: self.rotate(3)  # przywrócenie poczatkowego ustawienia

        return True


class Bullet(MovableObject):
    position = np.array([0, 0])
    rotation = 0
    exist = False
    health = 30