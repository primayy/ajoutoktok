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
import msget

import calendarW

class update_listener(QThread):
    chatUpdate = pyqtSignal(list)

    def __init__(self,parent = None):
        super().__init__()
        self.parent = parent
        self.chatSocket = parent.chatSocket
        self.go = True

    def run(self):
        while self.go:
            time.sleep(0.3)  # 클라이언트 처리 과부하 방지

            update_commend = self.chatSocket.recv(30000)
            update_commend = update_commend.decode('utf-8')
            update_commend = update_commend.split(',')
            print("update_commend: "+str(update_commend))
            if len(update_commend) != 1:
                if update_commend[0] == 'update':
                    tmp = []
                    if len(update_commend) == 11:
                        for i in range(1, len(update_commend)):
                            tmp.append(update_commend[i])
                    elif len(update_commend) > 11:
                        msglen = len(update_commend) - 11
                        msg = ",".join(update_commend[3:4 + msglen])

                        for i in range(msglen + 1):
                            del update_commend[3]
                        update_commend.insert(3, msg)

                        for i in range(1, len(update_commend)):
                            tmp.append(update_commend[i])

                    self.chatUpdate.emit(tmp)
                elif update_commend[0] == 'stop':
                    self.go = False

            else:
                if update_commend[0] =='stop':
                    self.go = False
                elif update_commend[0] =='connection_success':
                    print("QQQ")


