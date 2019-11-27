import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from socket import *
import time
import reply
import chat_search
import chat_mine
import pandas as pd

class update_listener(QThread):
    chatUpdate = pyqtSignal(list)

    def __init__(self,parent = None):
        super().__init__()
        self.parent = parent
        self.chatSocket = parent.chatSocket
        self.go = True
    def run(self):
        while self.go:
            time.sleep(1)  # 클라이언트 처리 과부하 방지

            update_commend = self.chatSocket.recv(1024)
            update_commend = update_commend.decode('utf-8')
            update_commend = update_commend.split(',')

            if len(update_commend) != 1:
                if update_commend[0] == 'update':
                    tmp = []
                    # print(update_commend)
                    if len(update_commend) == 8:
                        for i in range(1, len(update_commend)):
                            tmp.append(update_commend[i])
                    elif len(update_commend) > 8:
                        msglen = len(update_commend) - 8
                        msg = ",".join(update_commend[3:4 + msglen])

                        for i in range(msglen + 1):
                            del update_commend[3]
                        update_commend.insert(3, msg)
                        # print(update_commend)

                        for i in range(1, len(update_commend)):
                            tmp.append(update_commend[i])
                        # print(tmp)

                    self.chatUpdate.emit(tmp)
                    # print('업데이트 시그널 emit')
                elif update_commend[0] == 'stop':
                    self.go = False
                    # print('멈춤')

            else:
                if update_commend =='stop':
                    self.go = False
                    # print('멈춤')
                    # break


