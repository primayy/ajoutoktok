import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import after_login

class Register(QWidget):
    def __init__(self,window,name,studId):
        super().__init__()
        self.w = window
        self.clientSocket = window.clientSock
        self.studName = name
        self.studId = studId

        self.mainWidget = QWidget()
        self.widgetLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.widgetLayout)
        self.mainWidget.setStyleSheet('background-color:white')


        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.mainWidget)


        self.title = QHBoxLayout()

        self.id = QHBoxLayout()
        self.name = QHBoxLayout()
        self.department = QHBoxLayout()
        self.nickname = QHBoxLayout()

        self.line = QVBoxLayout()

        self.setLayout(self.mainLayout)
        self.initUi()

    def initUi(self):
        self.setWindowTitle('초기등록')

        init_register_label = QLabel('초기 등록')
        init_register_label.setAlignment(Qt.AlignTop)
        init_register_label.setStyleSheet('''font-weight: Bold; font-size: 16pt''')

        horizon_line = QLabel('─────────────────────')
        horizon_line.setAlignment(Qt.AlignTop)

        #이름
        student_name_label = QLabel('이름')
        student_name = QLabel(self.studName)

        #학과
        student_id_label = QLabel('학번')
        sutdent_id =  QLabel(self.studId)

        #학과
        department_label = QLabel('학과')
        department_comboBox = QComboBox(self)
        #디비에 있는 department 목록 불러오기 추가필요
        department_comboBox.addItem('소프트웨어학과')
        department_comboBox.addItem('전자공학과')
        department_comboBox.addItem('미디어학과')

        #닉네임
        nickname_label = QLabel('닉네임')
        nickname_textbox = QLineEdit()
        nickname_overlap = QPushButton('중복확인')
        nickname_overlap.clicked.connect(self.nickname_overlap_check)

        #등록
        register_button = QPushButton('등록')
        register_button.clicked.connect(lambda: self.register(nickname_textbox.text(),department_comboBox.currentText() ))

        self.title.addWidget(init_register_label)

        self.id.addWidget(student_id_label, alignment=(QtCore.Qt.AlignTop))
        self.id.addWidget(sutdent_id)

        self.name.addWidget(student_name_label)
        self.name.addWidget(student_name)

        self.department.addWidget(department_label)
        self.department.addWidget(department_comboBox)

        self.nickname.addWidget(nickname_label)
        self.nickname.addWidget(nickname_textbox)
        self.nickname.addWidget(nickname_overlap)

        self.widgetLayout.addLayout(self.title)
        self.widgetLayout.addWidget(horizon_line,alignment=Qt.AlignTop)
        self.widgetLayout.addStretch(1)
        self.widgetLayout.addLayout(self.name)
        self.widgetLayout.addLayout(self.id)
        self.widgetLayout.addLayout(self.department)
        self.widgetLayout.addLayout(self.nickname)
        self.widgetLayout.addWidget(register_button)
        self.widgetLayout.addStretch(1)

        self.setFixedSize(358,600)

    def nickname_overlap_check(self):
        print("중복확인")

    def register(self,nick,department):
        commend = 'register '+nick+" "+department+" "+self.studName+" "+self.studId
        self.clientSocket.send(commend.encode('utf-8'))

        print("등록완료")
        res = self.clientSocket.recv(1024)
        if res.decode('utf-8') == 'registered':
            commend = 'login ' + self.studId
            self.clientSocket.send(commend.encode('utf-8'))

            # 결과 도착
            server_msg = self.clientSocket.recv(1024)

            lectureId = server_msg.decode('utf-8')

            mainW = QApplication.activeWindow()
            self.afterLogin = after_login.App(mainW, self.studId, self.studName, lectureId)
            # self.afterLogin = after_login.App(mainW, ProfId, ProfName, lectureId)
            mainW.setCentralWidget(self.afterLogin)
            self.close()
    #움직이지 못하게 만듬
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        self.oldPos = event.globalPos()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Register()
    form.show()
    exit(app.exec_())