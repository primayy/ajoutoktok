import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import reply
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
        self.setMinimumSize(500, 300)
        self.setMaximumSize(500, 300)
        self.setStyleSheet('background-color:#eef5f6')

        self.initUI()

    def initUI(self):
        #화면 구성요소
        myquestion = QLabel('내 질문 모아보기')
        myquestion.setStyleSheet('font:13pt 나눔스퀘어라운드 Regular;color:#42808a;')
        #질문 목록
        self.question_mine = QListWidget()
        self.question_mine.scrollToBottom()
        #self.question_mine.setBaseSize(500, 200)
        self.question_mine.setMaximumSize(450,300)

        self.question_mine.setStyleSheet('''
                        # QListWidget:item:hover{background:#a1d2d7};
                        # QListWidget:item{padding:0px}
                        ''')
        self.question_mine.setContentsMargins(0,0,0,0)
        self.question_mine.clear()
        self.mineList = self.getMine()
        for i in range(len(self.mineList)):
            item = QListWidgetItem(self.question_mine)
            custom_widget = mineWidget(self.mineList[i],self.parent,self)
            item.setSizeHint(custom_widget.sizeHint())
            self.question_mine.setItemWidget(item, custom_widget)



        #widgetLayout에 추가
        self.widgetLayout.addWidget(myquestion)
        self.widgetLayout.addWidget(self.question_mine)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()

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

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)

        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    

class mineWidget(QWidget):
    def __init__(self,comments, chatParent,parent):
        super().__init__()
        #질문 위젯
        self.chatParent = chatParent
        #내질문 위젯
        self.parent = parent

        self.comments = comments.split(',')
        self.clientSocket = chatParent.clientSocket
        self.replyLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.setStyleSheet('background-color:#eef5f6;')

        self.initUI()

    def initUI(self):
        #Mined2 = QTextBrowser()
        Mined2 = QLabel()
        Mined2.setMaximumHeight(70)
        Mined2.setMinimumSize(400,70)
        Mined2.setStyleSheet('border:0px solid;background:white;')
        Mined2.setContentsMargins(0,0,0,0)
        Mined2.setText(self.comments[2])

        self.replyLayout.addWidget(Mined2)
        
        self.mainLayout.addLayout(self.replyLayout)
        
        self.mainLayout.setContentsMargins(5,5,5,5)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            #질문 목록 위젯 닫음
            self.chatParent.chatWidget.close()

            #메시지 전송 타입 답글로 변경
            self.chatParent.sendType = False
            #리플 위젯 생성 및 변수값 대입
            self.chatParent.comment_info = self.comments
            self.tmpSocket = self.chatParent.clientSocket
            self.chatParent.clientSocket = self.clientSocket
            replyWidget = reply.Reply(self.chatParent)
            replyWidget.widgetTmp = self.chatParent.chatWidget
            replyWidget.clientSocket = self.clientSocket
            self.chatParent.clientSocket = self.tmpSocket

            self.chatParent.chatWidget = replyWidget

            #리플 위젯 화면 뿌려주기
            self.chatParent.chatWidget.comment_info = self.comments
            self.chatParent.chatWidget.replyList = self.chatParent.chatWidget.getReply()
            self.chatParent.chatWidget.showReply()
            self.chatParent.chatContentLayout.addWidget(self.chatParent.chatWidget)

            # # 내 질문 목록 위젯 닫음
            self.parent.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mine(0)
    sys.exit(app.exec_())