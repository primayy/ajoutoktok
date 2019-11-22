import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from socket import *
import time


class update_listener(QThread):
    chatUpdate = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.chatSocket = parent.chatSocket
        self.go = True

    def run(self):
        while self.go:
            time.sleep(1)  # 클라이언트 처리 과부하 방지

            update_commend = self.chatSocket.recv(1024)
            update_commend = update_commend.decode('utf-8')

            if update_commend == 'update':
                self.chatUpdate.emit()
                # print('업데이트 시그널 emit')
            elif update_commend == 'stop':
                self.go = False
                print('멈춤')
                # break

class Reply(QWidget):
    def __init__(self):
        super().__init__()
        # self.parent = parent
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setOffset(3)
        self.setGraphicsEffect(shadow)
        self.oldPos = self.pos()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)

        #배경색 지정할 위젯 선언
        self.mainWidget = QWidget()
        self.mainWidget.setStyleSheet('background-color:white')

        #질문 타이틀 레이아웃
        self.questionWidget = QWidget()
        self.questionWidget.setStyleSheet('background-color:grey;')
        self.question_title_bottom = QHBoxLayout()

        #타이틀 관련 위젯은 questionLayout에 추가
        self.questionLayout = QVBoxLayout()
        self.questionWidget.setLayout(self.questionLayout)
        self.questionWidget.setMaximumSize(500,200)
        self.questionLayout.setContentsMargins(0,0,0,0)


        #위젯에 다른 위젯 추가하기 위한 레이아웃 선언
        self.widgetLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.widgetLayout)

        #메인 레이아웃에 메인 위젯 추가

        self.mainLayout.addWidget(self.mainWidget)


        self.setLayout(self.mainLayout)
        self.setMinimumSize(500, 400)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.initUI()

    def initUI(self):
        #화면 구성요소
        #위젯은 widgetLayout에 추가하면 됨
        btnBack =QPushButton('뒤로')

        #질문 타이틀
        question_title = QLabel('에에에에에')
        self.questionLayout.addWidget(question_title)

        #질문 타이틀 bottom
        self.dateLabel = QLabel('시간')
        self.btnLike = QPushButton('좋아요')

        self.question_title_bottom.addWidget(self.dateLabel)
        self.question_title_bottom.addWidget(self.btnLike)

        self.questionLayout.addLayout(self.question_title_bottom)


        #질문 목록
        self.question_reply = QListWidget()
        self.question_reply.setBaseSize(500, 200)
        self.question_reply.setMaximumSize(500,200)

        self.question_reply.setStyleSheet('''
                        # QListWidget:item:hover{background:white};
                        # QListWidget:item{padding:0px}
                        ''')
        item = QListWidgetItem(self.question_reply)

        custom_widget = replyWidget(self,['a','b'])
        item.setSizeHint(custom_widget.sizeHint())
        self.question_reply.setItemWidget(item, custom_widget)
        self.question_reply.addItem(item)



        #widgetLayout에 추가
        self.widgetLayout.addWidget(btnBack)
        self.widgetLayout.addWidget(self.questionWidget)

        # self.widgetLayout.addWidget(question_title)

        self.widgetLayout.addWidget(self.question_reply)


        # self.show()


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


class replyWidget(QWidget):
    def __init__(self, parent, comments):
        super().__init__()
        self.parent = parent

        self.replyLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        # comments 참조 순서 studid,name,comment,like,category_id,time
        self.comments = comments
        self.initUI()

    def initUI(self):
        if len(self.comments) != 2:
            BtnLike = QPushButton(self.comments[3])
            BtnLike.setIcon(QIcon('./icon/heart_unchecked.png'))
            BtnLike.setStyleSheet('''
            QPushButton{border:0px}''')
            BtnLike.setIconSize(QSize(20, 20))
            BtnLike.setMaximumWidth(35)
            BtnLike.clicked.connect(self.likeClicked)

            question = QLabel()
            question.setText(self.comments[2])
            date = QLabel('시간')

        else:
            BtnLike = QPushButton('0')
            BtnLike.setIcon(QIcon('./icon/heart_unchecked.png'))
            BtnLike.setStyleSheet('''
                        QPushButton{border:0px}''')
            BtnLike.setIconSize(QSize(20, 20))
            BtnLike.setMaximumWidth(35)
            BtnLike.clicked.connect(self.likeClicked)

            question = QLabel()
            question.setText(self.comments[0])

            date = QLabel('시간')

        self.replyLayout.addWidget(question)
        self.replyLayout.addWidget(date)
        self.mainLayout.addLayout(self.replyLayout)
        self.mainLayout.addWidget(BtnLike)

    def likeClicked(self):
        print(self.comments)
        commend = 'like_update ' + self.comments[6] + " " + self.grandparent.stuid  # 학번 + msg
        self.clientSocket.send(commend.encode('utf-8'))
        print(commend)
        result = self.clientSocket.recv(1024)
        result = result.decode('utf-8')
        print(result)
        self.parent.category_changed()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print(self.comments)
            print("Left Button Clicked")
            # self.chat = reply_test.replyRoom(self,self.grandparent)기능 안되서 주석처리

            # self.chat.setWindowTitle(self.comments[6])
            # self.chat.setMinimumSize(QSize(400, 400))

        elif QMouseEvent.button() == Qt.RightButton:
            print("Right Button Clicked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Reply()
    sys.exit(app.exec_())