class chatRoom(QWidget):
    def __init__(self,parent):
        super().__init__()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setOffset(3)
        self.setGraphicsEffect(shadow)

        #필수 변수
        self.parent = parent
        self.user = parent.w.user
        self.clientSocket = self.parent.w.clientSock
        self.lecId = self.getLecId()
        self.sendType = True
        self.comment_info = 0
        self.tab = QTabWidget()
        self.getCategory()

        #chat server와 연결
        self.chatSocket= socket(AF_INET, SOCK_STREAM)
        # self.chatSocket.connect(('192.168.0.31', 3334))
        self.chatSocket.connect(('192.168.43.180', 3334))
        # self.chatSocket.connect(('192.168.25.22', 3334))
        # self.chatSocket.connect(('34.84.112.149', 3334))

        self.history = self.getChatHistory()
        self.tab.currentChanged.connect(self.category_changed)

        #디자인
        self.showLayout = QVBoxLayout()
        self.mainLayout = QVBoxLayout()
        self.mainWidget = QWidget()
        self.mainLayout.setSpacing(0)

        #타이틀 -> 강의이름/타이틀바
        self.titleWidget = QWidget()
        self.titleWidget.setStyleSheet('background-color:#a1d2d7')
        self.titleLayout = QVBoxLayout()
        self.titleLayout.setContentsMargins(10,10,10,10)

        self.titleLayoutTop = QHBoxLayout()
        self.titleLayoutMid = QHBoxLayout()
        self.titleLayoutBot = QHBoxLayout()

        self.titleLayout.addLayout(self.titleLayoutTop)
        self.titleLayout.addLayout(self.titleLayoutMid)
        self.titleLayout.addLayout(self.titleLayoutBot)
        self.titleWidget.setLayout(self.titleLayout)
        self.titleWidget.setMaximumHeight(120)
        self.titleWidget.setMinimumWidth(500)

        #채팅 내용
        self.chatContentLayout = QVBoxLayout()
        self.chatWidget = QWidget()
        #e8f3f4
        self.chatWidget.setStyleSheet('background-color:#e8f3f4; border:0px')
        self.chatLayout = QVBoxLayout()
        self.chatWidget.setLayout(self.chatLayout)
        self.chatContentLayout.addWidget(self.chatWidget)

        #입력창
        self.chat_input = QLineEdit()
        self.chat_input.setStyleSheet('background:white; height:100px')
        self.chat_input.returnPressed.connect(lambda: self.sendMsg(self.chat_input.text()))  # 엔터 처리
        #a1d2d7
        self.chatLayoutWidget = QWidget()
        self.chatLayoutWidget.setStyleSheet('background-color:#a1d2d7')
        self.chatLayoutWidget.setMinimumHeight(100)
        self.chatInputLayout = QHBoxLayout()
        self.chatLayoutWidget.setLayout(self.chatInputLayout)

        #메인 레이아웃 설정
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.titleWidget)
        # self.mainLayout.addWidget(self.chatWidget)
        self.mainLayout.addLayout(self.chatContentLayout)

        self.mainLayout.addWidget(self.chatLayoutWidget)

        self.mainWidget.setLayout(self.mainLayout)

        self.showLayout.addWidget(self.mainWidget)
        self.showLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.showLayout)
        self.setMinimumSize(500,800)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.initUI()

    def initUI(self):
        # 쓰레드
        self.t = update_listener(parent=self)
        self.t.chatUpdate.connect(self.chat_Update)
        self.t.start()

        #타이틀
        # 최소화
        btMini = QPushButton()
        btMini.setStyleSheet('''border:0px''')
        btMini.setIcon(QIcon('./icon/minimize.png'))
        btMini.setIconSize(QSize(15, 15))
        btMini.clicked.connect(lambda: QApplication.activeWindow().showMinimized())

        # 종료
        btExit = QPushButton()
        btExit.setStyleSheet('''border:0px''')
        btExit.setIcon(QIcon('./icon/icons8-close-window-16.png'))
        btExit.setIconSize(QSize(15, 15))
        btExit.clicked.connect(self.quitClicked)

        BtnSearch  = QPushButton()
        BtnSearch.setStyleSheet('''border:0px''')
        BtnSearch.setIcon(QIcon('./ui/chatting_ui/find.png'))
        BtnSearch.setIconSize(QSize(30,30))
        BtnSearch.clicked.connect(self.searchClicked)
        
        BtnMine  = QPushButton()
        BtnMine.setStyleSheet('''border:0px''')
        BtnMine.setIcon(QIcon('./ui/chatting_ui/내질문3.png'))
        BtnMine.setIconSize(QSize(80,30))
        BtnMine.clicked.connect(self.mineClicked)


        self.titleLayoutTop.addStretch(1)
        self.titleLayoutTop.addWidget(btMini,alignment=QtCore.Qt.AlignRight)
        self.titleLayoutTop.addWidget(btExit,alignment=QtCore.Qt.AlignRight)

        #강의명
        lecName = QLabel(self.parent.course[0])
        lecName.setStyleSheet('font-weight:bold; font:13pt 나눔스퀘어라운드 Regular;color:#27565b')

        self.titleLayoutMid.addWidget(lecName,alignment=QtCore.Qt.AlignLeft)

        #강의 정보
        profName = QLabel(self.parent.course[1])
        profName.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;color:#27565b')

        download = QPushButton()
        download.clicked.connect(self.sendQuestionToEmail)
        download.setMaximumWidth(30)
        download.setStyleSheet('border:0px')
        download.setIcon(QIcon('./ui/chatting_ui/download.png'))
        download.setIconSize(QSize(30,30))
        self.titleLayoutBot.addWidget(profName,alignment=QtCore.Qt.AlignLeft)
        self.titleLayoutBot.addStretch(1)
        self.titleLayoutBot.addWidget(BtnMine)
        self.titleLayoutBot.addWidget(BtnSearch)
        self.titleLayoutBot.addWidget(download)

        #질문 목록
        question_layout = QVBoxLayout()
        question_layout.setContentsMargins(10,10,10,10)

        btn_category_add = QToolButton()
        self.tab.setCornerWidget(btn_category_add, Qt.TopLeftCorner)  # 버튼 위치
        btn_category_add.setAutoRaise(True)  # 마우스가 올라오면 올라옴
        btn_category_add.clicked.connect(self.add_new_tab)
        btn_category_add.setIcon(QIcon("./icon/add.png"))
        question_layout.addWidget(self.tab)

        self.showQuestions()

        self.chatLayout.addLayout(question_layout)
        self.chatLayout.setContentsMargins(0,0,0,0)

        #채팅입력
        chat_enter = QPushButton()
        #chat_enter.setStyleSheet('background:#F6F6F3;image:url(./ui/chatting_ui/보내기.png); border:0px;')
        chat_enter.setStyleSheet('''
                        QPushButton{image:url(./ui/chatting_ui/보내기.png); border:0px; width:60px; height:80px}        
                        
                        ''')
        # chat_enter.setMinimumHeight(78)
        # chat_enter.setIcon(QIcon('./icon/send.png'))
        # chat_enter.setIconSize(QSize(50,50))
        chat_enter.clicked.connect(lambda: self.sendMsg(self.chat_input.text()))

        self.chatInputLayout.addWidget(self.chat_input)
        self.chatInputLayout.addWidget(chat_enter)

        self.show()

    def chat_Update(self,msg):
        #새로 업데이트된 메시지만 위젯에 추가함
        item = QListWidgetItem(self.tab.currentWidget())

        custom_widget = chatWidget(self,msg,self.parent)
        item.setSizeHint(custom_widget.sizeHint())
        self.tab.currentWidget().setItemWidget(item, custom_widget)
        self.tab.currentWidget().addItem(item)
        self.tab.update()
        self.tab.currentWidget().scrollToBottom()

    def quitClicked(self):
        commend = 'exit'
        self.chatSocket.send(commend.encode('utf-8'))
        #쓰레드 삭제
        self.t.quit()
        # self.close()
        self.hide()

    def category_changed(self):
        self.tab.currentWidget().clear()
        self.history = self.getChatHistory()
        # if len(self.history) != 0:
        #     self.history.pop()
        self.showQuestions()

    def getCategory(self):
        commend = "getCategory " + self.lecId
        self.clientSocket.send(commend.encode('utf-8'))

        category = self.clientSocket.recv(1024)
        category = category.decode('utf-8')
        # print(category)

        category = category.split(',')
        category.pop()

        for i in range(len(category)):
            self.tab.addTab(QListWidget(self), category[i])

    def sendQuestionToEmail(self):
        dlg = sendQuestion(self)
        dlg.exec_()

    def showQuestions(self):
        print(self.history)
        for i in range(len(self.history)):
            item = QListWidgetItem(self.tab.currentWidget())

            custom_widget = chatWidget(self,self.history[i],self.parent)
            item.setSizeHint(custom_widget.sizeHint())
            self.tab.currentWidget().setItemWidget(item, custom_widget)
            self.tab.currentWidget().addItem(item)
        self.tab.currentWidget().scrollToBottom()


    def getLecId(self):
        commend = "get_lecture_id "+self.parent.course[-1]

        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(1024)

        return result.decode('utf-8')

    
    def searchClicked(self):
        self.search = chat_search.Search(self,self.parent.course[-1],self.tab.tabText(self.tab.currentIndex()))

        self.search.setWindowTitle("Search")
        self.search.setMinimumSize(QSize(400, 400))

    def mineClicked(self):
        self.mine = chat_mine.Mine(self,self.parent.stuid,self.parent.course[-1],self.tab.tabText(self.tab.currentIndex()))

        self.mine.setWindowTitle("Mine")
        self.mine.setMinimumSize(QSize(400, 400))
    
    
    def getChatHistory(self):
        commend = 'chat_history '+ self.lecId + " " + self.tab.tabText(self.tab.currentIndex())
        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(2048)
        print(len(result))
        result = result.decode('utf-8')

        if result == 'x':
            return []

        else:
            result = result.split('/')
            question = []

            for i in range(len(result)):
                tmp = result[i].split(',')
                tmp = [x for x in tmp if x]

                if len(tmp) == 7:
                    question.append(tmp)

                elif len(tmp) > 7:
                    msglen = len(tmp) - 7
                    msg = ",".join(tmp[2:3+msglen])

                    for i in range(msglen+1):
                        del tmp[2]
                    tmp.insert(2,msg)
                    question.append(tmp)
            return question

    def add_new_tab(self):
        dlg = category_create(QApplication.activeWindow(),self)
        dlg.exec_()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def sendMsg(self,msg):
        self.chat_input.setText('')
        if self.sendType == False:
            commend = 'sendReplyMsg ' + self.comment_info[6] + " " + self.parent.stuid + " " + msg
            # print(commend)

            # main server에 알림
            self.clientSocket.send(commend.encode('utf-8'))

            tmp = self.clientSocket.recv(1024)
            # print(tmp)
            self.chatWidget.refresh()
            # chat server에 전송 -> 모두에게 뿌리기 위해
            # self.chatSocket.send('chat_update'.encode('utf-8'))
        else:
            commend = 'sendMsg ' + self.tab.tabText(self.tab.currentIndex()) + " "+ self.lecId + " " + msg + " " + self.parent.stuid

            #main server에 알림
            self.clientSocket.send(commend.encode('utf-8'))

            tmp = self.clientSocket.recv(1024)
            tmp = tmp.decode('utf-8')

            chat_id = tmp.split(' ')
            #chat server에 전송 -> 모두에게 뿌리기 위해
            data = 'chat_update '+chat_id[1]
            self.chatSocket.send(data.encode('utf-8'))

