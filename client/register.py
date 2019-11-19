import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class test(QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QVBoxLayout()
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
        student_name = QLabel('전혜진')

        #학과
        student_id_label = QLabel('학번')
        sutdent_id =  QLabel('201720713')

        #학과
        department_label = QLabel('학과')
        department = QLabel('')
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
        register_button.clicked.connect(self.register)

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

        # self.line.addWidget(self.name)
        # self.line.addWidget(self.id)
        # self.line.addWidget(self.department)
        # self.line.addWidget(self.nickname)

        #self.line.addStretch(1)
        self.mainLayout.addLayout(self.title)
        self.mainLayout.addWidget(horizon_line,alignment=Qt.AlignTop)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.name)
        self.mainLayout.addLayout(self.id)
        self.mainLayout.addLayout(self.department)
        self.mainLayout.addLayout(self.nickname)
        self.mainLayout.addWidget(register_button)
        self.mainLayout.addStretch(1)
        self.setFixedSize(358,600)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def nickname_overlap_check(self):
        print("중복확인")

    def register(self):
        print("등록완료")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = test()
    form.show()
    exit(app.exec_())