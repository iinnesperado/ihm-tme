from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *


class Canvas(QWidget):

    def __init__(self, parent = None):
        print("class Canvas")
        super().__init__()
        self.setMinimumSize(400,300)
        self.setMouseTracking(True)
        self.cursorPos = None
        self.pStart = None
        self.pEnd = None


    def reset(self):
        print("reset")

    def add_object(self):
        print("add object")

    def set_color(self, color ):
        print("set color")
    
    def paintEvent(self,event):
        painter = QPainter(self)
        # painter.setBrush(Qt.blue)
        # painter.drawRect(5,5,120,40)
        if self.cursorPos != None and self.pStart != None and self.pEnd != None :
            painter.drawRect(self.pStart.x(),self.pStart.y(),
                             self.pEnd.x()-self.pStart.x(),
                             self.pEnd.y()-self.pStart.y())
        painter.end()
        return
    
    def mousePressEvent(self, event):
        self.pStart = event.pos()
    
    def mouseReleaseEvent(self, event):
        self.pEnd = event.pos()
    
    def mouseMoveEvent(self, event): 
        self.cursorPos = event.pos()
        self.update()