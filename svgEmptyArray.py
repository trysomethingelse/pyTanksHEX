from PyQt5 import QtSvg
WIDHT = 10
class
def svgEmpty(width,height):
    return [[QtSvg.QSvgWidget() for i in range(0, height)] for j in range(0, width)]