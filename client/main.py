import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow
import login
from socket import *
from PyQt5.QtWidgets import QApplication,QGraphicsDropShadowEffect

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        port = 3333

        self.clientSock = socket(AF_INET, SOCK_STREAM)
        #self.clientSock.connect(('34.84.112.149', port))
        self.clientSock.connect(('192.168.0.13', port))
        # self.clientSock.connect(('192.168.25.28', port))
        

        self.login = login.login(self)
        # self.login.setGraphicsEffect(shadow)

        self.init_window()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setContentsMargins(0,0,5,5)
        self.oldPos = self.pos()

    def init_window(self):
        self.setCentralWidget(self.login)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())