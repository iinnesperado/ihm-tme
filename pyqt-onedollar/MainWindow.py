import sys
import numpy as np
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from gdrawer import GDrawer
from Canvas import Canvas, qpolygonF_to_points

import pickle

class MainWindow(QMainWindow):

    def __init__(self, parent = None ):
        QMainWindow.__init__(self, parent )

        self.thumbnail_size = 150
        self.resize(600, 500)

        bar = self.menuBar()
        fileMenu = bar.addMenu("File")
        actOpen = fileMenu.addAction( QIcon("./icons/open.png"), "&Open...", self.open, QKeySequence("Ctrl+O") )
        actSave = fileMenu.addAction( QIcon("./icons/save.png"), "&Save...", self.save, QKeySequence("Ctrl+S") )
        actQuit = fileMenu.addAction( QIcon("./icons/quit.png"), "&Quit...", self.quit, QKeySequence("Ctrl+Q") )

        fileToolBar = QToolBar("File")
        self.addToolBar( fileToolBar )
        fileToolBar.addAction( actOpen )
        fileToolBar.addAction( actSave )


        self.container = QWidget(self)
        v_layout = QVBoxLayout( self.container )
        self.container.setLayout( v_layout )

        ################################
        # Ajout d'un bouton pour ajouter un template
        ###############################
        self.add_template_button = QPushButton("Ajouter un template", self)
        v_layout.addWidget(self.add_template_button)

        self.add_template_button.clicked.connect(self.add_new_template)


        ################################
        # TODO 2: create the template gallery
        ###############################
        self.gallery = self.create_template_gallery()
        v_layout.addWidget( self.gallery )

        self.canvas = Canvas()
        v_layout.addWidget(self.canvas)

        # Load the templates
        #self.load_templates()

        self.textEdit = QTextEdit( self )
        v_layout.addWidget( self.textEdit )

        self.setCentralWidget( self.container )

        ################################
        # TODO 9: connect the signal and the slot
        ###############################

        self.canvas.selected_template.connect( self.set_action_on_gesture )



        ################################
        # TODO 3: fill the template gallery
        ###############################
        name = ["Triangle", "X", "Rectangle", "Circle", "Check", "Caret", "Question", "Arrow", "left square bracket",
                "Right square bracket", "V", "Delete", "Left curly brace", "Right curly brace", "Star", "Pigtail"]
        #todo load the database
        d = pickle.load(open("./onedol_ds.pkl", "rb"))
        data = d['dataset']
        labels = d['labels']

        label = -1
        all_gesture = False
        for g, l in zip(data, labels):
            if l != label:

                #todo 3 add the template in the gallery
                self.add_template_thumbnail(g, name[l])

                #todo 4 add the template to the one_dollar_recognizer
                self.canvas.oneDollar.addTemplate(g, name[l])

                if not all_gesture:
                    label = l



    ################################
    #   Ajout d'un template
    ###############################

    def add_new_template(self):
        if self.canvas.path:
            label, ok = QInputDialog.getText(self, "Nouveau template", "Entrez un nom pour le template :")
            if ok and label:
                gesture = np.array(qpolygonF_to_points(self.canvas.path))
                
                # Ajouter à la galerie
                self.add_template_thumbnail(gesture, label)
                
                # Ajouter au modèle OneDollar
                self.canvas.oneDollar.addTemplate(gesture, label)
                
                # Sauvegarder les templates
                self.save_templates()

    def save_templates(self):
        data = {
            "datasets": self.canvas.oneDollar.templates,
            "labels": self.canvas.oneDollar.labels
        }
        with open("templates.pkl", "wb") as f:
            pickle.dump(data, f)
        print("Templates sauvegardés.")

    def load_templates(self):
        try:
            with open("templates.pkl", "rb") as f:
                data = pickle.load(f)
                for template, label in zip(data["datasets"], data["labels"]):
                    self.add_template_thumbnail(template, label)
                    self.canvas.oneDollar.addTemplate(template, label)
            print("Templates chargés.")
        except FileNotFoundError:
            print("Aucun fichier de templates trouvé.")




    ##########################
    # TODO 2: create the gallery (QListWidget)
    ##########################
    def create_template_gallery(self):
        gallery = QListWidget()

        #todo 2 customize the gallery
        gallery.setViewMode(QListWidget.IconMode)
        gallery.setUniformItemSizes(True)
        gallery.setIconSize(QSize(100, 100))
        gallery.setMinimumSize(600, 200)

        

        return gallery


    ################################
    # TODO 3: fill the template gallery
    ###############################
    def add_template_thumbnail(self, g, label):

        #draw the template path into a QIcon (icon)
        thumbnail_widget = GDrawer()
        thumbnail_widget.set_gesture_path(g, label )
        pix = QPixmap(thumbnail_widget.size())
        thumbnail_widget.render(pix, QPoint(), QRegion(0, 0, thumbnail_widget.width(), thumbnail_widget.height()));
        
        icon = QIcon(pix)

        #todo 3 create and add the corresponding item in the gallery
        item = QListWidgetItem(icon, label)
        self.gallery.addItem(item)


    #######################
    # TODO 9
    #######################
    def set_action_on_gesture(self, label, id, score):
        message = "template: " + label + " score: " + str(score)
        self.textEdit.setPlainText( message+  "\n" + self.textEdit.toPlainText() )

        #todo 9 select the corresponding element in the galery
        self.gallery.setCurrentRow(id)
        

    ##############
    def open(self):
        fileName = QFileDialog.getOpenFileName(self, "Open file", ".")
        file = open(fileName[0], 'r')
        str = file.readlines()
        str = '\n'.join(str)
        self.textEdit.setHtml( str )
        file.close()


    ###############
    def save(self):
        fileName = QFileDialog.getSaveFileName(self, "Save file", ".")
        with open(fileName[0], 'w') as fileSave:
            string = self.textEdit.toPlainText()
            fileSave.write(string)
            fileSave.close()
            print("Save... ", fileName[0], " saved.")

    ###############
    def quit(self):
        box = QMessageBox()
        b = box.question(self, 'Exit?', "Do you really want to exit ?", QMessageBox.Yes | QMessageBox.No)
        box.setIcon(QMessageBox.Question)
        if b == QMessageBox.Yes:
            sys.exit()

    def closeEvent(self, event):
        #event.ignore()
        #self.quit()
        return

    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText( content + "\n" + str)

if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
