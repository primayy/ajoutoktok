import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import chat_test
import time

class update_listener(QThread):
    countUpdate = pyqtSignal()

    def __init__(self,parent = None):
        super().__init__()
        parent.countStop.connect(self.count_stop)

        self.go = True

    def run(self):
        while self.go:
            time.sleep(2)  # 클라이언트 처리 과부하 방지

            self.countUpdate.emit()

    def count_stop(self):
        self.go = False

class Invisible(QWidget):
    countStop = pyqtSignal()

    def __init__(self,parent):
        super().__init__()
        self.__press_pos = QPoint()
        self.mainLayout = QHBoxLayout()

        self.lecture = parent.course[0]
        self.lecture_code = parent.course[1]

        self.clientSocket = parent.w.clientSock
        self.origin_num = int(self.howManyChat())

        self.parent = parent
        self.setLayout(self.mainLayout)
        self.initUI()

    def initUI(self):
        self.t = update_listener(parent=self)
        self.t.countUpdate.connect(self.count_update)
        self.t.start()

        self.l = QLabel()
        self.chatcount = 0
        self.l.setStyleSheet('QLabel{image:url(./icon/chat_Widget.png)}')
        self.l.setText(str(self.chatcount))
        self.l.setFont(QFont("Times", 50, QFont.Bold))

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.l.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.l)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()

    def count_update(self):
        num_new_msg = int(self.howManyChat())
        if self.parent.chat == 0:
            self.l.setText(str(num_new_msg-self.origin_num))
        else:
            self.origin_num = num_new_msg
            self.l.setText(str(num_new_msg - self.origin_num))


    def howManyChat(self):
        commend = "HowManyChat " + self.lecture_code
        self.clientSocket.send(commend.encode('utf-8'))
        chatcount = self.clientSocket.recv(1024)
        chatcount = chatcount.decode('utf-8')

        return chatcount

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__press_pos = event.pos()
        elif event.button() == Qt.RightButton:
            self.countStop.emit()
            self.t.quit()
            self.hide()
              

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__press_pos = QPoint()
        elif event.button() == Qt.RightButton:
            self.__press_pos = QPoint()
        

    def mouseMoveEvent(self, event):
        if not self.__press_pos.isNull():  
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def mouseDoubleClickEvent(self, QMouseEvent):
        title = self.parent.course
        self.parent.chat = chat_test.chatRoom(self.parent,1)
        self.parent.chat.msgWidgetPos = self.pos()
        self.parent.chat.setWindowTitle(title[0])
        self.parent.chat.setMinimumSize(QSize(400, 400))

        self.countStop.emit()
        self.t.quit()
        self.close()
        






if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Invisible("self")
    w.show()
    exit(app.exec_())
