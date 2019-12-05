import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow
import login
from socket import *
from PyQt5.QtWidgets import QApplication
import systemTray

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        #서버연결
        port = 3333
        self.clientSock = socket(AF_INET, SOCK_STREAM)
        # self.clientSock.connect(('34.84.112.149', port))
        #self.clientSock.connect(('192.168.0.6', port))
        # self.clientSock.connect(('192.168.43.36', port))
        #self.clientSock.connect(('192.168.25.22', port))
        self.clientSock.connect(('192.168.0.49', port))
        #self.clientSock.connect(('172.30.1.58', port))   
        #self.clientSock.connect(('172.30.1.21', port))   

        #트레이 아이콘 생성
        self.tray = systemTray.SystemTrayIcon(self)

        # 첫 화면 로그인 설정
        self.user = {'email':'','bb_url':'','is_prof':''}
        self.login = login.login(self)

        self.init_window()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setContentsMargins(0,0,5,5)
        self.oldPos = self.pos()

    def quitClicked(self):
        commend = 'exit'
        self.clientSock.send(commend.encode('utf-8'))
        QApplication.quit()

    def init_window(self):
        self.setCentralWidget(self.login)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())