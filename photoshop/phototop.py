import sys
import cv2
import numpy

from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtWidgets import QAction, QMenu, QMainWindow, QToolBar, qApp
from PyQt5.QtCore import Qt


# from PyQt5 import QtWidgets, QtGui
# from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, , QToolBar, QMenu, QLabel, QMessageBox
# from PyQt5.QtGui import QIcon, QPixmap, QImage
# from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.image = None
        self.sizeM = None
        self.label = QLabel()
        self.initUI()

    def initUI(self):
        self.label.setText('OpenCV Image')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('border: gray; border-style:solid; border-width: 1px;')
        root = QVBoxLayout(self)
        root.addWidget(self.label)
        self.setGeometry(70,50, 540, 540)


    def abrirImagen(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Buscar Imagen', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        self.image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

        self.mostrarImagen()

    
    def mostrarImagen(self):
        size = self.image.shape
        self.sizeM = self.image.shape
        step = self.image.size / size[0]
        qformat = QImage.Format_Indexed8

        if len(size) == 3:
            if size[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(self.image, size[1], size[0], step, qformat)
        img = img.rgbSwapped()        

        self.label.setPixmap(QPixmap.fromImage(img))
        self.resize(self.label.pixmap().size())

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ex = Example(self)
        self.setGeometry(300,100,640, 640)
        self.setWindowTitle("PhotoTop! ;D")

        # Menu
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&Arquivo')
        
        # ToolBar
        self.toolbar = QToolBar('Ferramentas')
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        
        # Contruindo as coisas
        self.Ferramentas()

    def Ferramentas(self):
        # ação SAIR
        self.exitAct = QAction(QIcon('icons/exit.png'), 'Sair', self)
        self.exitAct.setShortcut('Ctrl+W')
        self.exitAct.triggered.connect(qApp.quit)

        # ação Abrir
        self.openAct = QAction(QIcon('icons/open.png'), 'Abrir arquivo', self)
        self.openAct.setShortcut('Ctrl+O')
        self.openAct.triggered.connect(self.ex.abrirImagen)
        self.openAct.triggered.connect(self.AtualizarPAgina)
        
        # ação Salvar
        self.saveAct = QAction(QIcon('icons/save.png'), 'Salvar arquivo', self)
        self.saveAct.setShortcut('Ctrl+S')        


        # Actions for Menu
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.exitAct)
    
        # Actions for ToolBar
        self.toolbar.addAction(self.openAct)

    def AtualizarPAgina(self):
        self.resize(self.ex.sizeM[1]+100, self.ex.sizeM[0]+100)

    def contextMenuEvent(self, event):       
        cmenu = QMenu(self)
        # newAct = cmenu.addAction("New")
        # opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        
        if action == quitAct:
            qApp.quit()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())