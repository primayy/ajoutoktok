import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import smtplib
from email.mime.text import MIMEText
from socket import *
import time

class update_listener(QThread):
    chatUpdate = pyqtSignal()

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

            if update_commend == 'update':
                self.chatUpdate.emit()
                # print('업데이트 시그널 emit')
            elif update_commend =='stop':
                self.go = False
                print('멈춤')
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
        self.clientSocket = parent.w.clientSock
        self.lecId = self.getLecId()

        self.tab = QTabWidget()
        self.getCategory()

        #chat server와 연결
        self.chatSocket= socket(AF_INET, SOCK_STREAM)
        self.chatSocket.connect(('192.168.0.14', 3334))
        # self.chatSocket.connect(('34.84.112.149', 3334))

        self.history = self.getChatHistory()
        if len(self.history) != 0:
            self.history.pop()
        self.tab.currentChanged.connect(self.category_changed)

        #디자인
        self.showLayout = QVBoxLayout()
        self.mainLayout = QVBoxLayout()
        self.mainWidget = QWidget()
        self.mainLayout.setSpacing(0)

        #타이틀 -> 강의이름/타이틀바
        self.titleWidget = QWidget()
        self.titleWidget.setStyleSheet('background-color:#5218FA')
        self.titleLayout = QVBoxLayout()
        self.titleLayout.setContentsMargins(15,10,15,10)

        self.titleLayoutTop = QHBoxLayout()
        self.titleLayoutMid = QHBoxLayout()
        self.titleLayoutBot = QHBoxLayout()

        self.titleLayout.addLayout(self.titleLayoutTop)
        self.titleLayout.addLayout(self.titleLayoutMid)
        self.titleLayout.addLayout(self.titleLayoutBot)
        self.titleWidget.setLayout(self.titleLayout)
        #채팅 내용
        self.chatWidget = QWidget()
        self.chatWidget.setStyleSheet('background-color:white')
        self.chatLayout = QVBoxLayout()
        self.chatWidget.setLayout(self.chatLayout)

        #입력창
        self.chat_input = QTextEdit()
        self.chat_input.setStyleSheet('background:white')

        self.chatLayoutWidget = QWidget()
        self.chatLayoutWidget.setStyleSheet('background-color:#5218FA')
        self.chatLayoutWidget.setMaximumHeight(100)
        self.chatInputLayout = QHBoxLayout()
        self.chatLayoutWidget.setLayout(self.chatInputLayout)

        #메인 레이아웃 설정
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.titleWidget)
        self.mainLayout.addWidget(self.chatWidget)
        self.mainLayout.addWidget(self.chatLayoutWidget)

        self.mainWidget.setLayout(self.mainLayout)

        self.showLayout.addWidget(self.mainWidget)
        self.showLayout.setContentsMargins(0,0,5,5)
        self.setLayout(self.showLayout)
        self.setMinimumSize(500,700)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
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


        self.titleLayoutTop.addStretch(1)
        self.titleLayoutTop.addWidget(btMini,alignment=QtCore.Qt.AlignRight)
        self.titleLayoutTop.addWidget(btExit,alignment=QtCore.Qt.AlignRight)

        #강의명
        lecName = QLabel(self.parent.course[0])
        lecName.setStyleSheet('font-weight:bold; font-size:16pt')

        self.titleLayoutMid.addWidget(lecName,alignment=QtCore.Qt.AlignLeft)

        #강의 정보
        profName = QLabel(self.parent.course[1])
        download = QPushButton()
        download.clicked.connect(self.sendQuestionToEmail)
        download.setMaximumWidth(25)
        download.setStyleSheet('border:0px')
        download.setIcon(QIcon('./icon/download.png'))
        download.setIconSize(QSize(30,30))
        self.titleLayoutBot.addWidget(profName)
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
        chat_enter.setStyleSheet('background:#F6F6F3')
        chat_enter.setMinimumHeight(78)
        chat_enter.setIcon(QIcon('./icon/send.png'))
        chat_enter.setIconSize(QSize(50,50))
        chat_enter.clicked.connect(lambda: self.sendMsg(self.chat_input.toPlainText()))

        self.chatInputLayout.addWidget(self.chat_input)
        self.chatInputLayout.addWidget(chat_enter)

        self.show()

    def chat_Update(self):
        # print('ㅇㅇㅇ')
        self.category_changed()

    def quitClicked(self):
        commend = 'exit'
        self.chatSocket.send(commend.encode('utf-8'))
        #쓰레드 삭제
        self.t.quit()
        self.close()

    def category_changed(self):
        self.tab.currentWidget().clear()
        self.history = self.getChatHistory()
        if len(self.history) != 0:
            self.history.pop()
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
        for i in range(len(self.history)):
            item = QListWidgetItem(self.tab.currentWidget())

            custom_widget = chatWidget(self,self.history[i])
            item.setSizeHint(custom_widget.sizeHint())
            self.tab.currentWidget().setItemWidget(item, custom_widget)
            self.tab.currentWidget().addItem(item)

    def getLecId(self):
        commend = "get_lecture_id "+self.parent.course[1]

        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(1024)

        return result.decode('utf-8')

    def getChatHistory(self):
        commend = 'chat_history '+ self.lecId + " " + self.tab.tabText(self.tab.currentIndex())
        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(1024)
        result = result.decode('utf-8')

        if result == 'x':
            return []

        else:
            result = result.split('/')
            question = []

            for i in range(len(result)):
                question.append(result[i].split(','))

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
        self.chat_input.setPlainText('')
        commend = 'sendMsg ' + self.tab.tabText(self.tab.currentIndex()) + " "+ self.lecId + " " + msg + " " + self.parent.stuid
        # print(commend)

        #main server에 알림
        self.clientSocket.send(commend.encode('utf-8'))

        tmp = self.clientSocket.recv(1024)
        #chat server에 전송 -> 모두에게 뿌리기 위해
        self.chatSocket.send('chat_update'.encode('utf-8'))

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
        print(commend)
        self.clientSocket.send(commend.encode('utf-8'))

        new_tab = QListWidget(self)
        self.parent.tab.addTab(new_tab, name)
        self.close()