class chatRoom(QWidget):
    def __init__(self,parent,msgetted):
        super().__init__()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setOffset(3)
        self.setGraphicsEffect(shadow)

        #필수 변수
        self.parent = parent
        self.msgetted = msgetted
        self.msgWidgetPos = None
        self.user = parent.w.user
        self.clientSocket = self.parent.w.clientSock
        self.lecId = self.getLecId()
        self.sendType = True
        self.comment_info = 0
        self.tab = QTabWidget()

        self.getCategory()

        #chat server와 연결
        self.chatSocket= socket(AF_INET, SOCK_STREAM)
        # self.chatSocket.connect(('192.168.0.17', 3334))
        # self.chatSocket.connect(('192.168.43.36', 3334))
        #self.chatSocket.connect(('192.168.0.8',3334))
        self.chatSocket.connect(('192.168.25.22', 3334))
        # self.chatSocket.connect(('35.200.112.11', 3334))
        #self.chatSocket.connect(('172.30.1.21', 3334))
        # self.chatSocket.connect(('192.168.0.17', 3334))

        
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
        self.mainLayout.addLayout(self.chatContentLayout)

        self.mainLayout.addWidget(self.chatLayoutWidget)

        self.mainWidget.setLayout(self.mainLayout)

        self.showLayout.addWidget(self.mainWidget)
        self.showLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.showLayout)
        self.setMinimumSize(500,700)
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
        btMini.setIcon(QIcon('./icon/minimize2.png'))
        btMini.setIconSize(QSize(17, 17))
        btMini.clicked.connect(lambda: QApplication.activeWindow().showMinimized())

        # 종료
        btExit = QPushButton()
        btExit.setStyleSheet('''border:0px''')
        btExit.setIcon(QIcon('./icon/close.png'))
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
        self.profName = QLabel(self.parent.course[1])
        self.profName.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;color:#27565b')

        download = QPushButton()
        download.clicked.connect(self.sendQuestionToEmail)
        download.setMaximumWidth(30)
        download.setStyleSheet('border:0px')
        download.setIcon(QIcon('./ui/chatting_ui/download.png'))
        download.setIconSize(QSize(30,30))
        self.titleLayoutBot.addWidget(self.profName,alignment=QtCore.Qt.AlignLeft)
        self.titleLayoutBot.addStretch(1)
        self.titleLayoutBot.addWidget(BtnMine)
        self.titleLayoutBot.addWidget(BtnSearch)
        self.titleLayoutBot.addWidget(download)

        #질문 목록
        question_layout = QVBoxLayout()
        question_layout.setContentsMargins(10,10,10,10)

        if self.user['is_prof'] == 1:
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
        chat_enter.setStyleSheet('''
                        QPushButton{image:url(./ui/chatting_ui/보내기.png); border:0px; width:60px; height:80px}        
                        
                        ''')

        chat_enter.clicked.connect(lambda: self.sendMsg(self.chat_input.text()))

        self.chatInputLayout.addWidget(self.chat_input)
        self.chatInputLayout.addWidget(chat_enter)
        commend ="chat_client " + str(self.parent.course[1]) +" "+ str(self.tab.tabText(self.tab.currentIndex()))#과목코드 + 카테고리명
        self.chatSocket.send(commend.encode('utf-8'))
        self.show()

    def chat_Update(self,msg):
        self.tab.currentWidget().setStyleSheet('QListWidget:item:hover{background:#e8f3f4};')
        #새로 업데이트된 메시지만 위젯에 추가함
        item = QListWidgetItem(self.tab.currentWidget())
        print("msg: "+str(msg))
        custom_widget = chatWidget(self,msg,self.parent)
        item.setSizeHint(custom_widget.sizeHint())
        self.tab.currentWidget().setItemWidget(item, custom_widget)
        self.tab.currentWidget().addItem(item)
        #self.tab.currentWidget().setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab.update()
        self.tab.currentWidget().scrollToBottom()

    def quitClicked(self):

        commend = 'exit'
        self.chatSocket.send(commend.encode('utf-8'))
        #쓰레드 삭제
        self.t.quit()
        self.parent.chat = 0
        self.hide()

        if self.msgetted == 1:
            self.msgetted = 0
            self.mwidget = msget.Invisible(self.parent)
            self.mwidget.setMinimumSize(QSize(200, 200))
            self.mwidget.move(self.msgWidgetPos)

    def category_changed(self):
        self.tab.currentWidget().clear()
        self.history = self.getChatHistory()

        commend = 'category_change '+ self.parent.course[1] + ' ' + self.tab.tabText(self.tab.currentIndex())
        self.chatSocket.send(commend.encode('utf-8'))
        self.showQuestions()

    def getCategory(self):
        commend = "getCategory " + self.lecId
        self.clientSocket.send(commend.encode('utf-8'))

        category = self.clientSocket.recv(30000)
        category = category.decode('utf-8')

        category = category.split(',')
        category.pop()

        for i in range(len(category)):
            self.tab.addTab(QListWidget(self), category[i])

    def sendQuestionToEmail(self):
        self.dlg = sendQuestion(self)
        self.dlg.show()

    def showQuestions(self):
        # self.tab.currentWidget().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tab.currentWidget().setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab.currentWidget().setStyleSheet('QListWidget:item:hover{background:#a1d2d7};')

        for i in range(len(self.history)):
            item = QListWidgetItem(self.tab.currentWidget())
            print("Self.history["+str(i)+"]: "+str(i))
            custom_widget = chatWidget(self,self.history[i],self.parent)
            item.setSizeHint(custom_widget.sizeHint())
            self.tab.currentWidget().setItemWidget(item, custom_widget)
            self.tab.currentWidget().addItem(item)
        self.tab.currentWidget().scrollToBottom()


    def getLecId(self):
        print("self.parent.course: "+ str(self.parent.course))
        commend = "get_lecture_id "+self.parent.course[-1]

        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(30000)

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
        
        commend = 'chat_history '+ self.lecId + " " + self.tab.tabText(self.tab.currentIndex()) +" " + self.parent.stuid
        print("getChatHistory()'s commend: "+str(commend))
        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(30000)

        result = result.decode('utf-8')
        if result == 'x':
            return []

        else:
            result = result.split('/')
            result = result[:-1]
            print("result: "+str(result))
            question = []
            for i in range(len(result)):
                tmp = result[i].split(',')
                tmp = [x for x in tmp if x]
                print("tmp: "+str(tmp))
                if len(tmp) == 10:
                    question.append(tmp)

                elif len(tmp) > 10:
                    msglen = len(tmp) - 10
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

        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def sendMsg(self,msg):
        self.chat_input.setText('')
        if self.sendType == False:
            commend = 'sendReplyMsg ' + self.comment_info[6] + " " + self.parent.stuid + " " + msg


            # main server에 알림
            self.clientSocket.send(commend.encode('utf-8'))

            tmp = self.clientSocket.recv(30000)

            self.chatWidget.refresh()
            # chat server에 전송 -> 모두에게 뿌리기 위해
            # self.chatSocket.send('chat_update'.encode('utf-8'))
        else:
            commend = 'sendMsg ' + self.tab.tabText(self.tab.currentIndex()) + " "+ self.lecId + " " + msg + " " + self.parent.stuid

            #main server에 알림
            self.clientSocket.send(commend.encode('utf-8'))

            tmp = self.clientSocket.recv(30000)
            tmp = tmp.decode('utf-8')

            chat_id = tmp.split(' ')
            #chat server에 전송 -> 모두에게 뿌리기 위해
            data = 'chat_update '+chat_id[1] +" "  + self.parent.stuid+" "+self.parent.course[1]+" "+self.tab.tabText(self.tab.currentIndex())
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
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def create_category(self, name):
        #db로 보내서 등록하고 탭 늘려야됨
        commend = 'category_create ' + self.parent.lecId + " " + name
        self.clientSocket.send(commend.encode('utf-8'))

        new_tab = QListWidget(self)
        self.parent.tab.addTab(new_tab, name)
        self.close()

