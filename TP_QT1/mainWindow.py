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
		self.textEdit = QTextEdit(self)
		self.setCentralWidget(self.textEdit)

		label = QLabel("I'm working late cuz i'm a singerrrr")
		
		button = QRadioButton("That's that me espresso")
		button2 = QRadioButton("That's that me decafeino")
		layout = QVBoxLayout()
		layout.addWidget(label)
		label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
		layout.addWidget(self.textEdit)
		layout.addWidget(button)
		layout.addWidget(button2)
		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)

		

	###############
	def open(self):
		print("Open...")
		newAct = QAction(QIcon(":/icons/open.png"), " Open...", self)
		newAct.setShortcut(QKeySequence("Ctrl+O"))
		newAct.setToolTip("Open an existing file")
		self.fileMenu.addAction(newAct)
		newAct.triggered.connect(self.openFile)
	
	###############
	def save(self):
		print("Save")	
		newAct = QAction(QIcon(":/icons/save.png"), " Save...", self)
		newAct.setShortcut(QKeySequence("Ctrl+S"))
		newAct.setToolTip("Save file")
		self.fileMenu.addAction(newAct)
		newAct.triggered.connect(self.saveFile)	

	###############
	def quit(self):
		print("Quit")
		newAct = QAction(QIcon(":/icons/quit.png")," Quit...", self)
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
		self.textEdit.setPlainText(content)

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
		dlg.setText("Do you wanna quit")
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


def main(args):
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
	print("Hello World")
	
	
	

if __name__ == "__main__":
	main(sys.argv)