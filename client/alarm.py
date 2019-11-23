import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class alarm(QWidget):
    def __init__(self,parent,studId):
        super().__init__()
        self.mainLayout=QVBoxLayout()
        self.stuid = studId
        self.clientSocket = parent.clientSocket
        self.title = QHBoxLayout()
        group = QLabel('알림')
        horizon_line = QLabel('─────────────────────')
        btn_remove_all = QPushButton('모두 삭제')
        group.setStyleSheet('''
                font-weight:bold;
                font-size:16pt''')
        viewer = QListWidget(self)

        viewer.setMinimumSize(300, 500)
        viewer.setStyleSheet('''
                # QListWidget:item:hover{background:white};
                # QListWidget:item:selected:active{background:white}
                ''')

        item = QListWidgetItem(viewer)
        # custom_widget = lecture_group('add', studid, QApplication.activeWindow())
        # item.setSizeHint(custom_widget.sizeHint())
        # self.viewer.setItemWidget(item, custom_widget)
        commend = "Alarm " + self.stuid
        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(1024).decode('utf-8')
        print(str(result))
        alarmList = result.split("/")
        chatAlarm = alarmList[0] #게시글에 댓글 달림
        replyAlarm = alarmList[1] #댓글이 채택됨
        print(alarmList)
        print(chatAlarm)
        print(replyAlarm)
        chatAlarm = chatAlarm.split(".")[:-1] # 끝에 생성되는 [''] 삭제
        replyAlarm = replyAlarm.split(".")[:-1] # 끝에 생성되는 [''] 삭제
        print(chatAlarm)
        print(replyAlarm)
        for i in range(len(chatAlarm)):
                chattyAlarm = chatAlarm[i].split(",")
                viewer.addItem(str("[강의: "+chattyAlarm[0]+"]에 게시한 글에 "+chattyAlarm[1]+"개의 댓글이 추가되었습니다."))#게시글 관련 알림 추가
        
        
        for i in range(len(replyAlarm)):
                viewer.addItem(str("[강의: "+replyAlarm[i]+"]에 작성한 댓글이 채택되었습니다.")) #댓글 관련 알림 추가
        
        viewer.addItem(item) #혹시 몰라서 삭제 안함
        self.title.addWidget(group)
        self.title.addWidget(btn_remove_all,alignment=QtCore.Qt.AlignRight)
        self.mainLayout.addLayout(self.title)
        self.mainLayout.addWidget(horizon_line)
        self.mainLayout.addWidget(viewer)
        self.setLayout(self.mainLayout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = alarm()
    form.show()
    exit(app.exec_())