class chatWidget(QWidget):
    def __init__(self,parent,comments,grandparent):
        super().__init__()
        self.parent = parent
        self.user = self.parent.user
        self.grandparent = grandparent
        self.mainLayout = QHBoxLayout()
        self.questLayoutinMain = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.clientSocket = parent.clientSocket
        self.user_identity = QVBoxLayout() #등급아이콘 + "you" [수직]
        self.like_reply = QVBoxLayout() #좋아요/개수 + 댓글/개수

        #comments 참조 순서 studid,name,comment,like,category_id,time,chat_id
        self.comments = comments
        self.initUI()

    def initUI(self):
        if len(self.comments) != 2:
            # commend = 'like_status '+ self.comments[6] + " " + self.grandparent.stuid#학번
            # self.clientSocket.send(commend.encode('utf-8'))
            # result = self.clientSocket.recv(30000)
            # result = result.decode('utf-8')
            print("self.comments: "+str(self.comments))
            #하트아이콘
            if self.comments[-2] == str(0):
                self.BtnLike = QPushButton(self.comments[3])
                self.BtnLike.setIcon(QIcon('./ui/chatting_ui/unchecked_heart.png'))
            elif self.comments[-2] == str(1):
                self.BtnLike = QPushButton(self.comments[3])
                self.BtnLike.setIcon(QIcon('./ui/chatting_ui/checked_heart.png'))
            self.BtnLike.setStyleSheet('''
            QPushButton{border:0px; background-color:#e8f3f4; width:45px;padding:5px}''')
            self.BtnLike.setFixedSize(60,40)
            self.BtnLike.setIconSize(QSize(27,27))
            #BtnLike.setMaximumWidth()
            self.BtnLike.clicked.connect(self.likeClicked)

            #댓글 아이콘
            self.BtnReply = QPushButton()

            self.BtnReply.setIcon(QIcon('./ui/chatting_ui/reply.png'))
            self.BtnReply.setStyleSheet('''
            QPushButton{border:0px; background-color:#e8f3f4; width:50px;height:40px;padding:20px}''')
            self.BtnReply.setIconSize(QSize(30,30))
            self.BtnReply.setFixedSize(60,40)
            self.BtnReply.setText(str(self.comments[-1]))
            self.BtnReply.setStyleSheet('font:7pt')

            question = QLabel()
            #42939c#24565b
            question.setText(self.comments[2])
            question.setStyleSheet("color: black;"
                               "background-color: white;"
                               "border-style: solid;"
                               "border-width: 1px;"
                               "border-color: #42939c;"
                               "font:10pt 나눔스퀘어라운드 Regular;"
                               )
            question.setFixedHeight(50)
            question.setFixedWidth(320)


            date = QLabel()
            date.setStyleSheet('font:8pt 나눔스퀘어라운드 Regular')
            date.setFixedSize(320,30)
            date.setText(self.comments[5])

        self.mainLayout.setContentsMargins(5,5,5,5)



        user_icon = QPushButton()
        user_icon.setIconSize(QSize(35,35))
        #아이콘 등급
        if int(self.comments[-3])<10:
            user_icon.setIcon(QIcon('./ui/rank_icon/1.png'))

        elif int(self.comments[-3])<20:
            user_icon.setIcon(QIcon('./ui/rank_icon/2.png'))

        elif int(self.comments[-3])<30:
            user_icon.setIcon(QIcon('./ui/rank_icon/3.png'))

        elif int(self.comments[-3])<40:
            user_icon.setIcon(QIcon('./ui/rank_icon/4.png'))

        elif int(self.comments[-3])<50:
            user_icon.setIcon(QIcon('./ui/rank_icon/5.png'))

        else :
            user_icon.setIcon(QIcon('./ui/rank_icon/6.png'))

        user_icon.setStyleSheet('padding:5px')
        self.user_identity.addWidget(user_icon)


        self.like_reply.addWidget(self.BtnLike)
        self.like_reply.addWidget(self.BtnReply)
        # 내가 쓴 질문이면
        if self.comments[0] == self.grandparent.stuid:
            you = QLabel('Me')
            you.setStyleSheet('padding:5px; font:9pt 나눔스퀘어라운드 Regular;')
            #self.mainLayout.addWidget(you)
            self.user_identity.addWidget(you)
        else :
            notyou = QLabel()
            notyou.setStyleSheet('padding:5px')
            self.user_identity.addWidget(notyou)

        self.user_identity.setSpacing(0)
        self.like_reply.setSpacing(0)
        self.like_reply.setContentsMargins(0,0,0,0)
        self.mainLayout.addLayout(self.user_identity)

        self.questLayoutinMain.addStretch(1)
        self.questLayoutinMain.addWidget(question)
        self.questLayoutinMain.addWidget(date)
        self.questLayoutinMain.addStretch(1)
        self.questLayoutinMain.setSpacing(0)


        self.mainLayout.addLayout(self.questLayoutinMain)
        self.mainLayout.addLayout(self.like_reply)
        #self.mainLayout.addWidget(self.BtnLike)
        self.mainLayout.setSpacing(0)

        self.mainLayout.addStretch(1)

    def likeClicked(self):
        print("like_update's comments: "+str(self.comments))
        commend = 'like_update '+ self.comments[6] + " " + self.grandparent.stuid#학번 + msg
        self.clientSocket.send(commend.encode('utf-8'))

        result = self.clientSocket.recv(30000)
        result = result.decode('utf-8')
        result = result.split("!@!")

        self.BtnLike.setText(str(result[0]))
        #self.BtnLike.setText('99')
        self.comments[3] = str(result[0])
        if result[1] == '0':
            self.BtnLike.setIcon(QIcon('./ui/chatting_ui/unchecked_heart.png'))
        elif result[1] == '1':
            self.BtnLike.setIcon(QIcon('./ui/chatting_ui/checked_heart.png'))


    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            #질문 목록 위젯 닫음
            self.parent.chatWidget.close()

            #메시지 전송 타입 답글로 변경
            self.parent.sendType = False

            #리플 위젯 생성 및 변수값 대입
            self.parent.comment_info = self.comments
            self.tmpSocket = self.parent.clientSocket
            self.parent.clientSocket = self.clientSocket
            replyWidget = reply.Reply(self.parent)
            replyWidget.widgetTmp = self.parent.chatWidget
            replyWidget.clientSocket = self.clientSocket
            self.parent.clientSocket = self.tmpSocket
            # replyWidget = self.parent.reply

            self.parent.chatWidget = replyWidget

            #리플 위젯 화면 뿌려주기
            self.parent.chatWidget.comment_info = self.comments
            self.parent.chatWidget.replyList = self.parent.chatWidget.getReply()
            self.parent.chatWidget.showReply()
            self.parent.chatContentLayout.addWidget(self.parent.chatWidget)

        elif QMouseEvent.button() == Qt.RightButton:
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

        info = self.parent.clientSocket.recv(30000).decode('utf-8')
        info = info.split(',')

        if self.parent.user['is_prof'] == 1:
            self.name.setText('이름: '+info[5])
            self.depart.setText('학과: '+info[1])
            self.student_id.setText('학번: '+self.parent.comments[0])
        else:
            self.name.setText('닉네임: ' + info[0])
            self.depart.setText('학과: ' + info[1])
            self.student_id.setText('포인트: ' + info[4])


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)

        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