class category_create(QDialog):
    def __init__(self,window,parent):
        super().__init__()
        QApplication.setActiveWindow(window)
        self.parent=parent
        self.clientSocket = self.parent.clientSocket

        self.mainLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMinimumSize(150,150)
        self.initUi()

    def initUi(self):
        category_input = QLineEdit()
        category_input.setPlaceholderText('카테고리명')
        create = QPushButton('생성')
        cancel = QPushButton('취소')

        cancel.clicked.connect(self.close)
        self.btnLayout.addWidget(create)
        self.btnLayout.addWidget(cancel)
        create.clicked.connect(lambda: self.create_category(category_input.text()))

        self.mainLayout.addWidget(category_input)
        self.mainLayout.addLayout(self.btnLayout)
        self.setLayout(self.mainLayout)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def create_category(self, name):
        #db로 보내서 등록하고 탭 늘려야됨
        commend = 'category_create ' + self.parent.lecId + " " + name
        # print(commend)
        self.clientSocket.send(commend.encode('utf-8'))

        new_tab = QListWidget(self)
        self.parent.tab.addTab(new_tab, name)
        self.close()

class chatWidget(QWidget):
    def __init__(self,parent,comments,grandparent):
        super().__init__()
        self.parent = parent
        self.grandparent = grandparent

        self.mainLayout = QHBoxLayout()
        self.questLayoutinMain = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.clientSocket = parent.clientSocket

        #comments 참조 순서 studid,name,comment,like,category_id,time,chat_id
        self.comments = comments
        self.initUI()

    def initUI(self):
        if len(self.comments) != 2:
            self.BtnLike = QPushButton(self.comments[3])
            self.BtnLike.setIcon(QIcon('./icon/heart_unchecked.png'))
            self.BtnLike.setStyleSheet('''
            QPushButton{border:0px; background-color:#e8f3f4; width:45px}''')
            self.BtnLike.setIconSize(QSize(30,30))
            #BtnLike.setMaximumWidth()
            self.BtnLike.clicked.connect(self.likeClicked)

            question = QLabel()
            #42939c#24565b
            question.setText(self.comments[2])
            question.setStyleSheet("color: black;"
                               "background-color: white;"
                               "border-style: solid;"
                               "border-width: 1px;"
                               "border-color: #42939c;"
                               "font:9pt 나눔스퀘어라운드 Regular;"
                               )
            question.setFixedHeight(38)
            question.setFixedWidth(360)

            date = QLabel()
            date.setText(self.comments[5])

        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.addStretch(1)
        self.questLayoutinMain.addWidget(question)
        self.questLayoutinMain.addWidget(date)
        self.mainLayout.addLayout(self.questLayoutinMain)
        self.mainLayout.addWidget(self.BtnLike)
        self.mainLayout.addStretch(1)

    def likeClicked(self):
        # print(self.comments)
        commend = 'like_update '+ self.comments[6] + " " + self.grandparent.stuid#학번 + msg
        self.clientSocket.send(commend.encode('utf-8'))
        # print(commend)
        result = self.clientSocket.recv(1024)
        result = result.decode('utf-8')

        self.BtnLike.setText(result)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            #질문 목록 위젯 닫음
            self.parent.chatWidget.close()

            #메시지 전송 타입 답글로 변경
            self.parent.sendType = False

            #리플 위젯 생성 및 변수값 대입
            replyWidget = reply.Reply(self.parent)
            self.parent.comment_info = self.comments
            # replyWidget = self.parent.reply
            replyWidget.widgetTmp = self.parent.chatWidget
            replyWidget.clientSocket = self.clientSocket

            self.parent.chatWidget = replyWidget

            #리플 위젯 화면 뿌려주기
            self.parent.chatWidget.comment_info = self.comments
            self.parent.chatWidget.replyList = self.parent.chatWidget.getReply()
            self.parent.chatWidget.showReply()
            self.parent.chatContentLayout.addWidget(self.parent.chatWidget)
        
        elif QMouseEvent.button() == Qt.RightButton:
            print("Right Button Clicked")
            dlg = studentInfo(self)
            dlg.exec_()

