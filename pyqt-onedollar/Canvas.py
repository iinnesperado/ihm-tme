from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from onedollar import OneDollar
import numpy as np


def points_to_qpolygonF(points):
    polygon = QPolygonF()
    for elem in points:
        polygon.append( QPoint(elem[0], elem[1]) )
    return polygon

def qpolygonF_to_points(polygon):
    points = []
    for elem in polygon:
        points.append( [ elem.x(), elem.y() ] )
    return points


class Canvas(QWidget):


    ##########################
    # TODO 9: create a selected_template signal with three parameters: label, template_id, score
    ##########################

    selected_template = Signal(str, int, float)


    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setMinimumSize(600, 600)
        self.oneDollar = OneDollar()            #create a $1 recognizer

        self.path = QPolygonF()                 #user path
        self.feedback = QPolygonF()             #used for displaying the animated feedback trace
        self.termination = QPolygonF()          #recognized gesture

        self.animation = False

        #############################
        # TODO 11 create a timer
        # connect the timer to the sole timout
        #############################

        self.timer = QTimer(self)
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.timeout)




    ##############################
    def paintEvent(self, QPaintEvent):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        if self.animation == True:
            if self.feedback != QPolygonF():
                p.setPen(Qt.blue)
                p.setBrush(Qt.blue)
                p.drawPolyline(self.feedback)
                p.drawEllipse(self.feedback[0], 2, 2)
        else:

            if self.path != QPolygonF() and self.path.size() > 1:
                p.setPen(Qt.blue)
                p.setBrush(Qt.blue)
                p.drawPolyline(self.path)
                p.drawEllipse(self.path[0], 2, 2)

            if self.termination != QPolygonF() and self.termination.size() > 1:
                p.setPen(Qt.red)
                p.setBrush(Qt.red)
                p.drawPolyline(self.termination)
                p.drawEllipse(self.termination[0], 2, 2)


    ############################
    #TODO 11 create the animation
    ############################
    def timeout(self):
        self.animation = True       #used in paintEvent to know whether it displays the traces or the animated feedback
        nb_step = 100

        if self.counter > nb_step:
            self.timer.stop()
            self.counter
            self.animation = False
            return

        alpha = self.counter/nb_step
        #todo 11
        new_points = QPolygonF()
        for p1, p2 in zip(self.path, self.termination):
            x = p1.x() * (1-alpha) + p2.x() * alpha
            y = p1.y() * (1-alpha) + p2.y() * alpha
            new_points.append(QPoint(x, y))
        self.feedback = new_points


        self.counter += 1
        self.repaint()


    ############################
    # return a QPolygon located in the surrunding of the executed gesture
    ###########################
    def get_feedback(self, template_id):
        gesture = self.oneDollar.resampled_gesture
        template = self.oneDollar.resampled_templates[template_id]

        c_g = np.mean(gesture, 0)
        c_t = np.mean(template, 0)
        g0 = gesture[0]
        t0 = template[0]
        line_g = QLineF(QPoint(c_g[0], c_g[1]), QPoint(g0[0], g0[1]))
        line_t = QLineF(QPoint(c_t[0], c_t[1]), QPoint(t0[0], t0[1]))
        angle = line_g.angleTo(line_t) * 3.14 / 180
        res = self.oneDollar.rotateBy(template, angle)

        c_t = np.mean(res, 0)

        max_gx, max_gy = np.max(gesture, 0)
        min_gx, min_gy = np.min(gesture, 0)
        gb_height = max_gy - min_gy

        max_tx, max_ty = np.max(res, 0)
        min_tx, min_ty = np.min(res, 0)
        tb_height = max_ty - min_ty

        scale = gb_height / tb_height
        newPoints = np.zeros((1, 2))
        for point in res:
            q = np.array([0., 0.])
            q[0] = point[0] * scale
            q[1] = point[1] * scale
            newPoints = np.append(newPoints, [q], 0)
        res = newPoints[1:]
        c_t = np.mean(res, 0)
        res = self.oneDollar.translate(res, [c_g[0] - c_t[0], c_g[1] - c_t[1]])
        termination = points_to_qpolygonF(res)

        return termination


    #############################
    # TODO 10 and 11
    #############################
    def display_feedback(self, template_id):

        #todo 10
        self.termination = self.get_feedback(template_id)

        #todo 11
        self.path = points_to_qpolygonF(self.oneDollar.resampled_gesture)
        self.feedback = QPolygonF(self.path)

        #create a timer
        self.counter = 0
        self.animation = True


    ##############################
    def recognize_gesture(self):
        points = qpolygonF_to_points(self.path)
        template_id, label, score = self.oneDollar.recognize(points)
        print("template id: ", template_id, " label: ", label, " score: ", score)

        if score > 0.5:
            self.selected_template.emit(label, template_id, score)
            self.display_feedback(template_id)
        self.timer.start()


    ##############################
    def clear(self):
        self.path = QPolygonF()
        self.feedback = QPolygonF()
        self.termination = QPolygonF()

    ##############################
    def mousePressEvent(self,e):
        self.clear()
        self.path.append( e.pos() )
        self.repaint()

    ##############################
    def mouseMoveEvent(self, e):
        self.path.append( e.pos() )
        self.repaint()

    ##############################
    def mouseReleaseEvent(self, e):
        if self.path.size() > 10:
            self.recognize_gesture()
        else:
            print("not enough points")

        self.repaint()
