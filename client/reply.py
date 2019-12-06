import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import time


class update_listener(QThread):
    chatUpdate = pyqtSignal()

    def __init__(self, parent=None):
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
            elif update_commend == 'stop':
                self.go = False
                # break

class Reply(QWidget):
    def __init__(self,parent):
        super().__init__()
        #변수 설정
        self.parent = parent
        self.user = self.parent.user
        self.clientSocket = 0
        self.comment_info = 0
        self.replyList = 0
        self.widgetTmp = QWidget()
        #효과 설정
        # shadow = QGraphicsDropShadowEffect()
        # shadow.setBlurRadius(5)
        # shadow.setOffset(3)
        # self.setGraphicsEffect(shadow)
        self.oldPos = self.pos()
        #맨윗줄 톱 바
        self.topbar = QHBoxLayout()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)

        #배경색 지정할 위젯 선언
        self.mainWidget = QWidget()
        self.mainWidget.setStyleSheet('background-color:#e8f3f4')

        #질문 타이틀 레이아웃
        self.questionWidget = QWidget()
        self.questionWidget.setStyleSheet("background-color:white;")
        
        self.question_title_bottom = QHBoxLayout()

        #타이틀 관련 위젯은 questionLayout에 추가
        self.questionLayout = QVBoxLayout()
        self.questionWidget.setLayout(self.questionLayout)
        self.questionWidget.setMaximumSize(500,180)


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
        #위젯은 widgetLayout에 추가하면 됨
        btnBack =QPushButton()
        btnBack.setIconSize(QSize(30, 30))
        btnBack.setMaximumWidth(40)
        btnBack.setStyleSheet('width:40px; border:0px')
        btnBack.setIcon(QIcon('./ui/chatting_ui/back.png'))
        btnBack.clicked.connect(self.returnToChat)

        btnRefresh = QPushButton()
        btnRefresh.setStyleSheet('''QPushButton{image:url(./ui/chatting_ui/refresh.png); border:0px; width:30px; height:30px} ''')
        
        btnRefresh.clicked.connect(self.refresh)
        


        #질문 타이틀
        self.question_title = QLabel()

        self.question_title2 = QTextBrowser()
        self.question_title2.setMaximumHeight(80)
        self.question_title2.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;background-color:white;border:0px')
        
        self.questionLayout.addWidget(self.question_title2)

        #질문 타이틀 bottom
        self.dateLabel = QLabel()
        self.dateLabel.setStyleSheet('font:7pt 나눔스퀘어라운드 Regular')

        commend = 'like_status '+ self.parent.comment_info[-3] + " " + self.parent.parent.stuid#학번
        self.parent.clientSocket.send(commend.encode('utf-8'))
        result = self.parent.clientSocket.recv(1024)
        result = result.decode('utf-8')
        
        if result == '0':
            self.btnLike = QPushButton(self.parent.comment_info[3])
            self.btnLike.setIcon(QIcon('./ui/chatting_ui/unchecked_heart.png'))
        elif result == '1':
            self.btnLike = QPushButton(self.parent.comment_info[3])
            self.btnLike.setIcon(QIcon('./ui/chatting_ui/checked_heart.png'))
        
        self.btnLike.setStyleSheet('''
                                QPushButton{border:0px}''')
        self.btnLike.setIconSize(QSize(23, 23))
        self.btnLike.setMaximumWidth(35)
        self.btnLike.clicked.connect(self.likeClicked)

        self.question_title_bottom.addWidget(self.dateLabel)
        self.question_title_bottom.addWidget(self.btnLike)

        self.questionLayout.addLayout(self.question_title_bottom)


        #질문 목록
        self.question_reply = QListWidget()
        self.question_reply.scrollToBottom()
        self.question_reply.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.question_reply.setContentsMargins(0,0,0,0)
        self.question_reply.setStyleSheet('''
                        QListWidget:item:hover{background:#95c3cb};
                        QListWidget:item{margins:0px}
                        ''')

        #widgetLayout에 추가(총 세로 레이아웃:탑, 질문, 댓글)
        self.topbar.addWidget(btnBack)
        self.topbar.addStretch(1)
        self.topbar.addWidget(btnRefresh)
        self.widgetLayout.addLayout(self.topbar,1)

        self.widgetLayout.addWidget(self.questionWidget)
        self.widgetLayout.setStretchFactor(self.questionWidget,2)
        self.widgetLayout.addWidget(self.question_reply)
        self.widgetLayout.setStretchFactor(self.question_reply,5)

        # self.show()

    def refresh(self):
        self.question_reply.clear()
        self.replyList = self.getReply()
        for i in range(len(self.replyList)):
            item = QListWidgetItem(self.question_reply)

            custom_widget = replyWidget(self.replyList[i],self.parent,self)
            item.setSizeHint(custom_widget.sizeHint())
            self.question_reply.setItemWidget(item, custom_widget)
            self.question_reply.addItem(item)
        self.question_reply.scrollToBottom()


    def likeClicked(self):
        commend = 'like_update '+ self.parent.comment_info[-3] + " " + self.parent.parent.stuid#학번 + msg
        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(1024)
        result = result.decode('utf-8')
        result = result.split("!@!")

        self.btnLike.setText(str(result[0]))
        self.parent.comment_info[3] = str(result[0])
        if result[1] == '0':
            self.btnLike.setIcon(QIcon('./ui/chatting_ui/unchecked_heart.png'))
        elif result[1] == '1':
            self.btnLike.setIcon(QIcon('./ui/chatting_ui/checked_heart.png'))

    #뒤로가기 버튼 눌렀을시
    def returnToChat(self):
        self.close()
        self.parent.chatWidget = self.widgetTmp
        self.parent.sendType = True

        self.widgetTmp.show()
        

    #질문에 대한 답글 읽어옴
    def getReply(self):
        commend = 'replyHistory ' + self.comment_info[6]

        self.clientSocket.send(commend.encode('utf-8'))

        res = self.clientSocket.recv(1024)
        res = res.decode('utf-8')

        if res == 'x':
            return []

        else:
            res = res.split('/')
            res.pop()
            reply = []

            for i in range(len(res)):
                tmp = res[i].split(',')
                tmp = [x for x in tmp if x]

                if len(tmp) == 5:
                    reply.append(tmp)

                elif len(tmp) > 5:
                    msglen = len(tmp) - 5
                    msg = ",".join(tmp[0:1 + msglen])

                    for i in range(msglen + 1):
                        del tmp[0]
                    tmp.insert(0, msg)
                    reply.append(tmp)
                    
            return reply

    #리스트 위젯에 답글 추가
    def showReply(self):
        self.question_title2.setText(str(self.comment_info[2]))
        self.btnLike.setText(str(self.comment_info[3]))
        self.dateLabel.setText(str(self.comment_info[5]))

        for i in range(len(self.replyList)):
            item = QListWidgetItem(self.question_reply)

            custom_widget = replyWidget(self.replyList[i],self.parent,self)
            item.setSizeHint(custom_widget.sizeHint())
            self.question_reply.setItemWidget(item, custom_widget)
            self.question_reply.addItem(item)


