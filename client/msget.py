import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import chat_test



class Invisible(QWidget):
    def __init__(self,parent,lecture,prof):
        super().__init__()
        self.__press_pos = QPoint()
        self.mainLayout = QHBoxLayout()
        self.lecture = lecture.text()
        self.prof = prof.text()
        self.clientSocket = parent.w.clientSock
        self.parent = parent
        self.setLayout(self.mainLayout)
        self.initUI()
        #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def initUI(self):
        print(self.lecture)
        print(self.prof)
        commend = "HowManyChat " + self.lecture + " " + self.prof
        self.clientSocket.send(commend.encode('utf-8'))
        chatcount = self.clientSocket.recv(1024)
        chatcount = chatcount.decode('utf-8')
        l = QLabel()

        l.setStyleSheet('QLabel{image:url(./icon/msgWid.png)}')
        l.setText(str(chatcount))
        l.setFont(QFont("Times", 50, QFont.Bold))
        # self.adjustSize()
        # self.setGeometry(
        #     QStyle.alignedRect(
        #         Qt.LeftToRight,
        #         Qt.AlignCenter,
        #         self.size(),
        #         QApplication.instance().desktop().availableGeometry()
        #         )
        #     )
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        l.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(l)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__press_pos = event.pos()
        elif event.button() == Qt.RightButton:
            print("LELELELEL")
            self.close()
              

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__press_pos = QPoint()
        elif event.button() == Qt.RightButton:
            self.__press_pos = QPoint()
        

    def mouseMoveEvent(self, event):
        if not self.__press_pos.isNull():  
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def mouseDoubleClickEvent(self, QMouseEvent):
        print("ELELELELE")
        title = self.parent.course
        # self.chat = chat.chatRoom(title,self.stuid,self.w)
        self.parent.chat = chat_test.chatRoom(self.parent)
        self.parent.chat.setWindowTitle(title[0])
        self.parent.chat.setMinimumSize(QSize(400, 400))
        self.close()
        






if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Invisible("self")
    w.show()
    exit(app.exec_())
