# -*- coding:utf-8 -*-
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import after_login
import webbrowser
import register
import requests

class login(QWidget):
    def __init__(self, window):
        super().__init__()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setOffset(3)
        self.setGraphicsEffect(shadow)
        self.session = requests.session()

        QApplication.setActiveWindow(window)
        # 소켓 가져옴
        self.clientSocket = window.clientSock
        self.goToBB = False

        self.main = QVBoxLayout()
        self.mainWidget = QWidget()
        self.mainWidget.setObjectName("myParentWidget");
        self.mainWidget.setStyleSheet(
            'QWidget#myParentWidget { border-image:url(./ui/login_ui/점선2.png) 0 0 0 0 stretch stretch}')
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
        ajoutoktok = QPixmap('./ui/login_ui/toktok_logo.png')
        ajoutoktok = ajoutoktok.scaled(200, 400, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        logo.setPixmap(ajoutoktok)

        # titlebar 대신할 놈들
        btExit = QPushButton()
        btExit.setStyleSheet('border:0px')
        btExit.setIcon(QIcon('./icon/icons8-close-window-16.png'))
        btExit.setIconSize(QSize(15, 15))
        btExit.clicked.connect(self.quitClicked)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText('Account')
        self.id_input.setMaximumWidth(240)
        self.id_input.setStyleSheet('background:white; height:32; font-family: Arial')

        self.pw_input = QLineEdit()
        self.pw_input.setPlaceholderText('Password')
        self.pw_input.setMaximumWidth(240)
        self.pw_input.setStyleSheet('background:white; height:32; font-family: Arial')
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw_input.returnPressed.connect(self.btn_login_clicked)  # 엔터 처리

        self.subLayer.addStretch(3)

        # 로고1,2
        self.subLayer.addWidget(logo, alignment=(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop))

        # 로그인인풋
        self.subLayer.addWidget(self.id_input)
        self.subLayer.addWidget(self.pw_input)

        # 로그인버튼
        BtLogin = QPushButton()
        BtLogin.setMaximumWidth(240)
        BtLogin.setMaximumHeight(80)
        BtLogin.setStyleSheet('''
                        QPushButton{image:url(./ui/login_ui/login_button.png); border:0px; width:100px; height:50px}        

                        ''')
        self.subLayer.addWidget(BtLogin)

        checkgoToBB = QCheckBox('black board 이동하기')
        checkgoToBB.setStyleSheet('font:8pt 나눔스퀘어라운드 Regular;')
        checkgoToBB.stateChanged.connect(self.checkGoToBB)

        self.subLayer.addWidget(checkgoToBB)
        self.subLayer.addStretch(4.5)

        BtLogin.clicked.connect(self.btn_login_clicked)

        self.mainLayer.addWidget(btExit, alignment=QtCore.Qt.AlignRight)
        self.mainLayer.addLayout(self.subLayer)

        self.setLayout(self.main)
        self.setFixedSize(358, 590)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def checkGoToBB(self):
        if self.goToBB is False:
            self.goToBB = True
        else:
            self.goToBB = False
        # print(self.goToBB)

    def btn_login_clicked(self):
        # 교수용
        if self.id_input.text() == "a":
            if self.pw_input.text() == "a":
                # 첫 로그인인지 확인
                commend = "firstLogin " + '000000000'
                self.clientSocket.send(commend.encode('utf-8'))

                result = self.clientSocket.recv(1024)
                result = result.decode('utf-8')
                print(result)
                if result == 'first':
                    print('bb')
                    mainW = QApplication.activeWindow()
                    self.register = register.Register(self, mainW, '교수님', '000000000')
                    mainW.setCentralWidget(self.register)
                    self.close()

                else:  # already_resgisterd
                    # 응답 요청
                    commend = 'login ' + '000000000'
                    self.clientSocket.send(commend.encode('utf-8'))

                    # 결과 도착
                    server_msg = self.clientSocket.recv(1024)

                    lectureId = server_msg.decode('utf-8')

                    mainW = QApplication.activeWindow()
                    self.afterLogin = after_login.App(mainW, '000000000', '교수님', lectureId)
                    mainW.setCentralWidget(self.afterLogin)
                    self.close()
        else:
            res = self.session.post('https://eclass2.ajou.ac.kr/webapps/bbgs-autosignon-BBLEARN/ajouLogin.jsp',
                                    data={'userId': self.id_input.text(), 'userPw': self.pw_input.text()}).text

            res_split = res.split('^')

            # 로그인 성공
            if len(res_split) != 1:
                cookie = res_split[2]
                window = QApplication.activeWindow()
                window.user['email'] = self.id_input.text()
                r1 = self.session.get('https://eclass2.ajou.ac.kr' + cookie)
                window.user['bb_url'] = 'https://eclass2.ajou.ac.kr' + cookie

                if self.goToBB is True:
                    url = 'https://eclass2.ajou.ac.kr' + cookie
                    webbrowser.open(url)

                studentName = r1.text.split('title')[1].split('.')[1].split(' ')[0]
                studentId = res_split[0]

                # 첫 로그인인지 확인
                commend = "firstLogin " + studentId
                self.clientSocket.send(commend.encode('utf-8'))

                result = self.clientSocket.recv(1024)
                result = result.decode('utf-8')

                if result == 'first':
                    print('aaaa')
                    mainW = QApplication.activeWindow()
                    self.register = register.Register(self, mainW, studentName, studentId)
                    mainW.setCentralWidget(self.register)
                    self.close()

                else:  # already_resgisterd
                    # 응답 요청
                    commend = 'login ' + studentId
                    self.clientSocket.send(commend.encode('utf-8'))

                    # 결과 도착
                    server_msg = self.clientSocket.recv(1024)

                    lectureId = server_msg.decode('utf-8')

                    mainW = QApplication.activeWindow()
                    self.afterLogin = after_login.App(mainW, studentId, studentName, lectureId)
                    mainW.setCentralWidget(self.afterLogin)
                    self.close()

            # 로그인 실패
            else:
                print("Error")
                msg = QMessageBox()
                msg.setStyleSheet("background-color:#FFFFFF")
                msg.setText("Error: Login Error")
                msg.setWindowTitle("Login Error")
                msg.exec_()

    def quitClicked(self):
        commend = 'exit'
        self.clientSocket.send(commend.encode('utf-8'))
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = login()
    sys.exit(app.exec_())