import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class profile(QWidget):

    def cngPic(self):
        print("Yeah!")

    def cngNic(self):
        print("Yeah!!")

    def LGout(self):
        print("Yeah!!!")

    def __init__(self, Nicky, quest, answe, pointearned, Department, studentId):
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.head = QHBoxLayout()
        self.body = QVBoxLayout()
        self.bodypart1 = QWidget(self)
        self.bodypart11 = QHBoxLayout()
        self.bodypart2 = QWidget(self)
        self.bodypart22 = QHBoxLayout()
        self.tail = QVBoxLayout()

        self.initUi(Nicky, quest, answe, pointearned, Department, studentId)

    def initUi(self, Nicky, quest, answe, pointearned, Department, studentId):
        self.headbodyDiv = QLabel('─────────────────────')
        self.bodytailDiv = QLabel('─────────────────────')

        title = QLabel('프로필')
        title.setStyleSheet('''
                        font-weight:bold;
                        font-size:16pt''')

        logoutbtn = QPushButton()
        logoutbtn.setMaximumHeight(200)
        logoutbtn.setMaximumWidth(200)
        logoutbtn.setStyleSheet('''
                                QPushButton{image:url(./icon/logout.png); border:0px; width:32px; height:42px}        
                                QPushButton:hover{background:rgba(0,0,0,0); border:0px}
                                ''')

        logoutbtn.clicked.connect(self.LGout)

        profilebtn = QPushButton()
        profilebtn.setMaximumHeight(200)
        profilebtn.setMaximumWidth(200)
        profilebtn.setStyleSheet('''
                                QPushButton{image:url(./icon/user.png); border:0px; width:32px; height:42px}        
                                QPushButton:hover{background:rgba(0,0,0,0); border:0px}
                                ''')
        profilebtn.clicked.connect(self.cngPic)

        nickname = QLabel(Nicky)
        changeNick = QPushButton("변경")
        changeNick.setMaximumHeight(100)
        changeNick.setMaximumWidth(150)
        changeNick.clicked.connect(self.cngNic)
        Query = QLabel("질문: " + quest)
        Respond = QLabel("답변: " + answe)
        Points = QLabel(pointearned + " points")

        Dept = QLabel("소속: " + Department)
        ID = QLabel("학번: " + studentId)

        self.bodypart11.addWidget(nickname)
        self.bodypart11.addWidget(changeNick)
        self.bodypart22.addWidget(Query)
        self.bodypart22.addWidget(Respond)

        self.bodypart1.setLayout(self.bodypart11)
        self.bodypart2.setLayout(self.bodypart22)

        self.head.addWidget(title)
        self.head.addWidget(logoutbtn, alignment=QtCore.Qt.AlignRight)

        self.body.addWidget(profilebtn, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(self.bodypart1, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(self.bodypart2, alignment=QtCore.Qt.AlignCenter)
        self.body.addWidget(Points, alignment=QtCore.Qt.AlignCenter)

        self.tail.addWidget(Dept)
        self.tail.addWidget(ID)

        self.mainLayout.addLayout(self.head)
        self.mainLayout.addWidget(self.headbodyDiv)
        self.mainLayout.addLayout(self.body)
        self.mainLayout.addWidget(self.bodytailDiv)
        self.mainLayout.addLayout(self.tail)
        self.setLayout(self.mainLayout)
        self.setFixedSize(self.sizeHint())
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = profile('A', 'A', 'A', 'A', 'A', 'A')
    form.show()
    exit(app.exec_())