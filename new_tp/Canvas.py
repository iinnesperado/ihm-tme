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

        self.color = 0


    def reset(self):
        print("reset")

    def add_object(self):
        print("add object")

    def set_color(self, color ):
        print("set color")
        self.color = color
        self.colorChanged.emit(self.color)
    
    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(Qt.blue)
        # painter.drawRect(5,5,120,40)
        if self.pStart != None and self.pEnd != None :
            painter.drawRect(self.pStart.x(),self.pStart.y(),
                             self.pEnd.x()-self.pStart.x(),
                             self.pEnd.y()-self.pStart.y())
        painter.end()
        return
    
    def mousePressEvent(self, event):
        self.setMouseTracking(True)
        self.pStart = event.pos()
        self.update()
    
    def mouseReleaseEvent(self, event):
        self.pEnd = event.pos()
        self.setMouseTracking(False)
        self.pStart = None
        self.pEnd = None

    
    def mouseMoveEvent(self, event): 
        self.pEnd = event.pos()
        self.update()