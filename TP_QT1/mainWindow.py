# Ines Rahaoui
# Ines Tian Ruiz-Bravo Plovins

import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class MainWindow(QMainWindow):
	
	##############
	def __init__(self):
		super().__init__()
		print("constructeur de la class MainWindow")
		self.resize(300,300)

		bar = self.menuBar()
		self.fileMenu = bar.addMenu("File")
		self.open()
		self.save()
		self.quit()
		textEdit = QTextEdit(self)
		self.setCentralWidget(textEdit)

	###############
	def open(self):
		print("Open...")
		newAct = QAction(QIcon("~/androide/ihm203/TP_QT1/open.pgn"), " Open...", self)
		newAct.setShortcut(QKeySequence("Ctrl+O"))
		newAct.setToolTip("Open an existing file")
		self.fileMenu.addAction(newAct)
		newAct.triggered.connect(self.openFile)
	
	###############
	def save(self):
		print("Save")	
		newAct = QAction(QIcon("~/androide/ihm203/TP_QT1/save.pgn"), " Save...", self)
		newAct.setShortcut(QKeySequence("Ctrl+S"))
		newAct.setToolTip("Save file")
		self.fileMenu.addAction(newAct)
		newAct.triggered.connect(self.saveFile)	

	###############
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
		file = open(fileName[0],"r+")
		QTextEdit.setPlainText(file.read())
		


	def saveFile(self):
		print("Saving file...")
		fileName = QFileDialog.getSaveFileName(self, "Save File")
		print(f"{fileName[0]=}")

	def quitFile(self):
		print("Quitting file...")


def main(args):
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
	print("Hello World")
	
	
	

if __name__ == "__main__":
	main(sys.argv)