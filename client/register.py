import sys
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import after_login

class Register(QWidget):
    def __init__(self,parent,window,name,studId):
        super().__init__()
        self.w = window
        self.clientSocket = window.clientSock
        self.studName = name
        self.studId = studId

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

        init_register_label = QLabel()
        #init_register_label.setAlignment(Qt.AlignTop)
        #init_register_label.setStyleSheet('''font-weight: Bold; font-size: 16pt''')
        init_register_word = QPixmap('./ui/register_ui/초기등록2.png')
        init_register_word = init_register_word.scaled(122,53,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        init_register_label.setPixmap(init_register_word)

        # logo = QLabel()
        # ajoutoktok = QPixmap('./ui/register_ui/toktok_logo.png')
        # ajoutoktok= ajoutoktok.scaled(200,400,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        # logo.setPixmap(ajoutoktok)

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
        student_name_label = QLabel('이름')
        #student_name_label.setStyleSheet('''font-size: 10pt; font-family:NanumSquareRoundB''')
        # student_name_img = QPixmap('./ui/register_ui/이름.png')
        # student_name_img = student_name_img.scaled(60,40,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        # student_name_label.setPixmap(student_name_img)
        student_name_label.setStyleSheet("font: 9pt 나눔바른펜")
        student_name = QLabel(self.studName)
        
        #student_name_label.setFont(QtGui.QFont("궁서",20))
        
        #student_name_label.setStyleSheet('QLabel{font-family:NanumSquareRoundB}')
        
        #학번
        student_id_label = QLabel('학번')
        student_id_label.setStyleSheet("font: 9pt 나눔바른펜")
        # student_id_img = QPixmap('./ui/register_ui/학번.png')
        # student_id_img = student_id_img.scaled(75,47,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        # student_id_label.setPixmap(student_id_img)
        sutdent_id =  QLabel(self.studId)

        #학과
        department_label = QLabel('학과')
        department_label.setStyleSheet("font: 9pt 나눔바른펜")
        # department_img = QPixmap('./ui/register_ui/학과.png')
        # department_img = department_img.scaled(75,47,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        # department_label.setPixmap(department_img)
        
        department_comboBox = QComboBox(self)
        #디비에 있는 department 목록 불러오기 추가필요
        department_comboBox.addItem('소프트웨어학과')
        department_comboBox.addItem('전자공학과')
        department_comboBox.addItem('미디어학과')

        #닉네임
        nickname_label = QLabel('닉네임')
        nickname_label.setStyleSheet("font: 9pt 나눔바른펜")
        nickname_textbox = QLineEdit()
        nickname_overlap = QPushButton()
        nickname_overlap.setStyleSheet('''
                        QPushButton{image:url(./ui/register_ui/중복확인.png); border:0px; width:100px; height:50px}
                        ''')
        nickname_overlap.clicked.connect(self.nickname_overlap_check)

        #등록
        register_button = QPushButton()
        register_button.setStyleSheet('''
                        QPushButton{image:url(./ui/register_ui/등록.png); border:0px; width:100px; height:50px}        
                        
                        ''')
        register_button.clicked.connect(lambda: self.register(nickname_textbox.text(),department_comboBox.currentText() ))
        #self.subLayer.addWidget(logo, alignment=(QtCore.Qt.AlignCenter|QtCore.Qt.AlignTop))
        #self.title.addWidget(init_register_label, alignment=(QtCore.Qt.AlignCenter|QtCore.Qt.AlignTop))
        self.title.addWidget(init_register_label, alignment=(QtCore.Qt.AlignCenter|QtCore.Qt.AlignTop))

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
        self.widgetLayout.addWidget(horizon_line,alignment=Qt.AlignTop|Qt.AlignCenter)
        self.widgetLayout.addWidget(explanation_label,alignment=Qt.AlignTop)
        self.widgetLayout.addStretch(1)
        self.widgetLayout.addLayout(self.name)
        self.widgetLayout.addLayout(self.id)
        self.widgetLayout.addLayout(self.department)
        self.widgetLayout.addLayout(self.nickname)
        self.widgetLayout.addWidget(register_button)
        self.widgetLayout.addStretch(3)

        self.setFixedSize(358,600)

    def nickname_overlap_check(self):
        print("중복확인")
        #user 테이블 닉네임 항목 보고

        #중복이면
        
            
        #아니면

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Register()
    form.show()
    exit(app.exec_())