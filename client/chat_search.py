import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from socket import *
import time


class Search(QWidget):
    def __init__(self,parent,LeCode):
        super().__init__()
        #변수 설정
        self.parent = parent
        self.clientSocket = self.parent.parent.w.clientSock
        self.comment_info = 0
        self.lecture_code = LeCode
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
        self.mainWidget.setStyleSheet('background-color:white')

        #질문 타이틀 레이아웃
        self.questionWidget = QWidget()
        self.questionWidget.setStyleSheet('background-color:grey;')
        self.question_title_bottom = QHBoxLayout()

        #타이틀 관련 위젯은 questionLayout에 추가
        self.questionLayout = QVBoxLayout()
        self.questionWidget.setLayout(self.questionLayout)
        self.questionWidget.setMaximumSize(500,200)
        # self.questionLayout.setContentsMargins(0,0,0,0)


        #위젯에 다른 위젯 추가하기 위한 레이아웃 선언
        self.widgetLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.widgetLayout)

        #메인 레이아웃에 메인 위젯 추가

        self.mainLayout.addWidget(self.mainWidget)


        self.setLayout(self.mainLayout)
        self.setMinimumSize(500, 400)
        self.setStyleSheet('background-color:white')
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.initUI()

    def initUI(self):
        #화면 구성요소
        #위젯은 widgetLayout에 추가하면 됨

    
        self.search_input = QTextEdit()
        self.search_input.setStyleSheet('background:white')

        btnSearch = QPushButton('검색')
        btnSearch.clicked.connect(self.search)


        #질문 목록
        self.question_search = QListWidget()
        self.question_search.scrollToBottom()
        self.question_search.setBaseSize(500, 200)
        self.question_search.setMaximumSize(500,200)

        self.question_search.setStyleSheet('''
                        # QListWidget:item:hover{background:white};
                        # QListWidget:item{padding:0px}
                        ''')

        #widgetLayout에 추가
        self.widgetLayout.addWidget(self.search_input)
        self.widgetLayout.addWidget(btnSearch)
        self.widgetLayout.addWidget(self.question_search)

        self.show()

    def search(self):
        self.question_search.clear()
        self.searchList = self.getSearch()
        for i in range(len(self.searchList)):
            item = QListWidgetItem(self.question_search)

            custom_widget = searchWidget(self.searchList[i],self.parent)
            item.setSizeHint(custom_widget.sizeHint())
            self.question_search.setItemWidget(item, custom_widget)
            self.question_search.addItem(item)
        self.question_search.scrollToBottom()

        # self.question_search.update()

    #뒤로가기 버튼 눌렀을시
    def returnToChat(self):
        self.close()
        self.parent.chatWidget = self.widgetTmp
        print(self.parent.sendType)
        self.parent.sendType = True
        self.widgetTmp.show()

    #질문에 대한 답글 읽어옴
    def getSearch(self):
        commend = 'ChatSearch ' + self.search_input.toPlainText() +" "+ self.lecture_code
        print(commend)
        self.clientSocket.send(commend.encode('utf-8'))
        
        searched = self.clientSocket.recv(1024)
        searched = searched.decode('utf-8')

        if searched == 'x':
            return []

        else:
            searched = searched.split('/')
            print(searched)
            searched.pop()
            searchedResult = []

            for i in range(len(searched)):
                searchedResult.append(searched[i])

            return searchedResult


class searchWidget(QWidget):
    def __init__(self,comments, parent):
        super().__init__()
        self.parent = parent
        self.comments = comments

        self.searchLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.initUI()

    def initUI(self):

        searched = QLabel()
        searched.setText(self.comments)

        self.searchLayout.addWidget(searched)
        self.mainLayout.addLayout(self.searchLayout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Search(0)
    sys.exit(app.exec_())