class chatWidget(QWidget):
    def __init__(self,parent,comments):
        super().__init__()
        self.parent = parent
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.clientSocket = parent.clientSocket

        #comments 참조 순서 studid,name,comment,like,category_id,time
        self.comments = comments
        self.initUI()

    def initUI(self):
        if len(self.comments) != 2:
            BtnLike = QPushButton(self.comments[3])
            BtnLike.setIcon(QIcon('./icon/heart_unchecked.png'))
            BtnLike.setStyleSheet('''
            QPushButton{border:0px}''')
            BtnLike.setIconSize(QSize(20,20))
            BtnLike.setMaximumWidth(35)
            BtnLike.clicked.connect(self.likeClicked)

            question = QLabel()
            question.setText(self.comments[2])
        else:
            BtnLike = QPushButton('0')
            BtnLike.setIcon(QIcon('./icon/heart_unchecked.png'))
            BtnLike.setStyleSheet('''
                        QPushButton{border:0px}''')
            BtnLike.setIconSize(QSize(20, 20))
            BtnLike.setMaximumWidth(35)
            BtnLike.clicked.connect(self.likeClicked)

            question = QLabel()
            question.setText(self.comments[0])

        self.mainLayout.addWidget(question)
        self.mainLayout.addWidget(BtnLike)

    def likeClicked(self):
        print(self.comments)
        commend = 'like_update '+ self.comments[0] + " " + self.comments[2] #학번 + msg
        self.clientSocket.send(commend.encode('utf-8'))
        print(commend)
        result = self.clientSocket.recv(1024)
        result = result.decode('utf-8')
        print(result)
        self.parent.category_changed()


    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print(self.comments)
            print("Left Button Clicked")
        elif QMouseEvent.button() == Qt.RightButton:
            print("Right Button Clicked")

class sendQuestion(QDialog):
    def __init__(self,parent):
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.initUi()

    def initUi(self):
        head = QLabel('질문 전송')
        head.setStyleSheet('font-weight:bold; font-size:13pt')
        email = QLineEdit()
        email.setPlaceholderText('이메일')
        send = QPushButton('전송')
        send.clicked.connect(self.sendToEmail)
        cancel = QPushButton('취소')
        cancel.clicked.connect(self.close)

        self.btnLayout.addWidget(send)
        self.btnLayout.addWidget(cancel)

        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(head)
        self.mainLayout.addWidget(email)
        self.mainLayout.addLayout(self.btnLayout)
        self.mainLayout.addStretch(1)

        self.setFixedSize(200,150)
        self.setLayout(self.mainLayout)


    # 당분간 사용 금지
    def sendToEmail(self):
        print('aa')
        # try:
        #     smtp = smtplib.SMTP('smtp.gmail.com', 587)
        #     smtp.ehlo()
        #     smtp.starttls()
        #     smtp.login('primayy@ajou.ac.kr', 'cssprcyzfogxtmbu')
        #
        #     msg = MIMEText('되나')
        #     msg['Subject'] = '제목 테스트'
        #     msg['To'] = '테스트'
        #     smtp.sendmail('primayy@ajou.ac.kr', 'primayy@naver.com', msg.as_string())
        #
        #     smtp.quit()
        # except smtplib.SMTPException:
        #     print('error')
        # else:
        #     self.close()
        #     send_ok = QMessageBox()
        #     send_ok.setStyleSheet("background-color:#FFFFFF")
        #     send_ok.setText('전송 되었습니다')
        #     send_ok.exec_()

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