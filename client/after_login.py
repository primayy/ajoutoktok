import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
import lecture_list as lec
import alarm
import setting
import profile
import leaderBoard as leader
import webbrowser

class App(QWidget):
    def __init__(self, window, studid, studname, lecid):
        super().__init__()
        QApplication.setActiveWindow(window)

        #그림자 효과
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setOffset(3)
        self.setGraphicsEffect(shadow)

        self.w = window

        #클라이언트 소켓
        self.clientSocket = window.clientSock
        self.studId =studid
        if lecid is 'x':
            self.lecId = []
        else:
            self.lecId = lecid.split(' ')

        self.mainLayout = QHBoxLayout()

        # 왼쪽 레이아웃
        self.leftSide = QWidget(self)
        self.leftSide.setFixedWidth(100)
        self.leftSide.setStyleSheet("background-color:white")

        self.leftSideLayout = QVBoxLayout()
        self.leftSideLayout.setContentsMargins(0, 50, 0, 0)

        self.leftSide.setLayout(self.leftSideLayout)

        # 오른쪽 레이아웃
        self.rightSide = QWidget(self)

        self.rightSide.setStyleSheet('background-color:#eef5f6')

        self.rightSideLayout = QVBoxLayout()
        self.rightSideTitle = QHBoxLayout()
        self.rightSideInfo = QWidget()

        self.rightSideLayout.addLayout(self.rightSideTitle)
        self.rightSideLayout.addStretch(1)

        self.rightSide.setLayout(self.rightSideLayout)

        self.mainLayout.addWidget(self.leftSide)
        self.mainLayout.addWidget(self.rightSide)
        self.mainLayout.addLayout(self.rightSideLayout)

        self.mainLayout.setContentsMargins(1, 1, 1, 1)
        self.mainLayout.setSpacing(0)

        self.initUI(studid, studname, self.lecId)

    def initUI(self, studid, studname, lecid):

        ##왼쪽 레이아웃 유저
        user_img = QPushButton()
        user_img.setStyleSheet('''
                                QPushButton{border:0px;}
                                QPushButton:hover{background:#e9e9e2; border:0px}
                                ''')
        user_img.setIcon(QIcon('./icon/bb.png'))
        user_img.setIconSize(QSize(100,70))
        user_img.clicked.connect(self.goToBB)

        userName = QLabel(studname)
        userName.setStyleSheet("font: 9pt 나눔스퀘어라운드 Regular;color:#42808a")
        
        userHakNum = QLabel(str(studid))
        userHakNum.setStyleSheet("font: 8pt 나눔스퀘어라운드 Regular;color:#42808a")
        ##왼쪽 레이아웃 버튼
        btnList = QPushButton()
        btnList.setMaximumHeight(200)
        btnList.setMaximumWidth(200)
        btnList.setStyleSheet('''
                        QPushButton{image:url(./ui/afterlogin_ui/list.png); border:0px; width:32px; height:32px}        
                        QPushButton:hover{background:#e9e9e2; border:0px}
                        ''')
        btnList.setToolTip('강의 목록')
        btnList.clicked.connect(self.showList)

        btnAlram = QPushButton()
        btnAlram.setMaximumHeight(200)
        btnAlram.setMaximumWidth(200)
        btnAlram.setStyleSheet('''
                        QPushButton{image:url(./ui/afterlogin_ui/alarm.png); border:0px; width:36px; height:36px}        
                        QPushButton:hover{image:url(./icon/bell2.png); background:#e9e9e2; border:0px}
                        ''')
        btnAlram.setToolTip('알림')
        btnAlram.clicked.connect(self.showAlarm)

        btnLeaderBoard = QPushButton()
        btnLeaderBoard.setToolTip('리더보드')
        btnLeaderBoard.setStyleSheet('''
                QPushButton{image:url(./ui/afterlogin_ui/trophy.png); border:0px; width:40px; height:40px}        
                QPushButton:hover{background:#e9e9e2; border:0px}
                ''')
        btnLeaderBoard.clicked.connect(self.showLeader)

        btnMore = QPushButton()
        btnMore.setToolTip('설정')
        btnMore.setStyleSheet('''
                        QPushButton{image:url(./ui/afterlogin_ui/setting.png); border:0px; width:32px; height:32px}        
                        QPushButton:hover{background:#e9e9e2; border:0px}
                        ''')
        btnMore.clicked.connect(self.showSetting)

        self.leftSideLayout.addWidget(user_img, alignment=QtCore.Qt.AlignCenter)
        self.leftSideLayout.addWidget(userName, alignment=QtCore.Qt.AlignCenter)
        self.leftSideLayout.addWidget(userHakNum, alignment=QtCore.Qt.AlignCenter)
        self.leftSideLayout.addStretch(1)
        self.leftSideLayout.addWidget(btnList)
        self.leftSideLayout.addStretch(1)
        self.leftSideLayout.addWidget(btnAlram)
        self.leftSideLayout.addStretch(1)
        self.leftSideLayout.addWidget(btnLeaderBoard)
        self.leftSideLayout.addStretch(1)
        self.leftSideLayout.addWidget(btnMore)
        self.leftSideLayout.addStretch(5)

        ##오른쪽 레이아웃

        ##타이틀바

        # 최소화
        btMini = QPushButton()
        btMini.setStyleSheet('''border:0px''')
        btMini.setIcon(QIcon('./ui/afterlogin_ui/minimize_button.png'))
        btMini.setIconSize(QSize(17,17))
        btMini.clicked.connect(lambda: QApplication.activeWindow().showMinimized())

        # 종료
        btExit = QPushButton()
        btExit.setStyleSheet('''border:0px''')
        btExit.setIcon(QIcon('./ui/afterlogin_ui/close_button.png'))
        btExit.setIconSize(QSize(17,17))
        btExit.clicked.connect(self.quitClicked)

        self.rightSideTitle.addStretch(1)
        self.rightSideTitle.addWidget(btMini, alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))
        self.rightSideTitle.addWidget(btExit, alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))

        self.rightSideInfo = lec.lecture_list(studid,lecid,QApplication.activeWindow())
        self.rightSideLayout.addWidget(self.rightSideInfo)

        # 메인 레이아웃 그리기
        self.setLayout(self.mainLayout)
        self.setWindowTitle('test')
        self.setStyleSheet("background-color:white")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.show()

    def goToBB(self):
        webbrowser.open('eclass2.ajou.ac.kr')

    def profile(self):
        self.profile = profile.profile('A', 'A', 'A', 'A', 'A', self.studId)

    def showList(self):
        self.rightSideInfo.close()
        self.rightSideInfo = lec.lecture_list(self.studId,self.lecId,QApplication.activeWindow())
        self.rightSideInfo.setMinimumSize(300,500)

        self.rightSideLayout.addWidget(self.rightSideInfo)

    def showAlarm(self):
        self.rightSideInfo.close()
        self.rightSideInfo = alarm.alarm(self,self.studId)#clientSocket이랑 학번이 필요함
        self.rightSideInfo.setMinimumSize(300,500)

        self.rightSideLayout.addWidget(self.rightSideInfo)

    def showLeader(self):
        self.rightSideInfo.close()
        self.rightSideInfo = leader.LeaderBoard(self,self.studId)
        self.rightSideInfo.setMinimumSize(300,500)
        self.rightSideLayout.addWidget(self.rightSideInfo)


    def showSetting(self):
        self.rightSideInfo.close()
        self.rightSideInfo = setting.setting(self)
        self.rightSideLayout.addWidget(self.rightSideInfo)

    def quitClicked(self):
        # commend = 'exit'
        # self.clientSocket.send(commend.encode('utf-8'))
        # QApplication.quit()
        self.w.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = App()
    form.show()
    exit(app.exec_())