import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Canvas import *
import resources

class MainWindow(QMainWindow):

    def __init__(self, parent = None ):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("Untitled")
        print("init mainwindow")
        self.resize(600, 500)
        
        self.canva = Canvas()
        self.textEdit = QTextEdit(self)

        layout = QVBoxLayout()
        layout.addWidget(self.canva)
        layout.addWidget(self.textEdit)
        window = QWidget()
        window.setLayout(layout)
        self.setCentralWidget(window)

        bar = self.menuBar()
        self.fileMenu = bar.addMenu("File")

        colorMenu = bar.addMenu("Color")
        self.open()
        self.save()
        self.quit()

        actPen = colorMenu.addAction(QIcon(":/icons/pen.png"), "&Pen color", self.pen_color, QKeySequence("Ctrl+P"))
        actBrush = colorMenu.addAction(QIcon(":/icons/brush.png"), "&Brush color", self.brush_color, QKeySequence("Ctrl+B"))

        colorToolBar = QToolBar("Color")
        self.addToolBar( colorToolBar )
        colorToolBar.addAction( actPen )
        colorToolBar.addAction( actBrush )

        shapeMenu = bar.addMenu("Shape")
        actRectangle = shapeMenu.addAction(QIcon(":/icons/rectangle.png"), "&Rectangle", self.rectangle )
        actEllipse = shapeMenu.addAction(QIcon(":/icons/ellipse.png"), "&Ellipse", self.ellipse)
        actFree = shapeMenu.addAction(QIcon(":/icons/free.png"), "&Free drawing", self.free_drawing)

        shapeToolBar = QToolBar("Shape")
        self.addToolBar( shapeToolBar )
        shapeToolBar.addAction( actRectangle )
        shapeToolBar.addAction( actEllipse )
        shapeToolBar.addAction( actFree )

        modeMenu = bar.addMenu("Mode")
        actMove = modeMenu.addAction(QIcon(":/icons/move.png"), "&Move", self.move)
        actDraw = modeMenu.addAction(QIcon(":/icons/draw.png"), "&Draw", self.draw)
        actSelect = modeMenu.addAction(QIcon(":/icons/select.png"), "&Select", self.select)
        actLasso = modeMenu.addAction(QIcon(":/icons/lasso.png"), "&Lasso", self.lasso)

        modeToolBar = QToolBar("Navigation")
        self.addToolBar( modeToolBar )
        modeToolBar.addAction( actMove )
        modeToolBar.addAction( actDraw )
        modeToolBar.addAction( actSelect )
        modeToolBar.addAction( actLasso )

        optionsMenu = bar.addMenu("Options")
        actClearCanvas = optionsMenu.addAction(QIcon(":/icons/clear-all.png"), "&Clear canvas", self.clearCanvas)
        actNoBrush = optionsMenu.addAction("&No brush", self.clearBrush)

        optionsToolBar = QToolBar("Options")
        self.addToolBar( optionsToolBar )
        optionsToolBar.addAction( actClearCanvas )

    def open(self):
        print("Open...")
        newAct = QAction(QIcon(":/icons/open.png"), " Open...", self)
        newAct.setShortcut(QKeySequence("Ctrl+O"))
        newAct.setToolTip("Open an existing file")
        self.fileMenu.addAction(newAct)
        newAct.triggered.connect(self.openFile)
    
    def save(self):
        print("Save")    
        newAct = QAction(QIcon(":/icons/save.png"), " Save...", self)
        newAct.setShortcut(QKeySequence("Ctrl+S"))
        newAct.setToolTip("Save file")
        self.fileMenu.addAction(newAct)
        newAct.triggered.connect(self.saveFile)    


    def quit(self):
        print("Quit")
        newAct = QAction(QIcon(":/icons/quit.png")," Quit...", self)
        newAct.setShortcut(QKeySequence("Ctrl+W"))
        newAct.setToolTip("Quit open file")
        self.fileMenu.addAction(newAct)
        newAct.triggered.connect(self.quitFile)

    def openFile(self):
        self.log_action("Opening file...")
        fileName = QFileDialog.getOpenFileName(self, "Open File", "~/androide", "*.txt")
        print(f"{fileName[0]=}")
        file = open(fileName[0],"r")
        content = file.read()
        print(content)
        self.textEdit.setPlainText(content)
        self.setWindowTitle(fileName[0])

    def saveFile(self):
        print("Saving file...")
        fileName = QFileDialog.getSaveFileName(self, "Save File")
        print(f"{fileName[0]=}")
        file = open(fileName[0],"w")
        file.write(self.textEdit.toPlainText())

    def quitFile(self):
        print("Quitting file...")
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Quit")
        dlg.setText("Do you wanna quit ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            print("Yes!")
            QApplication.quit()
        else:
            print("No!")
            return "no"
        
    def closeEvent(self, event):
        event.ignore()
        q = self.quitFile()



    ##############
    def pen_color(self):
        self.log_action("choose pen color")
        color = QColorDialog.getColor()
        self.canva.set_colorPen(color)
        self.log_action("Pen color: " + str(color))

    def brush_color(self):
        self.log_action("choose brush color")
        color = QColorDialog.getColor()
        self.canva.set_colorBrush(color)
        self.log_action("Brush color: " + str(color))

    def rectangle(self):
        self.log_action("Shape mode: rectangle")
        self.canva.add_object("rectangle")

    def ellipse(self):
        self.log_action("Shape Mode: circle")
        self.canva.add_object("ellipse")

    def free_drawing(self):
        self.log_action("Shape mode: free drawing")
        self.canva.add_object("free")

    def move(self):
        self.log_action("Mode: move")
        self.canva.setMode("move")

    def draw(self):
        self.log_action("Mode: draw")
        self.canva.setMode("draw")

    def select(self):
        self.log_action("Mode: select")
        self.canva.setMode("select")
    
    def clearBrush(self):
        self.log_action("Mode: clear brush")
        self.canva.set_colorBrush(0)

    def lasso(self):
        self.log_action("Mode: lasso")
        self.canva.setMode("lasso")

    def clearCanvas(self):
        self.log_action("Mode: clear all drawings")
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Clear all")
        dlg.setText("Do you want to clear the canvas ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()
        if button == QMessageBox.Yes:
            print("Yes!")
            self.canva.clearCanvas()
            self.textEdit.clear()
        else:
            print("No!")
            return "no"

    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText( content + "\n" + str)

if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()
