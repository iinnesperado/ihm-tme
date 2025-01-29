import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Canvas import *
import resources

class MainWindow(QMainWindow):

    def __init__(self, parent = None ):
        QMainWindow.__init__(self, parent )
        print( "init mainwindow")
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

        actPen = self.fileMenu.addAction(QIcon(":/icons/pen.png"), "&Pen color", self.pen_color, QKeySequence("Ctrl+P"))
        actBrush = self.fileMenu.addAction(QIcon(":/icons/brush.png"), "&Brush color", self.brush_color, QKeySequence("Ctrl+B"))

        colorToolBar = QToolBar("Color")
        self.addToolBar( colorToolBar )
        colorToolBar.addAction( actPen )
        colorToolBar.addAction( actBrush )

        shapeMenu = bar.addMenu("Shape")
        actRectangle = self.fileMenu.addAction(QIcon(":/icons/rectangle.png"), "&Rectangle", self.rectangle )
        actEllipse = self.fileMenu.addAction(QIcon(":/icons/ellipse.png"), "&Ellipse", self.ellipse)
        actFree = self.fileMenu.addAction(QIcon(":/icons/free.png"), "&Free drawing", self.free_drawing)

        shapeToolBar = QToolBar("Shape")
        self.addToolBar( shapeToolBar )
        shapeToolBar.addAction( actRectangle )
        shapeToolBar.addAction( actEllipse )
        shapeToolBar.addAction( actFree )

        modeMenu = bar.addMenu("Mode")
        actMove = modeMenu.addAction(QIcon(":/icons/move.png"), "&Move", self.move)
        actDraw = modeMenu.addAction(QIcon(":/icons/draw.png"), "&Draw", self.draw)
        actSelect = modeMenu.addAction(QIcon(":/icons/select.png"), "&Select", self.select)

        modeToolBar = QToolBar("Navigation")
        self.addToolBar( modeToolBar )
        modeToolBar.addAction( actMove )
        modeToolBar.addAction( actDraw )
        modeToolBar.addAction( actSelect )

    def open(self):
        print("Open...")
        newAct = QAction(QIcon("~/androide/ihm203/TP_QT1/open.pgn"), " Open...", self)
        newAct.setShortcut(QKeySequence("Ctrl+O"))
        newAct.setToolTip("Open an existing file")
        self.fileMenu.addAction(newAct)
        newAct.triggered.connect(self.openFile)
    
    def save(self):
        print("Save")    
        newAct = QAction(QIcon("~/androide/ihm203/TP_QT1/save.pgn"), " Save...", self)
        newAct.setShortcut(QKeySequence("Ctrl+S"))
        newAct.setToolTip("Save file")
        self.fileMenu.addAction(newAct)
        newAct.triggered.connect(self.saveFile)    


    def quit(self):
        print("Quit")
        newAct = QAction(QIcon("~/androide/ihm203/TP_QT1/quit.pgn")," Quit...", self)
        newAct.setShortcut(QKeySequence("Ctrl+W"))
        newAct.setToolTip("Quit open file")
        self.fileMenu.addAction(newAct)
        newAct.triggered.connect(self.quitFile)

    def openFile(self):
        print("Opening file...")
        fileName = QFileDialog.getOpenFileName(self, "Open File", "~/androide", "*.txt")
        print(f"{fileName[0]=}")
        file = open(fileName[0],"r")
        content = file.read()
        print(content)
        self.textEdit.setPlainText(content) # TODO change to drawing style file

    def saveFile(self):
        print("Saving file...")
        fileName = QFileDialog.getSaveFileName(self, "Save File")
        print(f"{fileName[0]=}")
        file = open(fileName[0],"w")
        file.write(self.textEdit.toPlainText()) # TODO change 

    def quitFile(self):
        print("Quitting file...")



    ##############
    def pen_color(self):
        self.log_action("choose pen color")

    def brush_color(self):
        self.log_action("choose brush color")

    def rectangle(self):
        self.log_action("Shape mode: rectangle")

    def ellipse(self):
        self.log_action("Shape Mode: circle")

    def free_drawing(self):
        self.log_action("Shape mode: free drawing")

    def move(self):
        self.log_action("Mode: move")

    def draw(self):
        self.log_action("Mode: draw")

    def select(self):
        self.log_action("Mode: select")

    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText( content + "\n" + str)

if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()
