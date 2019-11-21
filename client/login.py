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
    def __init__(self,window):
        super().__init__()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setOffset(3)
        self.setGraphicsEffect(shadow)
        self.session = requests.session()

        QApplication.setActiveWindow(window)
        #소켓 가져옴
        self.clientSocket = window.clientSock
        self.goToBB = False

        self.main = QVBoxLayout()
        self.mainWidget = QWidget()
        self.mainWidget.setObjectName("myParentWidget");
        #self.mainWidget.setStyleSheet("background-color:#5218FA ")
        self.mainWidget.setStyleSheet('QWidget#myParentWidget { border-image:url(./ui/점선2.png) 0 0 0 0 stretch stretch}')
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
        ajoutoktok = QPixmap('./ui/toktok_logo.png')
        ajoutoktok= ajoutoktok.scaled(200,400,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        logo.setPixmap(ajoutoktok)

        # logo2 = QLabel()
        # ajoutoktok2 = QPixmap('./ui/Ajoutoktok.png')
        # ajoutoktok2= ajoutoktok2.scaled(100,200,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        # logo2.setPixmap(ajoutoktok2)

        # titlebar 대신할 놈들
        btExit = QPushButton()
        btExit.setStyleSheet('border:0px')
        btExit.setIcon(QIcon('./icon/icons8-close-window-16.png'))
        btExit.setIconSize(QSize(15,15))
        btExit.clicked.connect(self.quitClicked)

        #logo.setPixmap(QPixmap('./ui/아주똑똑_최종.png'))
        #logo.scaledToWidth(130)
        #logo.scaledToHeight(130)
        #logo.setIcon(QIcon('./ui/아주똑똑_최종.png'))
        #logo.setIconSize(QSize(50,200))
        #logo.resize(50,200)
        #logo.setStyleSheet('QLabel{image:url(./ui/아주똑똑_최종.png); height:300px}')
        
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

        #로고1,2
        self.subLayer.addWidget(logo, alignment=(QtCore.Qt.AlignCenter|QtCore.Qt.AlignTop))
        #self.subLayer.addWidget(logo2, alignment=QtCore.Qt.AlignCenter|QtCore.Qt.AlignTop)

        #로그인인풋
        self.subLayer.addWidget(self.id_input)
        self.subLayer.addWidget(self.pw_input)

        #로그인버튼
        BtLogin = QPushButton()
        BtLogin.setMaximumWidth(240)
        BtLogin.setMaximumHeight(80)
        #BtLogin.setStyleSheet('background:#F6F6F3; height:33; font-size:12px; font-family: Arial')
        #BtLogin.setIcon(QIcon('C:/Users/hyejin/1119/client/ui/로그인버튼.png'))
        #BtLogin.setStyleSheet('background-image:C:/Users/hyejin/ajoutoktok/ajoutoktok/client/ui/로그인버튼.png; height:33; font-size:12px; font-family: Arial')
        BtLogin.setStyleSheet('''
                        QPushButton{image:url(./ui/login_button.png); border:0px; width:100px; height:50px}        
                        
                        ''')
        self.subLayer.addWidget(BtLogin)

        checkgoToBB = QCheckBox('black board 이동하기')
        checkgoToBB.stateChanged.connect(self.checkGoToBB)

        self.subLayer.addWidget(checkgoToBB)
        #self.subLayer.setAlignment(AlignTop)
        self.subLayer.addStretch(4.5)

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
        res = self.session.post('https://eclass2.ajou.ac.kr/webapps/bbgs-autosignon-BBLEARN/ajouLogin.jsp',
                          data={'userId': self.id_input.text(), 'userPw': self.pw_input.text()}).text

        res_split = res.split('^')

        #로그인 성공
        if len(res_split) is not 1:
            cookie = res_split[2]

            r1 = self.session.get('https://eclass2.ajou.ac.kr' + cookie)
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
                self.register = register.Register(self,mainW, studentName, studentId)
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

        #로그인 실패
        else:
            print("Error")
            msg = QMessageBox()
            msg.setStyleSheet("background-color:#FFFFFF")
            msg.setText("Error: Login Error")
            msg.setWindowTitle("Login Error")
            msg.exec_()


        # # 테스트 코드
        # studentId = '201421123'
        # studentName = '김용표'

        # #첫 로그인인지 확인
        # commend = "firstLogin "+ studentId
        # self.clientSocket.send(commend.encode('utf-8'))
        #
        # result = self.clientSocket.recv(1024)
        # result = result.decode('utf-8')
        #
        # if result == 'first':
        #     mainW = QApplication.activeWindow()
        #     self.register = register.Register(mainW,studentName,studentId)
        #     mainW.setCentralWidget(self.register)
        #     self.close()
        #
        # else:#already_resgisterd
        #     # 응답 요청
        #     commend = 'login ' + studentId
        #     self.clientSocket.send(commend.encode('utf-8'))
        #
        #     # 결과 도착
        #     server_msg = self.clientSocket.recv(1024)
        #
        #     lectureId  = server_msg.decode('utf-8')
        #
        #     mainW = QApplication.activeWindow()
        #     self.afterLogin = after_login.App(mainW, studentId, studentName, lectureId)
        #     mainW.setCentralWidget(self.afterLogin)
        #     self.close()
        # DB에서 로그인 정보 확인

    def quitClicked(self):
        commend = 'exit'
        self.clientSocket.send(commend.encode('utf-8'))
        QApplication.quit()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = login()
    sys.exit(app.exec_())