class replyWidget(QWidget):
    def __init__(self,comments, parent,forRefresh):
        super().__init__()
        self.parent = parent
        self.forRefresh = forRefresh
        self.user = parent.user
        self.clientSocket = self.parent.clientSocket
        self.comments = comments

        self.replyLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.initUI()

    def initUI(self):
        adopt_medal = QLabel()
        adopt_medal_img = QPixmap('./ui/chatting_ui/champion.png')
        adopt_medal_img = adopt_medal_img.scaled(45,45)
        adopt_medal.setPixmap(adopt_medal_img)
        adopt_medal.setAlignment(Qt.AlignRight)

        question = QLabel()
        question.setMinimumWidth(400)
        question.setMaximumWidth(400)
        question.setWordWrap(True)
        
        question.setStyleSheet('width:400px;')

        question.setText(self.comments[0])

        question2 = QTextBrowser()
        question2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        question2.setMaximumWidth(385)
        question2.setMinimumWidth(385)
        question2.setFixedHeight(90)
        #question2.setSizeAdjustPolicy(question2.AdjustToContents)
        #question2.setFixedHeight(question2.document().size().height())
        #question2.setSizePolicy
        
        #question2.auto
        
        question2.setStyleSheet("border:1px;"
                                "border-color:red;"
                                "font: 9pt 나눔스퀘어라운드 Regular;"
                                )
        
        question2.setText(self.comments[0])
        question2.setSizeAdjustPolicy(question2.AdjustToContents)
        #question2.setFixedHeight(self.comments[0].size().height())
        #question2.setFixedHeight(question2.document().size().height())
        date = QLabel()
        date.setStyleSheet('font:8pt;color:#7f7f7f')
        date.setText(self.comments[2])

        #replyLayout: 댓글+날짜 (수직 레이아웃)
        self.replyLayout.addWidget(question2)
        self.replyLayout.addWidget(date)
        self.replyLayout.setContentsMargins(0,0,0,0)
        
        #mainLayout: replyLayout+메달 (수평 레이아웃)
        self.mainLayout.addLayout(self.replyLayout)
        self.mainLayout.setContentsMargins(5,5,5,5)

        if self.comments[4] == str(1):
            self.mainLayout.addWidget(adopt_medal,alignment=QtCore.Qt.AlignRight)
        self.mainLayout.addStretch(1)
        self.mainLayout.setSpacing(0)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.RightButton:
            msg = QMessageBox()

            msg.setWindowTitle('옵션')
            msg.setText('어떤 작업을 수행하시겠습니까?')
            msg.addButton(QPushButton('채택'), 0)
            msg.addButton(QPushButton('취소'), 1)
            msg.addButton(QPushButton('정보'), 2)

            msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)

            result = msg.exec_()

            if result == 0:
                dlg = sendQuestion(self)
                dlg.exec_()
                self.forRefresh.refresh()

            elif result == 2:
                dlg = studentInfo(self)
                dlg.exec_()


