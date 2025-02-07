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

        self.offset = QPoint(0,0)
        self.lastPos = None

        self.cur_obj = None

        self.free_drawings = [] 
        self.current_path = None


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
        if self.mode == "move":
            painter.translate(self.offset)
            

        if self.cur_obj is not None: # pour changer la forme selectionnée
            i = self.cur_obj
            self.obj[i][3] = QColor(self.colorPen)
            self.obj[i][4] = QColor(self.colorBrush)
            pen = QPen(Qt.DashLine)
            pen.setColor(QColor(self.colorPen))
            painter.setPen(pen)  
            painter.setBrush(QColor(self.colorBrush))
            if self.obj[i][0] == "rectangle":
                painter.drawRect(QRect(self.obj[i][1], self.obj[i][2]))
            elif self.obj[i][0] == "ellipse":
                painter.drawEllipse(QRect(self.obj[i][1], self.obj[i][2]))
            
        
        for o in self.obj: # pour redessiner les formes deja dessinées
            shape, pStart, pEnd, colorPen, colorBrush = o
            if self.mode == "select":
                if o == self.obj[self.cur_obj]:
                    continue
            painter.setPen(QColor(colorPen))
            painter.setBrush(QColor(colorBrush)) if colorBrush != 0 else painter.setBrush(Qt.NoBrush)
            if shape == "rectangle":
                painter.drawRect(QRect(pStart, pEnd))
            elif shape == "ellipse":
                painter.drawEllipse(QRect(pStart, pEnd))
        
        for path, colorPen in self.free_drawings:  # Dessiner tous les anciens tracés
            painter.setPen(QColor(colorPen))
            for i in range(1, len(path)):
                painter.drawLine(path[i - 1], path[i])
        
        if self.mode == "draw":
            if self.pStart and self.pEnd: # pour dessiner la forme en cours
                painter.setPen(QColor(self.colorPen))
                painter.setBrush(QColor(self.colorBrush)) if self.colorBrush != 0 else painter.setBrush(Qt.NoBrush)
                if self.shape == "rectangle":
                    painter.drawRect(QRect(self.pStart, self.pEnd))
                elif self.shape == "ellipse":
                    painter.drawEllipse(QRect(self.pStart, self.pEnd))
            elif self.shape == "free" and self.current_path:
                painter.setPen(QColor(self.colorPen))
                for i in range(1, len(self.current_path)):
                    painter.drawLine(self.current_path[i - 1], self.current_path[i])
            

        painter.end()
    
    def setMode(self, mode:str):
        self.mode = mode

    def mousePressEvent(self, event):
        self.setMouseTracking(True)
        if self.mode == "move":
            self.lastPos = event.pos()
        elif self.mode == "draw":
            if self.shape == "free":
                self.current_path = [event.pos()]
            else:
                self.pStart = event.pos()
        elif self.mode == "select":
            self.cur_obj = None
            for i, (_, pStart, pEnd, _, _) in enumerate(self.obj):
                r = QRect(pStart, pEnd)
                if r.contains(event.pos()):
                    self.cur_obj = i
                    print("selected ", self.obj[i])
                    break
        self.update()
    
    def mouseReleaseEvent(self, event):
        if self.mode == "move":
            self.lastPos = None
        elif self.mode == "draw":
            if self.current_path and self.shape == "free":
                self.free_drawings.append((self.current_path, self.colorPen))  # Sauvegarde le tracé
                self.current_path = None
            else:
                self.pEnd = event.pos()
                self.setMouseTracking(False)
                self.obj.append([self.shape,self.pStart, self.pEnd,self.colorPen,self.colorBrush])
                self.pStart = None
                self.pEnd = None
            
        self.setMouseTracking(False)
        self.update()

    
    def mouseMoveEvent(self, event): 
        if self.mode == "move" and self.lastPos:
            pos = event.pos() - self.lastPos
            #self.offset += event.pos() - self.lastPos
            self.lastPos = event.pos()
            self.obj = [[shape, pStart + pos, pEnd + pos, colorPen, colorBrush] 
                    for shape, pStart, pEnd, colorPen, colorBrush in self.obj]
            self.free_drawings = [( [p + pos for p in path], colorPen)  
                              for path, colorPen in self.free_drawings]
        elif self.mode == "draw":
            if self.shape == "free":
                self.current_path.append(event.pos()) 
            else:
                self.pEnd = event.pos()
        self.update()