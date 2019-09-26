import sys
import cv2
import numpy
import os

from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtWidgets import QAction, QMenu, QMainWindow, QToolBar, qApp, QMessageBox
from PyQt5.QtCore import Qt


# from PyQt5 import QtWidgets, QtGui
# from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, , QToolBar, QMenu, QLabel, QMessageBox
# from PyQt5.QtGui import QIcon, QPixmap, QImage
# from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.image = ''
        self.sizeImg = None
        self.label = QLabel()
        self.initUI()
        self.filename = ''
        self.pathSave = os.getenv('HOME')

    def initUI(self):
        self.label.setText('OpenCV Image')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('border: gray; border-style:solid; border-width: 1px;')
        root = QVBoxLayout(self)
        root.addWidget(self.label)
        self.setGeometry(70,50, 540, 540)


    def abrirImagen(self):
        self.filename, _ = QFileDialog.getOpenFileName(None, 'Buscar Imagen', '.', 'Image Files (*.png *.jpg *.bmp)')
        self.image = cv2.imread(self.filename, cv2.IMREAD_UNCHANGED)
        self.typeImg = self.filename[-4: ]        

        if (self.filename != ''):    
            for i in range(len(self.filename)-1, -1, -1):
                    if(self.filename[i] == '/'):
                        break        
            self.nameImg = self.filename[i+1 : ]

            self.mostrarImagen()

    
    def mostrarImagen(self):        
        self.sizeImg = self.image.shape    
        qformat = QImage.Format_Indexed8

        if len(self.sizeImg) == 3:
            if self.sizeImg[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        # ajustar imagem na tela caso ela seja grande demais
        if(self.sizeImg[1] > 600):
            self.image = cv2.resize(self.image,(600,self.sizeImg[1]))
        if(self.sizeImg[0] > 600):
            self.image = cv2.resize(self.image,(self.sizeImg[0], 600))
        
        # autalizando informações da imagem
        self.sizeImg = self.image.shape
        step = self.image.size / self.sizeImg[0]

        # parte final para mostrar
        img = QImage(self.image, self.sizeImg[1], self.sizeImg[0], step, qformat)
        img = img.rgbSwapped()        

        self.label.setPixmap(QPixmap.fromImage(img))
        self.resize(self.label.pixmap().size())

    def salvarImagem(self):   
        if(self.filename != ''):     
            # se for diferente do HOME, salvar na pasta onde ele ja esta
            if(self.pathSave != os.getenv('HOME')):
                for i in range(len(self.pathSave)-1, -1, -1):
                    if(self.pathSave[i] == '/'):
                        break
                self.pathSave = self.pathSave.replace(self.pathSave[i+1 : ], '')            
            self.pathSave, _ = QFileDialog.getSaveFileName(self, 'Backup Contacts', self.pathSave, 'Image Files (*.png *.jpg *.bmp)')
            
            # verificar se quer substituir imagem
            if(self.pathSave[-4: ] != self.typeImg):
                self.pathSave = self.pathSave+self.typeImg

            cv2.imwrite(self.pathSave, self.image)

    def mostrarInformacoes(self):
        if (self.filename != ''):
            Nome = "Nome: \n      " + self.nameImg + "\n\n"
            Larg = "Largura: \n      " + str(self.sizeImg[1]) + "\n\n"
            Alt = "Altura: \n      " + str(self.sizeImg[0]) + "\n\n"
            Tipo = "Tipo: \n      " + self.typeImg + "\n\n"
            Past = "Pasta: \n      " + self.filename + "\n\n"

            return Nome+Larg+Alt+Tipo+Past
        else:
            return "Nenhuma imagem a ser informada!"


###########################################################################
############### CLASS MAIN WINDOW #########################################
###########################################################################


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ex = Example(self)
        self.setGeometry(300,70,640, 640)
        # self.setGeometry(0,0,900, 700)
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
        # self.exitAct.triggered.connect(self.FecharTela)

        # ação ABRIR
        self.openAct = QAction(QIcon('icons/open.png'), 'Abrir arquivo', self)
        self.openAct.setShortcut('Ctrl+O')
        self.openAct.triggered.connect(self.ex.abrirImagen)
        self.openAct.triggered.connect(self.AtualizarPAgina)
        
        # ação SALVAR
        self.saveAct = QAction(QIcon('icons/save.png'), 'Salvar arquivo', self)
        self.saveAct.setShortcut('Ctrl+S')
        self.saveAct.triggered.connect(self.ex.salvarImagem)

        # ação ATUALIZAR PAGINA (ajeitar tela)
        self.autalizeAct = QAction(QIcon('icons/save.png'), 'Ajustar tela', self)
        self.autalizeAct.triggered.connect(self.AtualizarPAgina)

        # # ação Informarções
        self.infoAct = QAction(QIcon('icons/info.png'), 'Informações da imagem', self)
        self.infoAct.setShortcut('Ctrl+I')
        self.infoAct.triggered.connect(self.Infos)
        
        # # ação Desenhar
        # self.desenharAct = QAction(QIcon('icons/desenhar.png'), 'Desenhar linha', self)


        # # ação Pintar
        # self.pintAct = QAction(QIcon('icons/pintar.png'), 'Pintar', self)




        # Actions for Menu
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.infoAct)
        self.fileMenu.addAction(self.exitAct)
        
    
        # Actions for ToolBar
        self.toolbar.addAction(self.openAct)


    def AtualizarPAgina(self):
        if(self.ex.sizeImg != None):
            self.resize(self.ex.sizeImg[1]+100, self.ex.sizeImg[0]+70)

    def contextMenuEvent(self, event):       
        cmenu = QMenu(self)
        # infAct = cmenu.addAction(self.infoAct)
        atualAct = cmenu.addAction(self.autalizeAct)
        quitAct = cmenu.addAction(self.exitAct)
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
    
    # def closeEvent(self, event):        
    #     reply = QMessageBox.question(self, 'Mensagem',
    #         "Certeza que quer sair?", QMessageBox.Yes | 
    #         QMessageBox.No, QMessageBox.No)

    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()    

    # def FecharTela(self):
    #     reply = QMessageBox.question(self, 'Mensagem',
    #         "Certeza que quer sair?", QMessageBox.Yes | 
    #         QMessageBox.No, QMessageBox.No)

    #     if reply == QMessageBox.Yes:
    #         qApp.quit()
          
    def Infos(self):
        QMessageBox.about(self, "Informações", self.ex.mostrarInformacoes())
        


    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())