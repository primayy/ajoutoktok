import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import chat_test
import msget

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
        group.setStyleSheet("font: 16pt 나눔스퀘어라운드 Regular;background:#eef5f6;color:#42808a")
        #horizon_line = QLabel('─────────────────────')
            #구분선
        horizon_line = QLabel()
        horizon_img = QPixmap('./ui/afterlogin_ui/horizon_line.png')
        horizon_img = horizon_img.scaled(310,12,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        horizon_line.setPixmap(horizon_img)
        horizon_line.setAlignment(Qt.AlignTop)
        
        self.viewer = QListWidget(self)

        self.viewer.setMinimumSize(300, 500)
        self.viewer.setStyleSheet('''
                QListWidget:item:hover{background:#95c3cb};
                # QListWidget:item{padding:0px}
                ''')
        self.lecture_list = self.getLectureList()
        self.showLectures()
        # for i in range(len(lecture_list)):
        #     item = QListWidgetItem(self.viewer)
        #     custom_widget = lecture_group(lecture_list[i], QApplication.activeWindow(),self)
        #     item.setSizeHint(custom_widget.sizeHint())
        #     self.viewer.setItemWidget(item, custom_widget)
        #     self.viewer.addItem(item)
        #
        # item = QListWidgetItem(self.viewer)
        # custom_widget = lecture_group('add', QApplication.activeWindow(),self)
        # item.setSizeHint(custom_widget.sizeHint())
        # self.viewer.setItemWidget(item, custom_widget)
        # self.viewer.addItem(item)

        # 메인 레이아웃 그리기
        self.title.addWidget(group)
        self.mainLayout.addLayout(self.title)
        self.mainLayout.addWidget(horizon_line)
        self.mainLayout.addWidget(self.viewer)
        self.setLayout(self.mainLayout)
        self.setWindowTitle('test')
        self.setStyleSheet("background-color:white")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def showLectures(self):
        for i in range(len(self.lecture_list)):
            item = QListWidgetItem(self.viewer)
            custom_widget = lecture_group(self.lecture_list[i], QApplication.activeWindow(),self)
            item.setSizeHint(custom_widget.sizeHint())
            self.viewer.setItemWidget(item, custom_widget)
            self.viewer.addItem(item)

        item = QListWidgetItem(self.viewer)
        
        custom_widget = lecture_group('add', QApplication.activeWindow(),self)
        item.setSizeHint(custom_widget.sizeHint())
        self.viewer.setItemWidget(item, custom_widget)
        self.viewer.addItem(item)

    def getLectureList(self):
        if len(self.lecId) == 0:
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
    # def __init__(self,w,stuid,viewer,lecid):
    def __init__(self, w,lecture_list_widget):

        super().__init__()
        self.w = w
        self.clientSocket= w.clientSock
        self.lecture_list_widget = lecture_list_widget
        self.stuid = lecture_list_widget.studid
        self.lecId = lecture_list_widget.lecId
        self.viewer = lecture_list_widget.viewer

        self.mainLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.initUi()

    def initUi(self):
        if 'Prof' in str(self.stuid):
            groupSearchBar = QLineEdit()
            groupSearchBar.setPlaceholderText('강의명')
            search = QPushButton('생성')
            search.clicked.connect(lambda: self.group_insert(groupSearchBar.text()))
            cancel = QPushButton('취소')
        
        else:
            groupSearchBar = QLineEdit()
            groupSearchBar.setPlaceholderText('강의 코드')
            search = QPushButton('조회')
            search.clicked.connect(lambda: self.group_search(groupSearchBar.text()))
            cancel = QPushButton('취소')

        cancel.clicked.connect(self.close)
        self.btnLayout.addWidget(search)
        self.btnLayout.addWidget(cancel)


        self.mainLayout.addWidget(groupSearchBar)
        self.mainLayout.addLayout(self.btnLayout)
        self.setLayout(self.mainLayout)

    def group_search(self,lecture_code):
        commend = 'groupSearch ' + lecture_code
        self.clientSocket.send(commend.encode('utf-8'))
        # if 그룹이 존재
        recv = self.clientSocket.recv(1024)

        result_parse = recv.decode('utf-8').split(',')
        # result_parse.pop()
        print(result_parse)
        self.group_add(result_parse)

        # else 그룹 없음


    def group_insert(self,group_title):
        commend = 'groupInsert ' + group_title +' '+ str(self.stuid)
        self.clientSocket.send(commend.encode('utf-8'))
        # if 그룹이 존재
        recv = self.clientSocket.recv(1024)

        result_parse = recv.decode('utf-8')
        
        if result_parse == "add_success":
            lecture_list = self.getLectureList()
            for i in range(len(lecture_list)):
                lecture(self.lecture_list_widget,lecture_list[i])

        else:
            msg = QMessageBox()
            msg.setStyleSheet("background-color:#FFFFFF")
            msg.setText("이미 존재하는 강의입니다.")
            group_cancel = msg.addButton('확인', QMessageBox.NoRole)
            msg.setWindowTitle("강의 생성")
            msg.exec_()

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
                commend = "group_add " + result_parse[0] + " " + str(self.stuid)
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
                        custom_widget = lecture_group(lecture_list[i], QApplication.activeWindow(),self.lecture_list_widget)
                        item.setSizeHint(custom_widget.sizeHint())
                        self.viewer.setItemWidget(item, custom_widget)
                        self.viewer.addItem(item)

                    item = QListWidgetItem(self.viewer)
                    custom_widget = lecture_group('add', QApplication.activeWindow(), self.lecture_list_widget)
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

class lecture(QWidget):
    def __init__(self, lecture_list_Widget, course,window):
        super().__init__()
        self.lecture_list_Widget = lecture_list_Widget
        self.stuid = lecture_list_Widget.studid
        self.lecid = lecture_list_Widget.lecId
        self.chat = 0

        self.w = window
        self.clientSocket = self.w.clientSock
        self.viewer = lecture_list_Widget.viewer
        self.course = course

        self.mainLayout = QVBoxLayout()
        self.mainWidget = QWidget()
        self.mainWidget.setStyleSheet("background-color:#eef5f6;")
        self.mainWidget.setMinimumSize(100,50)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.mainWidget)

        if course[0] == 'add':
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0,0,0,0)
            self.layout_middle = QHBoxLayout()

            # middle
            self.lecture = QPushButton()
            self.lecture.setStyleSheet('''border:2px;''')
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
            self.btExit.clicked.connect(self.exitLecture)

            # middle
            self.lecture = QLabel(course[0])
            self.lecture.setStyleSheet('font: 10pt 나눔스퀘어라운드 Regular;background:#eef5f6;color:#42808a')
            #font: 20pt 나눔스퀘어라운드 Regular;background:#eef5f6;color:#42808a
            # print(course)
            self.layout_middle.addWidget(self.lecture)
            self.layout_middle.addWidget(self.btExit, alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))

            # bottom
            self.msg_widget = QPushButton()
            self.msg_widget.setMaximumHeight(23)
            self.msg_widget.setMaximumWidth(23)
            self.msg_widget.resize(23, 23)
            self.msg_widget.setStyleSheet('''border:0px''')
            self.msg_widget.setIcon(QIcon('./ui/afterlogin_ui/bubble.png'))
            self.prof = QLabel(course[1])
            self.prof.setStyleSheet('font: 8pt 나눔스퀘어라운드 Regular;background:#eef5f6;color:#42808a')
            self.msg_widget.clicked.connect(self.msg_widget_on)
            self.layout_bottom.addWidget(self.prof)
            self.layout_bottom.addWidget(self.msg_widget, alignment=(QtCore.Qt.AlignRight))

            self.layout.addLayout(self.layout_middle)
            self.layout.addLayout(self.layout_bottom)
            self.mainWidget.setLayout(self.layout)
            self.setLayout(self.mainLayout)

    def exitLecture(self):
        commend = "exitLecture " +self.stuid + " " + self.course[1]

        self.clientSocket.send(commend.encode('utf-8'))

        res = self.clientSocket.recv(1024)
        res = res.decode('utf-8')

        #삭제한 강의id를 강의id 리스트에서 삭제
        self.lecture_list_Widget.lecId.remove(res)

        #다시 읽어오는거 필요함
        self.lecture_list_Widget.viewer.clear()
        self.lecture_list_Widget.lecture_list = self.lecture_list_Widget.getLectureList()
        self.lecture_list_Widget.showLectures()

    def group_search_popup(self,w):
        # dlg = group_search_dialog(w,self.stuid,self.viewer,self.lecid)
        dlg = group_search_dialog(w,self.lecture_list_Widget)
        dlg.exec_()

    def mousePressEvent(self, QMouseEvent):
        title = self.course

        if self.chat == 0:
            self.chat = chat_test.chatRoom(self)

            self.chat.setWindowTitle(title[0])
            self.chat.setMinimumSize(QSize(400, 400))

    def msg_widget_on(self):
        self.mwidget = msget.Invisible(self,self.lecture,self.prof)
        self.mwidget.setMinimumSize(QSize(200, 200))

class lecture_group(QWidget):
    def __init__(self, courses,w,parent):
        super().__init__()
        self.parent = parent
        course = courses.split(',')
        # print(course)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5,5,5,5)
        #그룹 그리기
        # self.mainWidget = lecture(course, parent.studid, w, parent.viewer, parent.lecId)
        self.mainWidget = lecture(self.parent, course, w)

        self.mainLayout.addWidget(self.mainWidget)
        self.setLayout(self.mainLayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = lecture_list('201520990','0')
    form.show()
    exit(app.exec_())