class studentInfo(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.initUi()

        print(self.parent.comments)

    def initUi(self):
        head = QLabel('정보')
        head.setStyleSheet('font-weight:bold; font-size:13pt')

        # 학생 정보
        self.name = QLabel('이름')
        self.depart = QLabel('소속')
        self.student_id = QLabel('학번')

        # 버튼
        check = QPushButton('확인')
        check.clicked.connect(self.close)

        self.btnLayout.addWidget(check)

        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(head)
        self.mainLayout.addWidget(self.name)
        self.mainLayout.addWidget(self.depart)
        self.mainLayout.addWidget(self.student_id)
        self.mainLayout.addLayout(self.btnLayout)
        self.mainLayout.addStretch(1)

        self.student_info()

        self.setFixedSize(200, 150)
        self.setLayout(self.mainLayout)

    def student_info(self):
        commend = 'getProfile ' + self.parent.comments[0]
        self.parent.clientSocket.send(commend.encode('utf-8'))

        info = self.parent.clientSocket.recv(1024).decode('utf-8')
        info = info.split(',')

        self.name.setText('이름: '+info[5])
        self.depart.setText('학과: '+info[1])
        self.student_id.setText('학번: '+self.parent.comments[0])



    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

class sendQuestion(QDialog):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.initUi()

    def initUi(self):
        head = QLabel('질문 전송')
        head.setStyleSheet('font-weight:bold; font-size:13pt')
        self.email = QLabel(self.parent.user['email']+'@ajou.ac.kr')
        send = QPushButton('전송')
        send.clicked.connect(self.sendToEmail)
        cancel = QPushButton('취소')
        cancel.clicked.connect(self.close)

        self.btnLayout.addWidget(send)
        self.btnLayout.addWidget(cancel)

        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(head)
        self.mainLayout.addWidget(self.email)
        self.mainLayout.addLayout(self.btnLayout)
        self.mainLayout.addStretch(1)

        self.setFixedSize(200,150)
        self.setLayout(self.mainLayout)


    def sendToEmail(self):
        #이메일로 전송할 목록 정할수있게 해야할듯
        commend = "sendToEmail " + self.parent.tab.tabText(self.parent.tab.currentIndex()) + " " + self.parent.lecId + " "+ self.email.text()
        self.parent.clientSocket.send(commend.encode('utf-8'))

        res = self.parent.clientSocket.recv(1024).decode('utf-8')

        if res == 'success':
            self.close()
            send_ok = QMessageBox()
            send_ok.setStyleSheet("background-color:#FFFFFF")
            send_ok.setText('전송 되었습니다')
            send_ok.exec_()


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = chatRoom()
    sys.exit(app.exec_())