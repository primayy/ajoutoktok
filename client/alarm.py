import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import chat_test
import reply

class alarm(QWidget):
    def __init__(self,parent,studId):
        super().__init__()
        self.mainLayout=QVBoxLayout()
        self.stuid = studId
        self.clientSocket = parent.clientSocket
        self.title = QHBoxLayout()

        #강의 목록 그리기
        group = QLabel('알림')
        group.setStyleSheet("font: 16pt 나눔스퀘어라운드 Regular;background:#eef5f6;color:#42808a")

        horizon_line = QLabel()
        horizon_img = QPixmap('./ui/afterlogin_ui/horizon_line.png')
        horizon_img = horizon_img.scaled(310,12,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        horizon_line.setPixmap(horizon_img)
        horizon_line.setAlignment(Qt.AlignTop)

        btn_remove_all = QPushButton()
        btn_remove_all.setStyleSheet('''
                        QPushButton{image:url(./ui/afterlogin_ui/모두삭제4.png); border:0px; width:100px; height:40px}        
                        ''')
        
        btn_remove_all.clicked.connect(self.remove_it_all)

        self.viewer = QListWidget(self)

        self.viewer.setMinimumSize(300, 500)
        self.viewer.setStyleSheet('''
                # QListWidget:item:hover{background:white};
                # QListWidget:item:selected:active{background:white}
                ''')
        self.alarm_list = self.getAlarmList()
        self.showAlarms()

        item = QListWidgetItem(self.viewer)

        self.viewer.addItem(item) #혹시 몰라서 삭제 안함
        self.title.addWidget(group)
        self.title.addStretch(1)
        self.title.addWidget(btn_remove_all,alignment=(QtCore.Qt.AlignBottom)) #alignment=(QtCore.Qt.AlignRight)
        self.mainLayout.addLayout(self.title)
        self.mainLayout.addWidget(horizon_line)
        self.mainLayout.addWidget(self.viewer)
        self.setLayout(self.mainLayout)
    
    def remove_it_all(self):
        chattyId = ""
        replylyId = ""
        if len(self.chatIDs)>0:
            for i in range(len(self.chatIDs)):
                chattyId += self.chatIDs[i] + ";;;"


        if len(self.replyIDs)>0:
            for i in range(len(self.replyIDs)):
                replylyId += self.replyIDs[i] + ";;;"


        commend = "RemoveAlarm " + chattyId + " " + replylyId
        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(1024).decode('utf-8')
        self.viewer.clear()


    def showAlarms(self):
        for i in range(len(self.alarm_list)):
            for ii in range(len(self.alarm_list[i])):
                item = QListWidgetItem(self.viewer)
                custom_widget = alarm_group(self.alarm_list[i][ii], QApplication.activeWindow(),self,i)
                item.setSizeHint(custom_widget.sizeHint())
                self.viewer.setItemWidget(item, custom_widget)
                self.viewer.addItem(item)

    def getAlarmList(self):
        commend = "Alarm " + self.stuid
        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(1024).decode('utf-8')
        
        alarmList = result.split("$#%^")
        chatAlarm = alarmList[0] #게시글에 댓글 달림
        replyAlarm = alarmList[1] #댓글이 채택됨
        self.chatIDs = chatAlarm.split("!@#@!")[1].split("/./")[1:]
        self.replyIDs = replyAlarm.split("!@#@!")[1].split("/./")[1:]
        chatAlarm = chatAlarm.split("!@#@!")[0]
        replyAlarm = replyAlarm.split("!@#@!")[0]
        

        chatAlarm = chatAlarm.split("*&^%")[:-1] # 끝에 생성되는 [''] 삭제
        replyAlarm = replyAlarm.split("*&^%")[:-1] # 끝에 생성되는 [''] 삭제

        return [chatAlarm,replyAlarm]

class alarm_group(QWidget):
    def __init__(self, courses,w,parent,chatORreply):
        super().__init__()
        self.parent = parent
        course = courses.split('#&$@')

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(1,3,1,3)
        #그룹 그리기
        self.mainWidget = lecture(self.parent, course, w, chatORreply)

        self.mainLayout.addWidget(self.mainWidget)
        self.setLayout(self.mainLayout)

class lecture(QWidget):
    def __init__(self, alarm_list_Widget, course,window,chatORreply):
        super().__init__()
        self.alarm_list_Widget = alarm_list_Widget
        self.stuid = alarm_list_Widget.stuid

        self.w = window
        self.clientSocket = self.w.clientSock
        self.viewer = alarm_list_Widget.viewer
        self.course = course

        self.mainLayout = QVBoxLayout()
        self.mainWidget = QWidget()
        self.mainWidget.setStyleSheet("background-color:#eef5f6;")
        self.mainWidget.setMinimumSize(100,50)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.mainWidget)

        
        self.layout = QVBoxLayout()
        self.layout_middle = QHBoxLayout()

            # top

            # middle
        if chatORreply == 0:
            self.alarm = QWidget()
            layoutout = QVBoxLayout()
            Qlabel1 = QLabel(str("[강의: "+course[0]+"]에 게시한 글 '"+course[1]+"'에 "+course[2]+"개의 댓글이 추가되었습니다."))
            dateAtime = str(course[-4])

            layoutout.addWidget(Qlabel1)
            if(len(dateAtime)>0):
                dateBtime = dateAtime.split("(")[3].split(")")[0]

                datetime = dateBtime.split(",")

                date = ".".join(datetime[0:3])
                time = ":".join(datetime[3:6])

                Qlabel2 = QLabel(str(date)+" "+str(time))
                layoutout.addWidget(Qlabel2)
            self.alarm.setLayout(layoutout)
        elif chatORreply == 1:
                self.alarm = QLabel(str("[강의: "+course[0]+"]에 작성한 댓글'"+course[1]+"'이 채택되었습니다."))
        self.chatComm = course[1]
        self.chatName = course[-2]
        self.LecID = course[-3]
        self.alarm.setStyleSheet('font: 10pt 나눔스퀘어라운드 Regular;background:#eef5f6;color:#42808a')
        self.layout_middle.addWidget(self.alarm)

        self.layout.addLayout(self.layout_middle)
        self.mainWidget.setLayout(self.layout)
        self.setLayout(self.mainLayout)

    def mousePressEvent(self, QMouseEvent):
        title = self.course
        self.chat = chat_test.chatRoom(self,0)

        self.chat.setWindowTitle(title[0])
        self.chat.setMinimumSize(QSize(400, 400))

        #질문 목록 닫기
        self.chat.chatWidget.close()

        # 메시지 전송 타입 답글로 변경
        self.chat.sendType = False

        commend = "AlarmToReply " + self.LecID + " " + self.chatName + " " + self.chatComm
        self.clientSocket.send(commend.encode('utf-8'))
        self.coursep = self.clientSocket.recv(1024).decode('utf-8')
        self.coursep = self.coursep.split("/")
        self.coursep = self.coursep[0]

        #댓글 위젯 생성
        self.reply = reply.Reply(self.chat)
        self.coursep = self.coursep.split("#$%#")
        self.chat.comment_info = self.coursep

        self.reply.widgetTmp = self.chat.chatWidget
        self.reply.clientSocket = self.clientSocket

        self.chat.chatWidget = self.reply

        # 리플 위젯 화면 뿌려주기
        self.chat.chatWidget.comment_info = self.coursep
        self.chat.chatWidget.replyList = self.chat.chatWidget.getReply()
        self.chat.chatWidget.showReply()
        self.chat.chatContentLayout.addWidget(self.chat.chatWidget)

        self.reply.setWindowTitle(title[0])
        self.reply.setMinimumSize(QSize(400, 400))
        self.reply.show()







if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = alarm()
    form.show()
    exit(app.exec_())