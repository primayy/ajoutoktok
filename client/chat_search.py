import sys
import reply
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from socket import *
import time


class Search(QWidget):
    def __init__(self,parent,LeCode,tabId):
        super().__init__()
        #변수 설정
        self.parent = parent
        self.clientSocket = self.parent.parent.w.clientSock
        self.comment_info = 0
        self.lecture_code = LeCode
        self.tabId = tabId
        self.searchList = 0
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
        self.mainWidget.setStyleSheet('background-color:#eef5f6')

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

        #서치 바 레이아웃
        self.searchbar_layout = QHBoxLayout()

        self.setLayout(self.mainLayout)
        self.setMinimumSize(500, 400)
        self.setStyleSheet('background-color:white')

        self.initUI()

    def initUI(self):
        #화면 구성요소
        #위젯은 widgetLayout에 추가하면 됨
        question_search = QLabel('질문 검색')
        question_search.setStyleSheet('font:13pt 나눔스퀘어라운드 Regular;color:#42808a;')

        self.search_input = QLineEdit()
        self.search_input.setStyleSheet('background:white')
        
        self.search_input.setMinimumWidth(250)
        btnSearch = QPushButton('검색')
        btnSearch.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;color:#42808a;')
        btnSearch.clicked.connect(self.search)


        #질문 목록
        self.question_search = QListWidget()
        self.question_search.scrollToBottom()
        #self.question_search.setBaseSize(500, 300)
        self.question_search.setMaximumSize(480,280)
        self.question_search.setMinimumSize(480,280)

        self.question_search.setStyleSheet('''
                        # QListWidget:item:hover{background:white};
                        # QListWidget:item{padding:0px}
                        ''')
        # 종료
        btExit = QPushButton()
        btExit.setStyleSheet('''border:0px''')
        btExit.setIcon(QIcon('./icon/close.png'))
        btExit.setIconSize(QSize(15,15))
        btExit.setFocusPolicy(Qt.NoFocus)
        btExit.clicked.connect(self.quitClicked)

        #widgetLayout에 추가
        
        self.searchbar_layout.addWidget(self.search_input)
        self.searchbar_layout.addWidget(btnSearch)
        # self.widgetLayout.addWidget(self.search_input)
        # self.widgetLayout.addWidget(btnSearch)
        self.widgetLayout.addWidget(btExit, alignment=QtCore.Qt.AlignRight)
        self.widgetLayout.addWidget(question_search)
        self.widgetLayout.addLayout(self.searchbar_layout)
        self.widgetLayout.addWidget(self.question_search)
        self.widgetLayout.addStretch(1)
        self.widgetLayout.setContentsMargins(30,30,30,30)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()

    def quitClicked(self):
        self.hide()

    def search(self):
        self.question_search.clear()
        self.searchList = self.getSearch()
        for i in range(len(self.searchList)):
            item = QListWidgetItem(self.question_search)

            custom_widget = searchWidget(self.searchList[i],self.parent, self)
            item.setSizeHint(custom_widget.sizeHint())
            self.question_search.setItemWidget(item, custom_widget)
            self.question_search.addItem(item)
        self.question_search.scrollToBottom()

    #질문에 대한 답글 읽어옴
    def getSearch(self):
        commend = 'ChatSearch ' + self.search_input.text() +" "+ self.lecture_code +" "+self.tabId

        self.clientSocket.send(commend.encode('utf-8'))
        
        searched = self.clientSocket.recv(1024)
        searched = searched.decode('utf-8')

        if searched == 'x':
            return []

        else:
            searched = searched.split('/')

            searched.pop()
            searchedResult = []

            for i in range(len(searched)):
                searchedResult.append(searched[i])

            return searchedResult

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)

        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

class searchWidget(QWidget):
    def __init__(self, comments, chatParent, parent):
        super().__init__()
        # 질문 위젯
        self.chatParent = chatParent
        # 내질문 위젯
        self.parent = parent

        self.comments = comments.split(',')
        self.clientSocket = chatParent.clientSocket

        self.searchLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.initUI()

    def initUI(self):
        #searched2 = QTextBrowser()
        searched2 = QLabel()
        searched2.setMaximumHeight(40)
        searched2.setMinimumSize(400,40)
        searched2.setStyleSheet('border:0px solid;background:white;font:9pt 나눔스퀘어라운드 Regular;')
        searched2.setContentsMargins(0,0,0,0)
        searched2.setText(self.comments[2])

        self.searchLayout.addWidget(searched2)
        self.mainLayout.addLayout(self.searchLayout)
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
    ex = Search(0)
    sys.exit(app.exec_())