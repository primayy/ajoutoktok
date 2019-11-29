import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from socket import *
import time


class Mine(QWidget):
    def __init__(self,parent,stdid,LeCode,tabId):
        super().__init__()
        #변수 설정
        self.parent = parent
        self.clientSocket = self.parent.parent.w.clientSock
        self.comment_info = 0
        self.mineList = 0
        self.tabId = tabId
        self.student_id = stdid
        self.lecture_code = LeCode
        self.widgetTmp = QWidget()

        #효과 설정
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


        #위젯에 다른 위젯 추가하기 위한 레이아웃 선언
        self.widgetLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.widgetLayout)

        #메인 레이아웃에 메인 위젯 추가

        self.mainLayout.addWidget(self.mainWidget)


        self.setLayout(self.mainLayout)
        self.setMinimumSize(500, 400)
        self.setStyleSheet('background-color:white')

        self.initUI()

    def initUI(self):
        #화면 구성요소

        #질문 목록
        self.question_mine = QListWidget()
        self.question_mine.scrollToBottom()
        self.question_mine.setBaseSize(500, 200)
        self.question_mine.setMaximumSize(500,200)

        self.question_mine.setStyleSheet('''
                        # QListWidget:item:hover{background:white};
                        # QListWidget:item{padding:0px}
                        ''')
        self.question_mine.clear()
        self.mineList = self.getMine()
        for i in range(len(self.mineList)):
            item = QListWidgetItem(self.question_mine)
            

            custom_widget = mineWidget(self.mineList[i],self.parent)
            item.setSizeHint(custom_widget.sizeHint())
            self.question_mine.setItemWidget(item, custom_widget)

                        

        #widgetLayout에 추가
        self.widgetLayout.addWidget(self.question_mine)

        self.show()

    #뒤로가기 버튼 눌렀을시
    def returnToChat(self):
        self.close()
        self.parent.chatWidget = self.widgetTmp

        self.parent.sendType = True
        self.widgetTmp.show()

    #질문에 대한 답글 읽어옴
    def getMine(self):
        commend = 'ChatMine ' + self.student_id +" "+ self.lecture_code+" "+self.tabId

        self.clientSocket.send(commend.encode('utf-8'))
        
        mine = self.clientSocket.recv(1024)
        mine = mine.decode('utf-8')

        if mine == 'x':
            return []

        else:
            mine = mine.split('/')

            mine.pop()
            mineResult = []

            for i in range(len(mine)):
                mineResult.append(mine[i])

            return mineResult


class mineWidget(QWidget):
    def __init__(self,comments, parent):
        super().__init__()
        self.parent = parent
        self.comments = comments

        self.replyLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.initUI()

    def initUI(self):

        Mined = QLabel()
        Mined.setText(self.comments)

        self.replyLayout.addWidget(Mined)
        self.mainLayout.addLayout(self.replyLayout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mine(0)
    sys.exit(app.exec_())