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
        self.lastPoint = None

        self.pPrevious = None
        self.pCurrent = None
        self.cur_obj = None

        self.free_drawings = [] 
        self.current_path = None

        self.lasso = QPolygon()
        self.laso_selection =  False


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
    
    def setMode(self, mode:str):
        self.mode = mode
    
    def clearCanvas(self):
        self.obj = []
        self.lasso = QPolygon()
        self.lasso_selection = False
        self.update()
    
    #### paint event
    def paintEvent(self,event):
        painter = QPainter(self)
        if self.mode == "move":
            painter.translate(self.offset)

        if self.cur_obj is not None: # pour changer la forme selectionnée
            self.obj[self.cur_obj][3] = QColor(self.colorPen)
            self.obj[self.cur_obj][4] = QColor(self.colorBrush)
            self.obj[self.cur_obj][0] = self.shape
            
        
        for o in self.obj: # pour redessiner les formes deja dessinées
            shape, pStart, pEnd, colorPen, colorBrush = o
            painter.setPen(QColor(colorPen))
            painter.setBrush(QColor(colorBrush)) if colorBrush != 0 else painter.setBrush(Qt.NoBrush)
            if shape == "rectangle":
                painter.drawRect(QRect(pStart, pEnd))
            elif shape == "ellipse":
                painter.drawEllipse(QRect(pStart, pEnd))
            elif shape == "free":
                painter.drawPoint(pEnd)
        
        if self.mode == "draw" :
            if  self.pStart and self.pEnd : # pour dessiner la forme en cours
                painter.setPen(QColor(self.colorPen))
                painter.setBrush(QColor(self.colorBrush)) if self.colorBrush != 0 else painter.setBrush(Qt.NoBrush)
                if self.shape == "rectangle":
                    painter.drawRect(QRect(self.pStart, self.pEnd))
                elif self.shape == "ellipse":
                    painter.drawEllipse(QRect(self.pStart, self.pEnd))
                elif self.shape == "free" and self.current_path:
                    # painter.setPen(QColor(self.colorPen))
                    for i in range(1, len(self.current_path)):
                        painter.drawLine(self.current_path[i - 1], self.current_path[i])
            
        elif self.mode == "lasso":
            painter.setPen(Qt.gray)
            painter.setPen(Qt.DashLine)
            if not self.lasso.isEmpty():
                painter.drawPolygon(self.lasso)

        painter.end()

    #### mouse events
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
        '''elif self.mode == "lasso":
            self.lasso.append(event.pos())'''
        self.update()
    
    def mouseReleaseEvent(self, event):
        if self.mode == "move":
            self.lastPos = None
        elif self.mode == "draw":
            self.pEnd = event.pos()
            #self.setMouseTracking(False)
            self.obj.append([self.shape,self.pStart, self.pEnd,self.colorPen,self.colorBrush])
            self.pStart = None
            self.pEnd = None
            if self.current_path and self.shape == "free":
                self.free_drawings.append((self.current_path, self.colorPen, self.colorBrush))  # Sauvegarde le tracé
                self.current_path = None
        self.update()

    
    def mouseMoveEvent(self, event): 
        if self.mode == "move" and self.lastPos:
            pos = event.pos() - self.lastPos
            #self.offset += event.pos() - self.lastPos
            self.lastPos = event.pos()
            self.obj = [[shape, pStart + pos, pEnd + pos, colorPen, colorBrush] 
                    for shape, pStart, pEnd, colorPen, colorBrush in self.obj]
        elif self.mode == "draw":
            if self.shape == "free":
                self.current_path.append(event.pos()) 
            else:
                self.pEnd = event.pos()

        self.update()