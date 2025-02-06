from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *


class Canvas(QWidget):
    colorChanged = Signal()

    def __init__(self, parent = None):
        print("class Canvas")
        super().__init__()
        self.setMinimumSize(400,300)
        self.pStart = None
        self.pEnd = None
        self.colorPen = 0
        self.colorBrush = 0
        self.shape = "rectangle"
        self.obj = [] # (forme, coord, couleurpen, couleur brush)
        self.mode = "draw"


    def reset(self):
        print("reset")

    def add_object(self, obj:str):
        print("add object")
        self.shape=obj


    def set_colorPen(self, color):
        print("set color")
        self.colorPen = color

    def set_colorBrush(self, color):
        print("set color")
        self.colorBrush = color
    
    def paintEvent(self,event):
        painter = QPainter(self)
        for o in self.obj: # pour redessiner les formes deja dessinées
                shape, pStart, pEnd, colorPen, colorBrush = o
                painter.setPen(QColor(colorPen))
                painter.setBrush(QColor(colorBrush)) if colorBrush != 0 else painter.setBrush(Qt.NoBrush)
                if shape == "rectangle":
                    painter.drawRect(QRect(pStart, pEnd))
                elif shape == "ellipse":
                    painter.drawEllipse(QRect(pStart, pEnd))
        
        '''switch self.mopde : # TODO resoudre problème avec le switch
            case "draw":'''
        if self.pStart and self.pEnd : # pour dessiner la forme en cours
            painter.setPen(QColor(self.colorPen))
            painter.setBrush(QColor(self.colorBrush)) if self.colorBrush != 0 else painter.setBrush(Qt.NoBrush)
            if self.shape == "rectangle":
                painter.drawRect(QRect(self.pStart, self.pEnd))
            elif self.shape == "ellipse":
                painter.drawEllipse(QRect(self.pStart, self.pEnd))
            '''case "move":
                painter.translate(60,60)'''
            

        painter.end()
    
    def setMode(self, mode:str):
        self.mode = mode

    def mousePressEvent(self, event):
        self.setMouseTracking(True)
        self.pStart = event.pos()
        self.update()
    
    def mouseReleaseEvent(self, event):
        self.pEnd = event.pos()
        self.setMouseTracking(False)
        self.obj.append((self.shape,self.pStart, self.pEnd,self.colorPen,self.colorBrush))
        self.pStart = None
        self.pEnd = None

    
    def mouseMoveEvent(self, event): 
        self.pEnd = event.pos()
        self.update()