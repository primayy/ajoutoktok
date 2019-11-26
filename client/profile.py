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
        self.tail = QVBoxLayout()

        self.mainLayout.setContentsMargins(0,0,0,0)

        self.initUi()

    def initUi(self):
        profile_groupbox = QGroupBox('프로필')
        profile_groupbox.setLayout(self.body)
        profile_groupbox.setMinimumWidth(300)


        self.nickname = QLabel()
        changeNick = QPushButton("변경")
        changeNick.setMaximumHeight(100)
        changeNick.setMaximumWidth(150)
        changeNick.clicked.connect(self.changeNickname)

        self.Dept = QLabel()
        self.Query = QLabel()
        self.Respond = QLabel()
        self.Points = QLabel()

        self.getProfile()

        self.bodypart11.addWidget(self.nickname)
        self.bodypart11.addWidget(changeNick)
        self.bodypart22.addWidget(self.Query)
        self.bodypart22.addWidget(self.Respond)

        self.bodypart1.setLayout(self.bodypart11)
        self.bodypart2.setLayout(self.bodypart22)

        self.body.addWidget(self.bodypart1, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(self.Dept, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(self.bodypart2, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(self.Points, alignment=QtCore.Qt.AlignCenter)


        self.mainLayout.addLayout(self.head)
        self.mainLayout.addWidget(profile_groupbox)
        self.setLayout(self.mainLayout)
        self.setFixedSize(self.sizeHint())

    def changeNickname(self):
        commend = 'changeNick ' + self.studid
        # self.clientSocket.send(commend.encode('utf-8'))

    def getProfile(self):
        commend = 'getProfile ' + self.studid
        self.clientSocket.send(commend.encode('utf-8'))
        res = self.clientSocket.recv(1024)
        res = res.decode('utf-8')
        res = res.split(',')

        self.nickname.setText("닉네임: " + res[0])
        self.Dept.setText("소속: " + res[1])
        self.Query.setText("질문: " + res[2])
        self.Respond.setText("답변: " + res[3])
        self.Points.setText("포인트: " + res[4])