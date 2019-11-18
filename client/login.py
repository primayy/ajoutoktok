# -*- coding:utf-8 -*-
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import after_login
import webbrowser
import requests

class login(QWidget):
    def __init__(self,window):
        super().__init__()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setOffset(3)
        self.setGraphicsEffect(shadow)

        QApplication.setActiveWindow(window)
        #소켓 가져옴
        self.clientSocket = window.clientSock
        self.goToBB = False

        self.main = QVBoxLayout()
        self.mainWidget = QWidget()
        self.mainWidget.setStyleSheet("background-color:#5218FA ")
        self.mainLayer = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayer)

        self.subLayer = QVBoxLayout()
        self.subLayer.setAlignment(Qt.AlignCenter)
        self.subLayer.setContentsMargins(0, 0, 0, 0)

        self.main.addWidget(self.mainWidget)
        self.main.setContentsMargins(0, 0, 0, 0)

        self.oldPos = self.pos()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('로그인')

        logo = QLabel()

        # titlebar 대신할 놈들
        btExit = QPushButton()
        btExit.setStyleSheet('border:0px')
        btExit.setIcon(QIcon('./icon/icons8-close-window-16.png'))
        btExit.setIconSize(QSize(15,15))
        btExit.clicked.connect(self.quitClicked)

        logo.setPixmap(QPixmap('./icon/gnb_ajoulogo.png'))

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText('Account')
        self.id_input.setMaximumWidth(240)
        self.id_input.setStyleSheet('background:white; height:37; font-family: Arial')

        self.pw_input = QLineEdit()
        self.pw_input.setPlaceholderText('Password')
        self.pw_input.setMaximumWidth(240)
        self.pw_input.setStyleSheet('background:white; height:37; font-family: Arial')
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw_input.returnPressed.connect(self.btn_login_clicked)  # 엔터 처리

        self.subLayer.addStretch(2)
        self.subLayer.addWidget(logo)
        self.subLayer.addStretch(1)
        self.subLayer.addWidget(self.id_input)
        self.subLayer.addWidget(self.pw_input)

        BtLogin = QPushButton('Login')
        BtLogin.setMaximumWidth(240)
        BtLogin.setMaximumHeight(37)
        BtLogin.setStyleSheet('background:#F6F6F3; height:33; font-size:12px; font-family: Arial')

        self.subLayer.addWidget(BtLogin)

        checkgoToBB = QCheckBox('black board 이동하기')
        checkgoToBB.stateChanged.connect(self.checkGoToBB)

        self.subLayer.addWidget(checkgoToBB)

        self.subLayer.addStretch(3)

        BtLogin.clicked.connect(self.btn_login_clicked)

        self.mainLayer.addWidget(btExit, alignment=QtCore.Qt.AlignRight)
        self.mainLayer.addLayout(self.subLayer)

        self.setLayout(self.main)
        self.setFixedSize(358, 590)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.show()

    def checkGoToBB(self):
        if self.goToBB is False:
            self.goToBB = True
        else:
            self.goToBB = False
        # print(self.goToBB)

    def btn_login_clicked(self):

        # res = requests.post('https://eclass2.ajou.ac.kr/webapps/bbgs-autosignon-BBLEARN/ajouLogin.jsp',
        #                   data={'userId': self.id_input.text(), 'userPw': self.pw_input.text()}).text
        #
        # res_split = res.split('^')

        # #로그인 성공
        # if len(res_split) is not 1:
        #     cookie = res_split[2]
        #
        #     r1 = requests.get('https://eclass2.ajou.ac.kr' + cookie)
        #     if self.goToBB is True:
        #         url = 'https://eclass2.ajou.ac.kr' + cookie
        #         webbrowser.open(url)
        #
        #     studentName = r1.text.split('title')[1].split('.')[1].split(' ')[0]
        #     studentId = res_split[0]
        #
        #     #응답 요청
        #     commend = 'login '+studentId
        #     self.clientSocket.send(commend.encode('utf-8'))
        #
        #     print("LOG IN")
        #
        #     #결과 도착
        #     server_msg = self.clientSocket.recv(1024)
        #     print(server_msg.decode('utf-8'))
        #
        #     lectureId = server_msg.decode('utf-8')
        #
        #     mainW = QApplication.activeWindow()
        #     self.afterLogin = after_login.App(mainW, studentId, studentName, lectureId)
        #     mainW.setCentralWidget(self.afterLogin)
        #     self.close()
        #
        # #로그인 실패
        # else:
        #     print("Error")
        #     msg = QMessageBox()
        #     msg.setStyleSheet("background-color:#FFFFFF")
        #     msg.setText("Error: Login Error")
        #     msg.setWindowTitle("Login Error")
        #     msg.exec_()


        # 테스트 코드
        studentId = '201520990'

        # 응답 요청
        commend = 'login ' + studentId
        self.clientSocket.send(commend.encode('utf-8'))
        studentName = '김용표'

        # 결과 도착
        server_msg = self.clientSocket.recv(1024)
        # print(server_msg.decode('utf-8'))

        lectureId = server_msg.decode('utf-8')
        print(lectureId)

        mainW = QApplication.activeWindow()
        self.afterLogin = after_login.App(mainW, studentId, studentName, lectureId)
        mainW.setCentralWidget(self.afterLogin)
        self.close()
        # DB에서 로그인 정보 확인

    def quitClicked(self):
        commend = 'exit'
        self.clientSocket.send(commend.encode('utf-8'))
        QApplication.quit()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = login()
    sys.exit(app.exec_())