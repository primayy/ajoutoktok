import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import after_login
from bs4 import BeautifulSoup

class Register(QWidget):
    def __init__(self,parent,window,name,studId):
        super().__init__()
        self.w = window
        self.clientSocket = window.clientSock
        self.studName = name
        self.studId = studId
        self.session = parent.session

        self.courses = self.getCourses()

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
        self.regi_qual = 0 #가입가능한지아닌지

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
        self.nickname_textbox = QLineEdit()
        nickname_overlap = QPushButton('중복확인')
        nickname_overlap.clicked.connect(self.nickname_overlap_check)

        #등록
        register_button = QPushButton('등록')
        register_button.clicked.connect(lambda: self.register(self.nickname_textbox.text(),department_comboBox.currentText() ))

        self.title.addWidget(init_register_label)

        self.id.addWidget(student_id_label, alignment=(QtCore.Qt.AlignTop))
        self.id.addWidget(sutdent_id)

        self.name.addWidget(student_name_label)
        self.name.addWidget(student_name)

        self.department.addWidget(department_label)
        self.department.addWidget(department_comboBox)

        self.nickname.addWidget(nickname_label)
        self.nickname.addWidget(self.nickname_textbox)
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
        self.show

    def getCourses(self):
        res = ""

        session = self.session
        u = 'https://eclass2.ajou.ac.kr/webapps/portal/execute/tabs/tabAction'

        custom_header = {
            'referer': 'https://eclass2.ajou.ac.kr:8443/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

        course_get = session.get(u, headers=custom_header,
                                 params="action=refreshAjaxModule&modId=_3_1&tabId=_1_1&tab_tab_group_id=_1_1")
        soup = BeautifulSoup(course_get.text, 'lxml')

        courses = soup.select(''
                              '#_3_1termCourses__15_1 > ul > li > a'
                              '')

        #블랙보드에서 학기별 분류 안해놨을 경우
        if len(courses) == 0:
            courses = soup.select(''
                                  '#_3_1termCourses_noterm > ul > li > a'
                                  '')

            for course in courses:
                print(course.text)
                if course.text == "Blackboard Learn 소개하기 (학습자용)":
                    continue
                else:
                    temp = ' '.join(course.text.split(' ')[1:])
                    course_name = temp.split('(')[0]
                    course_code = temp.split('(')[1].split(')')[0]
                    res += course_name + ',' + course_code + '/'

            return res
        else:
            for course in courses:
                temp = ' '.join(course.text.split(' ')[1:])
                course_name = temp.split('(')[0]
                course_code = temp.split('(')[1].split(')')[0]
                res += course_name+','+course_code+'/'

            # print(res)
            return res

    def nickname_overlap_check(self):
        commend = "OvelapCheck "
        commend += self.nickname_textbox.text()
        self.clientSocket.send(commend.encode('utf-8'))
        print("중복확인")
        answer = self.clientSocket.recv(1024).decode('utf-8')
        if answer == "newone":
            self.regi_qual=1
        elif answer == "overlap":
            self.regi_qual=2

    def register(self,nick,department):
        if self.regi_qual == 1 :#새로운 아이디일때 (밑으로는 모두 한단계 indendation이 되었다.)
            commend = 'register '+nick+" "+department+" "+self.studName+" "+self.studId
            self.clientSocket.send(commend.encode('utf-8'))

            print("등록완료")
            res = self.clientSocket.recv(1024)
            if res.decode('utf-8') == 'registered':
                commend = 'courses_create '+self.studId + " " + self.courses
                self.clientSocket.send(commend.encode('utf-8'))

                course_res = self.clientSocket.recv(1024).decode('utf-8')
                # print(course_res)

                commend = 'login ' + self.studId
                self.clientSocket.send(commend.encode('utf-8'))

                # 결과 도착
                server_msg = self.clientSocket.recv(1024)

                lectureId = server_msg.decode('utf-8')

                mainW = QApplication.activeWindow()
                self.afterLogin = after_login.App(mainW, self.studId, self.studName, lectureId)
                mainW.setCentralWidget(self.afterLogin)
                self.close()
        elif self.regi_qual == 0 :
            print("중복검사 하세요")
        elif self.regi_qual == 2 :
            print("아이디 중복")
            
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