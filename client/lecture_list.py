import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import chat
import chat_test

class lecture_list(QWidget):
    def __init__(self,studid,lecid,w):
        super().__init__()
        self.studid = studid
        self.lecId = lecid
        self.w = w
        self.clientSocket = w.clientSock

        self.mainLayout=QVBoxLayout()
        self.title = QHBoxLayout()

        #강의 목록 그리기
        group = QLabel('강의 목록')
        horizon_line = QLabel('─────────────────────')

        group.setStyleSheet('''
                font-weight:bold;
                font-size:16pt''')
        self.viewer = QListWidget(self)

        self.viewer.setMinimumSize(300, 500)
        self.viewer.setStyleSheet('''
                # QListWidget:item:hover{background:white};
                # QListWidget:item{padding:0px}
                ''')
        lecture_list = self.getLectureList()
        for i in range(len(lecture_list)):
            item = QListWidgetItem(self.viewer)
            custom_widget = lecture_group(lecture_list[i], studid, QApplication.activeWindow(),self.viewer,self.lecId)
            item.setSizeHint(custom_widget.sizeHint())
            self.viewer.setItemWidget(item, custom_widget)
            self.viewer.addItem(item)

        item = QListWidgetItem(self.viewer)
        custom_widget = lecture_group('add', studid, QApplication.activeWindow(),self.viewer,self.lecId)
        item.setSizeHint(custom_widget.sizeHint())
        self.viewer.setItemWidget(item, custom_widget)
        self.viewer.addItem(item)

        # 메인 레이아웃 그리기
        self.title.addWidget(group)
        self.mainLayout.addLayout(self.title)
        self.mainLayout.addWidget(horizon_line)
        self.mainLayout.addWidget(self.viewer)
        self.setLayout(self.mainLayout)
        self.setWindowTitle('test')
        self.setStyleSheet("background-color:white")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def getLectureList(self):
        if self.lecId == 'x':
            return []
        else:
            lectureList = "lecture "
            for lectureId in self.lecId:
                lectureList += lectureId + " "
            lectureList = lectureList.rstrip()

            self.clientSocket.send(lectureList.encode('utf-8'))
            recv = self.clientSocket.recv(1024)

            list_parse = recv.decode('utf-8').split('/')
            list_parse.pop()
            return list_parse

class group_search_dialog(QDialog):
    def __init__(self,w,stuid,viewer,lecid):
        super().__init__()
        self.w = w
        self.clientSocket= w.clientSock
        self.stuid = stuid
        self.lecId = lecid
        self.viewer = viewer
        self.mainLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.initUi()

    def initUi(self):
        groupSearchBar = QLineEdit()
        groupSearchBar.setPlaceholderText('강의 코드')
        search = QPushButton('조회')
        cancel = QPushButton('취소')

        cancel.clicked.connect(self.close)
        self.btnLayout.addWidget(search)
        self.btnLayout.addWidget(cancel)
        search.clicked.connect(lambda: self.group_search(groupSearchBar.text()))

        self.mainLayout.addWidget(groupSearchBar)
        self.mainLayout.addLayout(self.btnLayout)
        self.setLayout(self.mainLayout)

    def group_search(self,group_title):
        commend = 'groupSearch ' + group_title
        self.clientSocket.send(commend.encode('utf-8'))
        # if 그룹이 존재
        recv = self.clientSocket.recv(1024)

        result_parse = recv.decode('utf-8').split(',')
        result_parse.pop()
        self.group_add(result_parse)

        # else 그룹 없음

    def group_add(self, result_parse):
        if len(result_parse) == 3:
            self.close()
            msg = QMessageBox()
            msg.setStyleSheet("background-color:#FFFFFF")
            msg.setText(result_parse[1] + " " + result_parse[2])
            group_add = msg.addButton('추가', QMessageBox.YesRole)
            group_cancel = msg.addButton('취소', QMessageBox.NoRole)
            msg.setWindowTitle("그룹 조회")
            msg.exec_()
            # 그룹 추가
            if msg.clickedButton() == group_add:
                # 그룹 추가 서버로 요청
                commend = "group_insert " + result_parse[0] + " " + str(self.stuid)
                self.clientSocket.send(commend.encode('utf-8'))
                # 반환 결과
                result = self.clientSocket.recv(1024)
                result = result.decode('utf-8')
                if result == 'already':
                    print('이미 있다')
                else:
                    self.lecId.append(result_parse[0])
                    self.viewer.clear()
                    lecture_list = self.getLectureList()
                    for i in range(len(lecture_list)):
                        item = QListWidgetItem(self.viewer)
                        custom_widget = lecture_group(lecture_list[i], self.stuid, QApplication.activeWindow(), self.viewer,
                                                      self.lecId)
                        item.setSizeHint(custom_widget.sizeHint())
                        self.viewer.setItemWidget(item, custom_widget)
                        self.viewer.addItem(item)

                    item = QListWidgetItem(self.viewer)
                    custom_widget = lecture_group('add', self.stuid, QApplication.activeWindow(), self.viewer, self.lecId)
                    item.setSizeHint(custom_widget.sizeHint())
                    self.viewer.setItemWidget(item, custom_widget)
                    self.viewer.addItem(item)

        else:
            msg = QMessageBox()
            msg.setStyleSheet("background-color:#FFFFFF")
            msg.setText("그룹이 존재하지 않습니다.")
            msg.setWindowTitle("그룹 조회")
            msg.exec_()

    def getLectureList(self):
        if self.lecId is 'x':
            return []
        else:
            lectureList = "lecture "
            for lectureId in self.lecId:
                lectureList += lectureId + " "
            lectureList = lectureList.rstrip()

            self.clientSocket.send(lectureList.encode('utf-8'))
            recv = self.clientSocket.recv(1024)

            list_parse = recv.decode('utf-8').split('/')
            list_parse.pop()
            return list_parse

