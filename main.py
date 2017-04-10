from mapGenerator import MapGenerator
from tank import Tank

if (__name__ == "__main__"):
    map = MapGenerator()
    map.generate()
    map.toConsole()

    myTank = Tank()
    print("rotacja: ", myTank.rotation)

    while True:

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
            myTank.shoot()
            # while myTank.myBullet.exist:





        onTile = map.plane[myTank.position[0], myTank.position[1]]  # co jest na danej plytce

        # wychodzneie poza mapę i jesli kolizja z przeszkoda
        if myTank.position[0] < 0 or myTank.position[1] < 0 or myTank.position[0] >= map.HEIGHT or myTank.position[
            1] >= map.WIDTH or onTile != map.EMPTY:
            myTank.position = oldTankPos

        map.plane[oldTankPos[0], oldTankPos[1]] = map.EMPTY  # usuwanie czolgu ze starej pozycji
        map.plane[myTank.position[0], myTank.position[1]] = map.AGENT  # dodawanie czolgu

        map.toConsole()

        print("rotacja: ", myTank.rotation)
