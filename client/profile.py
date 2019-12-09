import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class profile(QWidget):
    def __init__(self, after_login):
        super().__init__()
        self.after_login = after_login
        self.clientSocket = after_login.clientSocket
        self.studid = after_login.studId

        self.mainLayout = QVBoxLayout()
        self.head = QHBoxLayout()
        self.body = QVBoxLayout()
        self.bodypart1 = QWidget(self)
        self.bodypart11 = QHBoxLayout()
        self.bodypart2 = QWidget(self)
        self.bodypart22 = QHBoxLayout()
        self.bodypart3 = QWidget(self)
        self.bodypart33 = QHBoxLayout()
        self.tail = QVBoxLayout()

        self.mainLayout.setContentsMargins(0,0,0,0)

        self.initUi()

    def initUi(self):
        profile_groupbox = QGroupBox('프로필')
        profile_groupbox.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;')
        profile_groupbox.setLayout(self.body)
        profile_groupbox.setMinimumWidth(300)
        profile_groupbox.setMaximumHeight(300)


        self.nickname = QLabel()
        self.nickname.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')
        changeNick = QPushButton("변경")
        changeNick.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')
        changeNick.setMaximumHeight(60)
        changeNick.setMaximumWidth(90)
        changeNick.clicked.connect(self.changeNicknamePop)

        self.Dept = QLabel()
        self.Dept.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')
        self.Query = QLabel()
        self.Query.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')
        self.Respond = QLabel()
        self.Respond.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')
        self.Points = QLabel()
        self.Points.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')
        self.introduceLabel = QLabel("자기소개")
        self.introduceLabel.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')
        self.changeIntro = QPushButton("변경")
        self.changeIntro.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')
        self.introduceText = QTextBrowser()
        self.changeIntro.clicked.connect(self.changeIntroPop)

        self.getProfile()

        self.bodypart11.addWidget(self.nickname)
        self.bodypart11.addWidget(changeNick)
        self.bodypart22.addWidget(self.Query)
        self.bodypart22.addWidget(self.Respond)
        self.bodypart33.addWidget(self.introduceLabel)
        self.bodypart33.addWidget(self.changeIntro)

        self.bodypart1.setLayout(self.bodypart11)
        self.bodypart2.setLayout(self.bodypart22)
        self.bodypart3.setLayout(self.bodypart33)

        self.body.addWidget(self.bodypart1, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(self.Dept, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(self.bodypart2, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(self.Points, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(self.bodypart3, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(self.introduceText, alignment=QtCore.Qt.AlignCenter)


        self.body.addStretch(1)
        self.body.setSpacing(0)


        self.mainLayout.addLayout(self.head)
        self.mainLayout.addWidget(profile_groupbox)
        self.setLayout(self.mainLayout)
        self.setFixedSize(self.sizeHint())

    def getProfile(self):
        commend = 'getProfile ' + self.studid
        self.clientSocket.send(commend.encode('utf-8'))
        res = self.clientSocket.recv(1024)
        res = res.decode('utf-8')
        res = res.split(',')
        print(res)

        self.nickname.setText("닉네임: " + res[0])
        self.Dept.setText("소속: " + res[1])
        self.Query.setText("질문: " + res[2])
        self.Respond.setText("답변: " + res[3])
        self.Points.setText("포인트: " + res[4])
        self.introduceText.setText(res[6])


    def changeIntroPop(self):
        dlg = changeIntroPop(self)
        dlg.exec_()

    def changeNicknamePop(self):
        dlg = changeNickPop(self)
        dlg.exec_()


class changeIntroPop(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.clientSocket = self.parent.clientSocket

        self.mainLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMinimumSize(150, 150)
        self.setStyleSheet('background:')
        self.initUi()

    def initUi(self):
        intro_input = QLineEdit()
        intro_input.setPlaceholderText('자기소개 입력')
        change = QPushButton('확인')
        change.setFocusPolicy(Qt.NoFocus)
        cancel = QPushButton('취소')

        cancel.clicked.connect(self.close)
        change.clicked.connect(lambda: self.changeIntro(intro_input.text()))

        self.btnLayout.addWidget(change)
        self.btnLayout.addWidget(cancel)

        self.mainLayout.addWidget(intro_input)
        self.mainLayout.addLayout(self.btnLayout)
        self.setLayout(self.mainLayout)

    def changeIntro(self,intro):
        commend = "change_intro "+self.parent.studid + "!#!#" + intro
        self.clientSocket.send(commend.encode('utf-8'))
        res = self.clientSocket.recv(1024).decode('utf-8')

        if str(res) == 'changed':
            self.parent.introduceText.setText(intro)
            self.close()


class changeNickPop(QDialog):
    def __init__(self,parent):
        super().__init__()
        self.parent=parent
        self.clientSocket = self.parent.clientSocket

        self.mainLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMinimumSize(150,150)
        self.setStyleSheet('background:')
        self.initUi()

    def initUi(self):
        nick_input = QLineEdit()
        nick_input.setPlaceholderText('변경할 닉네임')
        change = QPushButton('변경')
        change.setFocusPolicy(Qt.NoFocus)
        cancel = QPushButton('취소')

        cancel.clicked.connect(self.close)
        change.clicked.connect(lambda: self.changeNickname(nick_input.text()))

        self.btnLayout.addWidget(change)
        self.btnLayout.addWidget(cancel)

        
        self.mainLayout.addWidget(nick_input)
        self.mainLayout.addLayout(self.btnLayout)
        self.setLayout(self.mainLayout)

    def changeNickname(self,nick):
        #중복검사 안함 추가해야됨
        commend = "OvelapCheck " + nick
        self.clientSocket.send(commend.encode('utf-8'))
        answer = self.clientSocket.recv(1024).decode('utf-8')
        if answer == "newone":
            send_noMark = QMessageBox()
            send_noMark.setStyleSheet("background-color:#FFFFFF")
            send_noMark.setText("닉네임 변경완료")
            send_noMark.exec_()

            commend = 'changeNick ' + self.parent.studid + " " + nick
            self.clientSocket.send(commend.encode('utf-8'))
            res = self.clientSocket.recv(1024).decode('utf-8')

            self.parent.nickname.setText(nick)
            self.close()
        elif answer == "noMark":
            send_noMark = QMessageBox()
            send_noMark.setStyleSheet("background-color:#FFFFFF")
            send_noMark.setText("ERROR["+answer+"]: 특수문자 감지")
            send_noMark.exec_()
        elif answer == "length":
            send_length = QMessageBox()
            send_length.setStyleSheet("background-color:#FFFFFF")
            send_length.setText("ERROR["+answer+"]: 길이는 4자~8자 한정")
            send_length.exec_()
        elif answer == "overlap":
            send_overlap = QMessageBox()
            send_overlap.setStyleSheet("background-color:#FFFFFF")
            send_overlap.setText("ERROR["+answer+"]: 닉네임 중복")
            send_overlap.exec_()


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()