class lecture(QWidget):
    def __init__(self, course,stuid,window,viewer,lecid):
        super().__init__()
        self.stuid = stuid
        self.lecid = lecid
        self.w = window
        self.viewer = viewer
        self.mainLayout = QVBoxLayout()
        self.mainWidget = QWidget()
        self.mainWidget.setStyleSheet('background-color:grey')
        self.mainWidget.setMinimumSize(200,80)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.mainWidget)
        self.course = course

        if course[0] is 'add':
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0,0,0,0)
            self.layout_middle = QHBoxLayout()

            # middle
            self.lecture = QPushButton()
            self.lecture.setStyleSheet('''border:0px;''')
            self.lecture.setIcon(QIcon('./icon/add.png'))
            self.lecture.setIconSize(QSize(40, 70))
            self.lecture.clicked.connect(lambda: self.group_search_popup(self.w))
            self.layout_middle.addWidget(self.lecture)

            self.layout.addLayout(self.layout_middle)

            self.mainWidget.setLayout(self.layout)
            self.setLayout(self.mainLayout)
        else:
            self.layout = QVBoxLayout()
            self.layout_middle = QHBoxLayout()
            self.layout_bottom = QHBoxLayout()

            # top
            self.btExit = QPushButton()
            self.btExit.setIconSize(QSize(13,13))
            self.btExit.setStyleSheet('''border:0px''')
            self.btExit.setIcon(QIcon('./icon/x.png'))

            # middle
            self.lecture = QLabel(course[0])
            self.layout_middle.addWidget(self.lecture)
            self.layout_middle.addWidget(self.btExit, alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))

            # bottom
            self.msg_widget = QPushButton()
            self.msg_widget.setMaximumHeight(20)
            self.msg_widget.setMaximumWidth(20)
            self.msg_widget.resize(20, 20)
            self.msg_widget.setStyleSheet('''border:0px''')
            self.msg_widget.setIcon(QIcon('./icon/msg_widget.png'))
            self.msg_widget.clicked.connect(self.msg_widget_on)
            self.prof = QLabel(course[1])
            self.layout_bottom.addWidget(self.prof)
            self.layout_bottom.addWidget(self.msg_widget, alignment=(QtCore.Qt.AlignRight))

            self.layout.addLayout(self.layout_middle)
            self.layout.addLayout(self.layout_bottom)
            self.mainWidget.setLayout(self.layout)
            self.setLayout(self.mainLayout)

    def group_search_popup(self,w):
        dlg = group_search_dialog(w,self.stuid,self.viewer,self.lecid)
        dlg.exec_()

    def mousePressEvent(self, QMouseEvent):
        title = self.course
        # self.chat = chat.chatRoom(title,self.stuid,self.w)
        self.chat = chat_test.chatRoom(self)

        self.chat.setWindowTitle(title[0])
        self.chat.setMinimumSize(QSize(400, 400))

    def msg_widget_on(self):
        print('aaa')

class lecture_group(QWidget):
    def __init__(self, courses,stuid,w,viewer,lecid):
        super().__init__()
        course = courses.split(',')

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(1,3,1,3)
        #그룹 그리기
        self.mainWidget = lecture(course,stuid,w,viewer,lecid)
        self.mainLayout.addWidget(self.mainWidget)
        self.setLayout(self.mainLayout)

    # def chatStart(self, title):
    #     self.chat = chat.chatRoom(title)
    #     self.chat.setWindowTitle(title)
    #     self.chat.setMinimumSize(QSize(400, 400))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = lecture_list('201520990','0')
    form.show()
    exit(app.exec_())