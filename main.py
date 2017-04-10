from mapGenerator import mapGenerator
from tank import tank




if(__name__ == "__main__"):
    map = mapGenerator()
    map.generate()
    map.toConsole()

    myTank  = tank()
    print("rotacja: ", myTank.rotation)

    while True:

        oldTankPos = myTank.position
        map.plane[myTank.position[0], myTank.position[1]] = map.EMPTY  # usuwanie czolgu

        key = input()
        if key == 'w':
            myTank.move(1)

        elif key == 's':
            myTank.move(-1)

        elif key == 'a':
            myTank.rotate(-1)

        elif key == 'd':
            myTank.rotate(1)

        elif key == 'p':
            myTank.shoot()


        if myTank.position[0] < 0 or myTank.position[1] < 0 or myTank.position[0] >= map.HEIGHT or myTank.position[
            1] >= map.WIDTH:
            myTank.position = oldTankPos

        map.plane[myTank.position[0], myTank.position[1]] = map.AGENT  # dodawanie czolgu
        map.toConsole()

        print("rotacja: ",myTank.rotation)