class sendQuestion(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.dateLayout1 = QHBoxLayout()
        self.dateLayout2 = QHBoxLayout()
        self.topbar = QWidget()
        self.topbar_layout = QHBoxLayout()
        #self.topbar_layout.setContentsMargins(0,0,0,0)
        self.topbar.setLayout(self.topbar_layout)

        self.topbar.setStyleSheet('background:#a1d2d7')
        self.topbar.setContentsMargins(0,0,0,0)

        self.botbar = QVBoxLayout()
        self.botbar.setContentsMargins(10,10,10,10)

        self.oldPos = self.pos()
        self.btnLayout = QHBoxLayout()
        self.btnLayout.setContentsMargins(10,10,10,10)
        self.setStyleSheet('background-color:#e8f3f4')
        self.setMaximumSize(250,250)
        self.setMinimumSize(250,250)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setContentsMargins(0,0,0,0)
        self.initUi()

    def initUi(self):
        head = QLabel('질문 전송')
        head.setStyleSheet('font:13pt 나눔스퀘어라운드 Regular;')

        self.email = QLabel(self.parent.user['email']+'@ajou.ac.kr')
        self.email.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;')
        self.startDate = QLabel('시작 날짜: ')
        self.startDate.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;')
        self.btnStart = QPushButton('날짜 입력')
        self.btnStart.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;border:0px;')
        self.btnStart.clicked.connect(lambda : self.openCalendar('start'))

        self.finishDate = QLabel('종료 날짜: ')
        self.finishDate.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;')
        self.btnFinish = QPushButton('날짜 입력')
        self.btnFinish.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;border:0px;')
        self.btnFinish.clicked.connect(lambda : self.openCalendar('finish'))

        send = QPushButton('전송')
        send.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;')
        send.clicked.connect(self.sendToEmail)
        cancel = QPushButton('취소')
        cancel.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;')
        cancel.clicked.connect(self.close)

        self.btnLayout.addWidget(send)
        self.btnLayout.addWidget(cancel)

        self.dateLayout1.addWidget(self.startDate)
        self.dateLayout1.addWidget(self.btnStart)

        self.dateLayout2.addWidget(self.finishDate)
        self.dateLayout2.addWidget(self.btnFinish)



        #self.mainLayout.addWidget(head)
        self.topbar_layout.addWidget(head)
        self.mainLayout.addWidget(self.topbar)

        self.botbar.addWidget(self.email)
        self.botbar.addLayout(self.dateLayout1)
        self.botbar.addLayout(self.dateLayout2)
        self.mainLayout.addLayout(self.botbar)
        self.mainLayout.addLayout(self.btnLayout)
        self.mainLayout.addStretch(1)

        #self.setFixedSize(200,200)
        self.setLayout(self.mainLayout)

    def openCalendar(self, type):
        self.calendar = calendarW.calendarWidget(self, type)
        self.calendar.exec_()

    def sendToEmail(self):
        #카테고리 이름, lecid, email주소
        commend = "sendToEmail " + self.parent.tab.tabText(self.parent.tab.currentIndex()) + " " + self.parent.lecId + " "+ self.email.text()
        if self.btnStart.text() == '날짜 입력':
            errMsg = QMessageBox()
            errMsg.setStyleSheet("background-color:#FFFFFF")
            errMsg.setText('날짜를 입력해주세요')
            errMsg.exec_()
        elif self.btnFinish.text() == '날짜 입력':
            errMsg = QMessageBox()
            errMsg.setStyleSheet("background-color:#FFFFFF")
            errMsg.setText('날짜를 입력해주세요')
            errMsg.exec_()

        else:
            commend += " " + self.btnStart.text()  # 3 시작 날짜
            commend += " " + self.btnFinish.text()  # 4 종료 날짜

            self.parent.clientSocket.send(commend.encode('utf-8'))

            res = self.parent.clientSocket.recv(30000).decode('utf-8')

            if res == 'success':
                self.close()
                send_ok = QMessageBox()
                send_ok.setStyleSheet("background-color:#FFFFFF")
                send_ok.setText('전송 되었습니다')
                send_ok.exec_()
            elif res == 'no':
                noMsg = QMessageBox()
                noMsg.setStyleSheet("background-color:#FFFFFF")
                noMsg.setText('질문이 존재하지 않습니다.')
                noMsg.exec_()


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)

        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = chatRoom()
    sys.exit(app.exec_())