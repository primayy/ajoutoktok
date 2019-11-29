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

        #레이아웃 설정
        self.mainLayout=QVBoxLayout()
        self.rankWidget = QWidget()
        self.title = QHBoxLayout()
        self.myRankLayout = QVBoxLayout()

        #랭크 탭 설정
        self.tab = QTabWidget()
        self.tab.setStyleSheet('''
        QTabBar:tab{width:100px}''')

        #랭크 리스트 설정
        self.show_all = QListWidget(self)
        self.show_inDepart = QListWidget(self)
        self.show_compDepart = QListWidget(self)
        self.initUi()

    def initUi(self):

        #강의 목록 그리기
        group = QLabel('리더보드')
        group.setStyleSheet("font: 16pt 나눔스퀘어라운드 Regular;background:#eef5f6;color:#42808a")
        group.setAlignment(QtCore.Qt.AlignTop)
        #horizon_line = QLabel('─────────────────────')
            #구분선
        horizon_line = QLabel()
        horizon_img = QPixmap('./ui/afterlogin_ui/horizon_line.png')
        horizon_img = horizon_img.scaled(310,12,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        horizon_line.setPixmap(horizon_img)
        horizon_line.setAlignment(Qt.AlignTop)

        empty = QLabel(' ')


        self.myRankLabel = QLabel('내 등수는')
        self.myRankLabel.setStyleSheet("font: 10pt 나눔스퀘어라운드 Regular;")
        self.myRank = QLabel()
        self.myRank.setStyleSheet("font-size:14pt 나눔스퀘어라운드 Regular;")
        myPoint = QLabel()
        myPoint.setStyleSheet("font: 10pt 나눔스퀘어라운드 Regular;")
        mP = self.getMyPoint()

        tmp = "내 점수는 "+ mP + " Points!"
        myPoint.setText(tmp)

        self.myRankLayout.addWidget(self.myRankLabel)
        self.myRankLayout.addWidget(self.myRank)
        self.myRankLayout.addWidget(myPoint)

        ##### 첫화면에서 바로 전체 순위 확인할 수 있도록
        commend = "getRank "
        commend += "1 " + self.studId
        self.clientSocket.send(commend.encode('utf-8'))
        result = self.clientSocket.recv(1024).decode('utf-8')
        # print(str(result))
        UnivRank = str(result).split(" ")
        myRank = UnivRank.pop()
        myRank = str(myRank[0]) + " 등!"


        self.myRank.setText(myRank)
        for i in range(len(UnivRank)):
            if len(UnivRank[i])>0:
                allRank = UnivRank[i].split(",")

                if len(allRank)>0:
                    if i<3:
                        item = QListWidgetItem(self.show_all)
                        custom_widget = medalWidget(allRank,i)
                        item.setSizeHint(custom_widget.sizeHint())
                        self.show_all.setItemWidget(item, custom_widget)
                        self.show_all.addItem(item)
                        self.show_all.update()

                    else:
                        self.show_all.addItem(str(str(i+1)+"등- "+allRank[1]+" / " +allRank[0]+"Pt"))
                    #self.show_all.addItem(medal1_info_id)
            #########여기까지가 그 코드



        self.tab.addTab(self.show_all, "전체")
        self.tab.addTab(self.show_inDepart, "학과내")
        self.tab.addTab(self.show_compDepart, "학과별")

        self.tab.currentChanged.connect(self.tab.tabText)
        self.tab.currentChanged.connect(self.getRank)
        self.title.addWidget(group)
        self.mainLayout.addWidget(group)
        #self.mainLayout.addLayout(self.title)
        self.mainLayout.addWidget(horizon_line)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(empty)
        self.mainLayout.addWidget(self.myRankLabel,alignment=(QtCore.Qt.AlignCenter))
        self.mainLayout.addWidget(self.myRank,alignment=(QtCore.Qt.AlignCenter))
        self.mainLayout.addWidget(myPoint,alignment=(QtCore.Qt.AlignCenter))
        self.mainLayout.addWidget(empty)
        self.mainLayout.addStretch(1)
        #self.mainLayout.addLayout(self.myRankLayout)
        #self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.tab)
        self.mainLayout.addWidget(empty)
        self.mainLayout.addWidget(empty)
        self.mainLayout.addWidget(empty)
        self.mainLayout.addWidget(empty)
        self.tab.setMinimumSize(300,300)
        self.tab.setMaximumSize(300,400)

        self.setLayout(self.mainLayout)

    def getMyPoint(self):
        commend = "getMyPoint " + self.studId
        self.clientSocket.send(commend.encode('utf-8'))
        point = self.clientSocket.recv(1024)
        point = point.decode('utf-8')

        return point

    def getRank(self):
        commend = "getRank "
        if self.tab.tabText(self.tab.currentIndex()) == '전체':
            self.myRankLabel.setText('내 등수는')
            self.show_all.clear()
            commend += "1 " + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')
            # print(str(result))
            #등수 추가
            UnivRank = str(result).split(" ")
            myRank = UnivRank.pop()
            myRank = str(myRank[0]) +" 등!"
            self.myRank.setText(myRank)

            # for i in range(len(UnivRank)):
            #     if len(UnivRank[i])>0:#있을 때만, index out of range 오류 피하기
            #         allRank = UnivRank[i].split(",")
            #         if len(allRank)>0:#있을 때만, index out of range 오류 피하기
            #             self.show_all.addItem(str("Points: "+allRank[0]+" / 아이디: "+allRank[1]))
            for i in range(len(UnivRank)):
                if len(UnivRank[i])>0:
                    allRank = UnivRank[i].split(",")

                    if len(allRank)>0:
                        if i<3:
                            item = QListWidgetItem(self.show_all)
                            custom_widget = medalWidget(allRank,i)
                            item.setSizeHint(custom_widget.sizeHint())
                            self.show_all.setItemWidget(item, custom_widget)
                            self.show_all.addItem(item)
                            self.show_all.update()

                        else:
                            self.show_all.addItem(" "+str(str(i+1)+"등  "+allRank[1]+"      " +allRank[0]+"Pt"))


        elif self.tab.tabText(self.tab.currentIndex()) == '학과내':
            self.myRankLabel.setText('내 등수는')
            self.show_inDepart.clear()
            commend += "2 " + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')
            # print(str(result))
            #등수 추가
            inDeptRank = result.split(" ")
            myRank = inDeptRank.pop()
            myRank = str(myRank[0]) +" 등!"
            self.myRank.setText(myRank)
            # print(inDeptRank)
            for i in range(len(inDeptRank)):
                if len(inDeptRank[i])>0:#있을 때만, index out of range 오류 피하기
                    inDepartRank = inDeptRank[i].split(",")
                    # print(inDepartRank)
                    if len(inDepartRank)>0:#있을 때만, index out of range 오류 피하기
                        if i<3:
                            item = QListWidgetItem(self.show_inDepart)
                            custom_widget = medalWidget(inDepartRank,i)
                            item.setSizeHint(custom_widget.sizeHint())
                            self.show_inDepart.setItemWidget(item, custom_widget)
                            self.show_inDepart.addItem(item)
                            self.show_inDepart.update()

                    else:
                        self.show_inDepart.addItem("    "+str(str(i+1)+"등  "+inDepartRank[1]+"     " +inDepartRank[0]+"Pt"))
                        #self.show_inDepart.addItem(str("Points: "+inDepartRank[0]+" / 아이디: "+inDepartRank[1]))


        elif self.tab.tabText(self.tab.currentIndex()) == '학과별':
            self.myRankLabel.setText('우리과 등수는')
            self.show_compDepart.clear()
            commend += "3 " + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')
            # print(str(result))

            DeptRank = result.split(" ")
            myRank = DeptRank.pop()
            myRank = str(myRank[0]) +" 등!"
            self.myRank.setText(myRank)

            for i in range(len(DeptRank)):
                if len(DeptRank[i])>0:#있을 때만, index out of range 오류 피하기
                    compDepartRank = DeptRank[i].split(",")
                    if len(compDepartRank)>0:#있을 때만, index out of range 오류 피하기
                        if i<3:
                            item = QListWidgetItem(self.show_compDepart)
                            custom_widget = medalWidget(compDepartRank,i)
                            item.setSizeHint(custom_widget.sizeHint())
                            self.show_compDepart.setItemWidget(item, custom_widget)
                            self.show_compDepart.addItem(item)
                            self.show_compDepart.update()

                        else:
                            self.show_compDepart.addItem("  "+str(str(i+1)+"등  "+compDepartRank[1]+"       " +compDepartRank[0]+"Pt"))                       
                            #self.show_compDepart.addItem(str("Points: "+compDepartRank[0]+" / 학과: "+compDepartRank[1]))

class medalWidget(QWidget):
    def __init__(self, info,idx):
        super().__init__()

        medal_layout = QHBoxLayout()
        medal_info_layout = QVBoxLayout()
        medal_img = QLabel()

        # logo = QLabel()
        # ajoutoktok = QPixmap('./ui/login_ui/toktok_logo.png')
        # ajoutoktok= ajoutoktok.scaled(200,400,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        # logo.setPixmap(ajoutoktok)

        if idx==0:
            medal_img_file = QPixmap('./ui/board_ui/first.png')
            medal_img_file= medal_img_file.scaled(50,50,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
            medal_img.setPixmap(medal_img_file)

        elif idx==1:
            medal_img_file = QPixmap('./ui/board_ui/second.png')
            medal_img_file= medal_img_file.scaled(50,50,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
            medal_img.setPixmap(medal_img_file)

        elif idx==2:
            medal_img_file = QPixmap('./ui/board_ui/third.png')
            medal_img_file= medal_img_file.scaled(50,50,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
            medal_img.setPixmap(medal_img_file)

        medal_id = QLabel(info[1])
        medal_id.setStyleSheet('font:11pt 나눔스퀘어라운드 Regular;')
        medal_id.setAlignment(QtCore.Qt.AlignBottom)
        medal_point = QLabel(info[0]+'Pt')
        medal_point.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')

        medal_info_layout.addWidget(medal_id)
        medal_info_layout.addWidget(medal_point)
        medal_info_layout.setSpacing(0)

        medal_layout.addWidget(medal_img)
        medal_layout.setStretchFactor(medal_img,1)
        medal_layout.addLayout(medal_info_layout)
        medal_layout.setStretchFactor(medal_info_layout,4)
        medal_layout.setSpacing(5)
        self.setLayout(medal_layout)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = LeaderBoard(QApplication.activeWindow())
    form.show()
    exit(app.exec_())