class studentInfo(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.user = parent.user
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
        commend = 'getProfile ' + self.parent.comments[1]
        self.parent.clientSocket.send(commend.encode('utf-8'))

        info = self.parent.clientSocket.recv(1024).decode('utf-8')
        info = info.split(',')

        if self.user['is_prof']:
            self.name.setText('이름: '+info[5])
            self.depart.setText('학과: '+info[1])
            self.student_id.setText('학번: '+self.parent.comments[1])
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

class sendQuestion(QDialog):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.initUi()

    def initUi(self):
        head = QLabel('\t현 댓글을 채택하시겠습니까?\n(주의! 한 번 채택하시면 현 게시글의 댓글에 더 이상 \n 채택을 하시지 못하시며 취소도 하실수 없습니다.)')
        head.setStyleSheet('font-weight:bold; font-size:13pt;')
        send = QPushButton('확인')
        send.clicked.connect(self.sendToEmail)
        cancel = QPushButton('취소')
        cancel.clicked.connect(self.close)

        self.btnLayout.addWidget(send)
        self.btnLayout.addWidget(cancel)

        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(head)
        self.mainLayout.addLayout(self.btnLayout)
        self.mainLayout.addStretch(1)

        self.setFixedSize(550,200)
        self.setLayout(self.mainLayout)

    def sendToEmail(self):
        self.close()
        commend = 'reply_select ' + self.parent.comments[3] + " " + self.parent.parent.parent.stuid  # reply_id + 학번

        self.parent.parent.clientSocket.send(commend.encode('utf-8'))
        result = self.parent.parent.clientSocket.recv(1024)
        result = result.decode('utf-8')

        if(result == "already"):
            send_already = QMessageBox()
            send_already.setStyleSheet("background-color:#FFFFFF")
            send_already.setText("이미 채택하셨습니다")
            send_already.exec_()

        elif(result=="update"):
            send_update = QMessageBox()
            send_update.setStyleSheet("background-color:#FFFFFF")
            send_update.setText("채택하셨습니다")
            send_update.exec_()

        elif(result=="notyour"):
            send_notyour = QMessageBox()
            send_notyour.setStyleSheet("background-color:#FFFFFF")
            send_notyour.setText("자신의 게시글에 대한 답글에만 채택하실 수 있습니다")
            send_notyour.exec_()

        elif(result=="same"):
            send_same = QMessageBox()
            send_same.setStyleSheet("background-color:#FFFFFF")
            send_same.setText("자신의 글은 채택 불가합니다")
            send_same.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Reply()
    sys.exit(app.exec_())