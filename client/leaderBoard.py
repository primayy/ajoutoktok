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
        self.show_all = QListWidget(self)
        self.show_inDepart = QListWidget(self)
        self.show_compDepart = QListWidget(self)
        self.initUi()

    def initUi(self):
        group = QLabel('리더보드')

        horizon_line = QLabel('─────────────────────')
        group.setStyleSheet('''
                        font-weight:bold;
                        font-size:16pt''')
        ##### 첫화면에서 바로 전체 순위 확인할 수 있도록
        commend = "getRank "
        commend += "1 " + self.studId
        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(1024).decode('utf-8')
        # print(str(result))
        UnivRank = str(result).split(" ")
        for i in range(len(UnivRank)):
            if len(UnivRank[i])>0:
                allRank = UnivRank[i].split(",")
                if len(allRank)>0:
                    self.show_all.addItem(str("Points: "+allRank[0]+" / 아이디: "+allRank[1]))
            #########여기까지가 그 코드



        self.tab.addTab(self.show_all, "전체")
        self.tab.addTab(self.show_inDepart, "학과내")
        self.tab.addTab(self.show_compDepart, "학과별")

        self.tab.currentChanged.connect(self.tab.tabText)
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
            self.show_all.clear()
            commend += "1 " + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')
            # print(str(result))
            UnivRank = str(result).split(" ")
            for i in range(len(UnivRank)):
                if len(UnivRank[i])>0:#있을 때만, index out of range 오류 피하기
                    allRank = UnivRank[i].split(",")
                    if len(allRank)>0:#있을 때만, index out of range 오류 피하기
                        self.show_all.addItem(str("Points: "+allRank[0]+" / 아이디: "+allRank[1]))

            

        elif self.tab.tabText(self.tab.currentIndex()) == '학과내':
            self.show_inDepart.clear()
            commend += "2 " + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')
            # print(str(result))
            inDeptRank = result.split(" ")
            # print(inDeptRank)
            for i in range(len(inDeptRank)):
                if len(inDeptRank[i])>0:#있을 때만, index out of range 오류 피하기
                    inDepartRank = inDeptRank[i].split(",")
                    # print(inDepartRank)
                    if len(inDepartRank)>0:#있을 때만, index out of range 오류 피하기
                        self.show_inDepart.addItem(str("Points: "+inDepartRank[0]+" / 아이디: "+inDepartRank[1]))


        elif self.tab.tabText(self.tab.currentIndex()) == '학과별':
            self.show_compDepart.clear()
            commend += "3 " + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')
            # print(str(result))
            DeptRank = result.split(" ")
            # print(DeptRank)
            for i in range(len(DeptRank)):
                if len(DeptRank[i])>0:#있을 때만, index out of range 오류 피하기
                    compDepartRank = DeptRank[i].split(",")
                    if len(compDepartRank)>0:#있을 때만, index out of range 오류 피하기
                        self.show_compDepart.addItem(str("Points: "+compDepartRank[0]+" / 학과: "+compDepartRank[1]))
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = LeaderBoard(QApplication.activeWindow())
    form.show()
    exit(app.exec_())