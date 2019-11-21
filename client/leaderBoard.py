import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class LeaderBoard(QWidget):
    def __init__(self,parent,studId):
        super().__init__()
        self.parent = parent
        self.studId = studId
        self.clientSocket = parent.clientSocket
        self.mainLayout=QVBoxLayout()
        self.rankWidget = QWidget()
        self.title = QHBoxLayout()
        self.tab = QTabWidget()
        self.tab.setStyleSheet('''
        QTabBar:tab{width:100px}''')
        self.initUi()

    def initUi(self):
        group = QLabel('리더보드')

        horizon_line = QLabel('─────────────────────')
        group.setStyleSheet('''
                        font-weight:bold;
                        font-size:16pt''')
        show_all = QListWidget(self)
        show_inDepart = QListWidget(self)
        show_compDepart = QListWidget(self)

        self.tab.addTab(show_all, "전체")
        self.tab.addTab(show_inDepart, "학과내")
        self.tab.addTab(show_compDepart, "학과별")

        self.tab.currentChanged.connect(self.getRank)

        self.title.addWidget(group)
        self.mainLayout.addLayout(self.title)
        self.mainLayout.addWidget(horizon_line)
        self.mainLayout.addWidget(self.tab)

        self.tab.setMinimumSize(300,500)

        self.setLayout(self.mainLayout)

    def getRank(self):
        commend = "getRank "
        if self.tab.tabText(self.tab.currentIndex()) == '전체':
            commend += "1 "  + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')
            print(str(result))

        elif self.tab.tabText(self.tab.currentIndex()) == '학과내':
            commend += "2 "  + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')
            print(str(result))

        elif self.tab.tabText(self.tab.currentIndex()) == '학과별':
            commend += "3 "  + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')
            print(str(result))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = LeaderBoard(QApplication.activeWindow())
    form.show()
    exit(app.exec_())