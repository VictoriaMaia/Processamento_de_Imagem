import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QToolBar, QMenu, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initWin()
            
    def initWin(self):
        # (int x, int y, int width, int height)
        self.setGeometry(300,100,500,500)
        self.setWindowTitle("PhotoTop! ;D") 


class Acoes():
    def __init__(self, win):
        # ação SAIR
        self.exitAct = QAction(QIcon('icons/exit.png'), 'Sair', win)
        self.exitAct.setShortcut('Ctrl+W')
        self.exitAct.triggered.connect(qApp.quit)

        # ação Abrir
        self.openAct = QAction(QIcon('icons/open.png'), 'Abrir arquivo', win)
        self.openAct.setShortcut('Ctrl+O')

        # ação Salvar
        self.saveAct = QAction(QIcon('icons/save.png'), 'Salvar arquivo', win)
        self.saveAct.setShortcut('Ctrl+S')        


class Menu():
    def __init__(self, win):
        self.A = Acoes(win)
        # Menu
        self.menubar = win.menuBar()
        self.File(win)

        # ToolBar
        self.toolbar = QToolBar('Ferramentas')
        win.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.Tools(win)
        

    def File(self, win):
        fileMenu = self.menubar.addMenu('&Arquivo')
        fileMenu.addAction(self.A.openAct)
        fileMenu.addAction(self.A.saveAct)
        fileMenu.addAction(self.A.exitAct)
        
    def Tools(self, win):
        self.toolbar.addAction(self.A.openAct)

class MaiorDeTodas(MainWindow):
    def __init__(self):
        super().__init__()
        self.menu = Menu(self)
    
    def contextMenuEvent(self, event):       
        cmenu = QMenu(self)
        # newAct = cmenu.addAction("New")
        # opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        
        if action == quitAct:
            qApp.quit()


app = QApplication(sys.argv)
maior = MaiorDeTodas()
maior.show()
sys.exit(app.exec_())



