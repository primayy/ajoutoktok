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

        self.overlap_status =0

        self.mainWidget = QWidget()
        self.widgetLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.widgetLayout)
        self.mainWidget.setStyleSheet('background-color:#f2f2f2;')


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
        init_register_word = QPixmap('./ui/register_ui/초기등록2.png')
        init_register_word = init_register_word.scaled(277,53,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        init_register_label.setPixmap(init_register_word)
        #init_register_label.setAlignment(Qt.AlignTop)
        #init_register_label.setStyleSheet('''font-weight: Bold; font-size: 16pt''')

        #구분선
        horizon_line = QLabel()
        horizon_img = QPixmap('./ui/register_ui/구분선5.png')
        horizon_img = horizon_img.scaled(290,12,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        horizon_line.setPixmap(horizon_img)
        horizon_line.setAlignment(Qt.AlignTop)

        #안내
        explanation_label = QLabel()
        explanation_img = QPixmap('./ui/register_ui/안내문4.png')
        explanation_img = explanation_img.scaled(320,112,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        explanation_label.setPixmap(explanation_img)

        #이름
        student_name_label = QLabel(' 이름')
        student_name_label.setStyleSheet("font: 9pt 나눔바른펜")
        student_name = QLabel(self.studName)
        student_name.setStyleSheet("font: 9pt 나눔바른펜")


        #학번
        student_id_label = QLabel(' 학번')
        student_id_label.setStyleSheet("font: 9pt 나눔바른펜")
        # student_id_img = QPixmap('./ui/register_ui/학번.png')
        # student_id_img = student_id_img.scaled(75,47,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        # student_id_label.setPixmap(student_id_img)
        student_id =  QLabel(self.studId)
        student_id.setStyleSheet("font: 9pt 나눔바른펜")

        #학과
        department_label = QLabel('학과')
        department_label.setStyleSheet("font: 9pt 나눔바른펜")
        # department_img = QPixmap('./ui/register_ui/학과.png')
        # department_img = department_img.scaled(75,47,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        # department_label.setPixmap(department_img)
        
        department_comboBox = QComboBox(self)
        department_comboBox.setStyleSheet('''
                QListWidget:item:{background:white};
                QListWidget:item:hover{background:white};
                QListWidget:item{padding:0px; width:100px; height:23}
                ''')
        if 1==1:
        #if department_label_upper == '공과대학' :
            #department_comboBox.clear()
            department_comboBox.addItem('기계학과')
            department_comboBox.addItem('산업공학과')
            department_comboBox.addItem('화학공학과')
            department_comboBox.addItem('신소재공학과')
            department_comboBox.addItem('응용화학생명공학과')
            department_comboBox.addItem('환경안전공학과')
            department_comboBox.addItem('건설시스템공학과')
            department_comboBox.addItem('건축학과')
            department_comboBox.addItem('융합시스템공학과')

        #elif department_label_upper == '정보통신대학' :
            #department_comboBox.clear()
            department_comboBox.addItem('전자공학과')
            department_comboBox.addItem('미디어학과')
            department_comboBox.addItem('사이버보안학과')
            department_comboBox.addItem('소프트웨어학과')
            department_comboBox.addItem('국방디지털융합학과')
            
        #elif department_label_upper == '자연과학대학' :
            #department_comboBox.clear()
            department_comboBox.addItem('수학과')
            department_comboBox.addItem('화학과')
            department_comboBox.addItem('물리학과')
            department_comboBox.addItem('생명과학과')
            
        #elif department_label_upper == '경영대학' :
            #department_comboBox.clear()
            department_comboBox.addItem('경영학과')
            department_comboBox.addItem('금융공학과')
            department_comboBox.addItem('e-비즈니스학과')
            department_comboBox.addItem('글로벌경영학과')
            
        #elif department_label_upper == '인문대학' :
            #department_comboBox.clear()
            department_comboBox.addItem('국어국문학과')
            department_comboBox.addItem('불어불문학과')
            department_comboBox.addItem('문화콘텐츠학과')
            department_comboBox.addItem('영어영문학과')
            department_comboBox.addItem('사학과')
            
        #elif department_label_upper == '사회과학대학' :
            #department_comboBox.clear()
            department_comboBox.addItem('경제학과')
            department_comboBox.addItem('심리학과')
            department_comboBox.addItem('정치외교학과')
            department_comboBox.addItem('행정학과')
            department_comboBox.addItem('사회학과')
            department_comboBox.addItem('스포츠레저학과')
            
        #elif department_label_upper == '의과대학' :
            #department_comboBox.clear()
            department_comboBox.addItem('의학과')
            
        #elif department_label_upper == '간호대학' :
            #department_comboBox.clear()
            department_comboBox.addItem('간호학과')
            
        #elif department_label_upper == '약학대학' :
            #department_comboBox.clear()
            department_comboBox.addItem('약학대학')
            
        #elif department_label_upper == '다산학부대학' :
            #department_comboBox.clear()
            department_comboBox.addItem('다산학부대학')
            
        #elif department_label_upper == '국제학부' :
            #department_comboBox.clear()
            department_comboBox.addItem('국제학부')



        #닉네임
        nickname_label = QLabel('닉네임')
        nickname_label.setStyleSheet("font: 9pt 나눔바른펜")
        self.nickname_textbox = QLineEdit()
        self.nickname_textbox.setStyleSheet('height:20; width:90px')
        self.nickname_overlap = QPushButton()
        self.nickname_overlap.setStyleSheet('''
                        QPushButton{image:url(./ui/register_ui/중복확인.png); border:0px; width:100px; height:50px}
                        ''')
        self.nickname_overlap.clicked.connect(self.nickname_overlap_check)

       #등록
        register_button = QPushButton()
        register_button.setStyleSheet('''
                        QPushButton{image:url(./ui/register_ui/등록.png); border:0px; width:95px; height:45px}        
                        
                        ''')
        register_button.clicked.connect(lambda: self.register(self.nickname_textbox.text(),department_comboBox.currentText() ))
        
        self.title.addWidget(init_register_label,alignment=(QtCore.Qt.AlignCenter))

        self.name.addWidget(student_name_label)
        self.name.addWidget(student_name)
        self.name.addStretch(1)

        self.id.addWidget(student_id_label, alignment=(QtCore.Qt.AlignTop))
        self.id.addWidget(student_id)
        self.id.addStretch(1)

        self.department.addStretch(1)
        self.department.addWidget(department_label)
        self.department.addWidget(department_comboBox)
        self.department.addStretch(12)

        self.nickname.addStretch(1)
        self.nickname.addWidget(nickname_label)
        self.nickname.addWidget(self.nickname_textbox)
        self.nickname.addWidget(self.nickname_overlap)
        self.nickname.addStretch(4)

        self.widgetLayout.addStretch(2)
        self.widgetLayout.addLayout(self.title)
        #self.widgetLayout.addWidget(horizon_line,alignment=Qt.AlignTop)
        self.widgetLayout.addWidget(explanation_label)
        #self.widgetLayout.addStretch(1)
        self.widgetLayout.addLayout(self.name)
        self.widgetLayout.addLayout(self.id)
        self.widgetLayout.addLayout(self.department)
        self.widgetLayout.addLayout(self.nickname)
        self.widgetLayout.addWidget(register_button)
        self.widgetLayout.addStretch(3)

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
            self.overlap_status=1
            self.overlap_button_toggle()
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


    def overlap_button_toggle(self):
        if (self.overlap_status == True):
            self.nickname_overlap.setStyleSheet('''
                                QPushButton{image:url(./ui/register_ui/확인완료.png); border:0px; width:100px; height:50px}                        
                                ''')
            self.widget_on_off_button_status = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Register()
    form.show()
    exit(app.exec_())