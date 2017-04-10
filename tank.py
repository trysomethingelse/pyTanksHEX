import numpy as np
class tank:
    position = np.array([5,5])
    rotation = 0 #ktory ruch mozna wykonac znajdujacy sie w available 0-5

    availableMoveForEven = np.array([[-1,-1],[-2,0],[-1,0],[1,0],[2,0],[1,-1]])#dla przystych kolumn w tablicy
    availableMoveForOdd = np.array([[-1,0], [-2, 0], [-1, 1], [1, 1], [2, 0], [1, 0]])
    health = 100

    def rotate(self,value):#value 1 prawo, -1 lewo
        self.rotation += value
        if(self.rotation < 0):self.rotation = 5 #przekrecenie na drugą stronę
        self.rotation %= 6
        return True

    def move(self,direction): #direction 1-przód, -1 tył
        if self.position[1] % 2 == 0: #dla parzystych wierszy
            self.position = np.add(self.position,np.multiply(direction,self.availableMoveForEven[self.rotation]))
        else:
            self.position = np.add(self.position, np.multiply(direction, self.availableMoveForOdd[self.rotation]))

        return True
    def shoot(self):
        return True