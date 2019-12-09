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
        self.myRankLayout.setContentsMargins(0,0,0,0)

        #랭크 탭 설정
        self.tab = QTabWidget()
        self.tab.setStyleSheet('''
        QTabBar:tab{width:100px}''')

        #랭크 리스트 설정
        self.show_all = QListWidget(self)
        self.show_all.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show_all.setStyleSheet('''
                QListWidget:item:hover{background:#95c3cb};
                ''')
        self.show_all.setContentsMargins(0,0,0,0)

        self.show_inDepart = QListWidget(self)
        self.show_inDepart.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show_inDepart.setStyleSheet('''
                QListWidget:item:hover{background:#95c3cb};
                ''')

        self.show_compDepart = QListWidget(self)
        self.show_compDepart.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show_compDepart.setStyleSheet('''
                QListWidget:item:hover{background:#95c3cb};
                ''')
        self.initUi()

    def initUi(self):

        #강의 목록 그리기
        group = QLabel('리더보드')
        group.setStyleSheet("font: 16pt 나눔스퀘어라운드 Regular;background:#eef5f6;color:#42808a")
        group.setAlignment(QtCore.Qt.AlignTop)

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

        UnivRank = str(result).split("!#!#")


        myRank = UnivRank.pop()

        myRank = str(myRank) + " 등!"

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
                        #self.show_all.addItem(str(str(i+1)+"등- "+allRank[1]+" / " +allRank[0]+"Pt"))
                        item2 =QListWidgetItem(self.show_all)
                        custom_widget2 = elseWidget(allRank,i)
                        item2.setSizeHint(custom_widget2.sizeHint())
                        self.show_all.setItemWidget(item2, custom_widget2)
                        self.show_all.addItem(item2)
                        self.show_all.update()


            #########여기까지가 그 코드


        
        self.tab.addTab(self.show_all, "   전체   ")
        self.tab.setStyleSheet('font:10pt 나눔스퀘어라운드 Regular;')
        self.tab.addTab(self.show_inDepart, "학과내")
        self.tab.addTab(self.show_compDepart, "학과별")
        self.tab.setContentsMargins(0,0,0,0)
        
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

        self.mainLayout.addWidget(self.tab)
        self.mainLayout.addWidget(empty)
        self.mainLayout.addWidget(empty)
        self.mainLayout.addWidget(empty)
        self.mainLayout.addWidget(empty)
        self.tab.setMinimumSize(310,320)
        self.tab.setMaximumSize(310,320)

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

            #등수 추가
            UnivRank = str(result).split("!#!#")

            myRank = UnivRank.pop()
            myRank = str(myRank) +" 등!"

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
                            item2 =QListWidgetItem(self.show_all)
                            custom_widget2 = elseWidget(allRank,i)
                            item2.setSizeHint(custom_widget2.sizeHint())
                            self.show_all.setItemWidget(item2, custom_widget2)
                            self.show_all.addItem(item2)
                            self.show_all.update()


        elif self.tab.tabText(self.tab.currentIndex()) == '학과내':
            self.myRankLabel.setText('내 등수는')
            self.show_inDepart.clear()
            commend += "2 " + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')

            #등수 추가
            inDeptRank = result.split("!#!#")
            myRank = inDeptRank.pop()
            myRank = str(myRank) +" 등!"
            self.myRank.setText(myRank)

            for i in range(len(inDeptRank)):
                if len(inDeptRank[i])>0:#있을 때만, index out of range 오류 피하기
                    inDepartRank = inDeptRank[i].split(",")

                    if len(inDepartRank)>0:#있을 때만, index out of range 오류 피하기
                        if i<3:
                            item = QListWidgetItem(self.show_inDepart)
                            custom_widget = medalWidget(inDepartRank,i)
                            item.setSizeHint(custom_widget.sizeHint())
                            self.show_inDepart.setItemWidget(item, custom_widget)
                            self.show_inDepart.addItem(item)
                            self.show_inDepart.update()

                        else:
                            item2 =QListWidgetItem(self.show_inDepart)
                            custom_widget2 = elseWidget(inDepartRank,i)
                            item2.setSizeHint(custom_widget2.sizeHint())
                            self.show_inDepart.setItemWidget(item2, custom_widget2)
                            self.show_inDepart.addItem(item2)
                            self.show_inDepart.update()
                        


        elif self.tab.tabText(self.tab.currentIndex()) == '학과별':
            self.myRankLabel.setText('우리과 등수는')
            self.show_compDepart.clear()
            commend += "3 " + self.studId
            self.clientSocket.send(commend.encode('utf-8'))
            result = self.clientSocket.recv(1024).decode('utf-8')

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
                            item2 =QListWidgetItem(self.show_compDepart)
                            custom_widget2 = elseWidget(compDepartRank,i)
                            item2.setSizeHint(custom_widget2.sizeHint())
                            self.show_compDepart.setItemWidget(item2, custom_widget2)
                            self.show_compDepart.addItem(item2)
                            self.show_compDepart.update()

class medalWidget(QWidget):
    def __init__(self, info,idx):
        super().__init__()
        medal_layout = QHBoxLayout()
        medal_id_point_layout = QHBoxLayout()
        medal_info_layout = QVBoxLayout()
        medal_info_layout.setContentsMargins(0,0,0,0)
        medal_img = QLabel()

        if idx==0:
            medal_img_file = QPixmap('./ui/board_ui/first.png')
            medal_img_file= medal_img_file.scaled(45,45,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
            medal_img.setPixmap(medal_img_file)

        elif idx==1:
            medal_img_file = QPixmap('./ui/board_ui/second.png')
            medal_img_file= medal_img_file.scaled(45,45,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
            medal_img.setPixmap(medal_img_file)

        elif idx==2:
            medal_img_file = QPixmap('./ui/board_ui/third.png')
            medal_img_file= medal_img_file.scaled(45,45,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
            medal_img.setPixmap(medal_img_file)

        medal_id = QLabel(" " +info[1])
        medal_id.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')
        medal_id.setMaximumWidth(160)
        medal_id.setAlignment(QtCore.Qt.AlignBottom)

        self.medal_aboutMe = QTextBrowser()
        if len(info) >2:
            self.medal_aboutMe.setText(info[2])

        self.medal_aboutMe.setStyleSheet('font:8pt 나눔스퀘어라운드 Regular;border:0px; background-color:#eef5f6;color:#737373')
        self.medal_aboutMe.setMaximumWidth(215)
        self.medal_aboutMe.setMaximumHeight(47)
        self.medal_aboutMe.setAlignment(QtCore.Qt.AlignBottom)

        medal_point = QLabel(info[0]+'Pt')
        medal_point.setStyleSheet('font:8pt 나눔스퀘어라운드 Regular;')

        medal_id_point_layout.addWidget(medal_id)
        medal_id_point_layout.setStretchFactor(medal_id,5)
        medal_id_point_layout.addWidget(medal_point)
        medal_id_point_layout.setStretchFactor(medal_point,1)
        #medal_info_layout.addWidget(medal_id)
        medal_info_layout.addLayout(medal_id_point_layout)
        medal_info_layout.addWidget(self.medal_aboutMe)
        #medal_info_layout.addWidget(medal_point)
        medal_info_layout.setSpacing(0)

        medal_layout.addWidget(medal_img)
        medal_layout.setStretchFactor(medal_img,1)
        medal_layout.addLayout(medal_info_layout)
        medal_layout.setStretchFactor(medal_info_layout,5)
        medal_layout.setSpacing(5)
        medal_layout.setContentsMargins(5,5,5,5)
        self.setLayout(medal_layout)
        #self.setContentsMargins(0,0,0,0)

class elseWidget(QWidget):
    def __init__(self, info,idx):
        super().__init__()

        else_layout = QVBoxLayout()
        else_info_layout = QHBoxLayout()
        
        else_rank = QLabel(str(idx+1) + "등")
        else_rank.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')

        else_id = QLabel(info[1])
        else_id.setStyleSheet('font:9pt 나눔스퀘어라운드 Regular;')
        else_id.setAlignment(QtCore.Qt.AlignBottom)

        else_point = QLabel(info[0]+'Pt')
        else_point.setStyleSheet('font:8pt 나눔스퀘어라운드 Regular;')

        self.else_aboutMe = QTextBrowser()
        print(info)
        if len(info)>2:
            self.else_aboutMe.setText(info[2])
        self.else_aboutMe.setStyleSheet('font:7pt 나눔스퀘어라운드 Regular;border:0px; background-color:#eef5f6;color:#737373')
        self.else_aboutMe.setMaximumWidth(265)
        self.else_aboutMe.setMaximumHeight(25)
        self.else_aboutMe.setAlignment(QtCore.Qt.AlignBottom)

        
        else_info_layout.addWidget(else_rank)
        else_info_layout.setStretchFactor(else_rank,2)
        else_info_layout.addWidget(else_id)
        else_info_layout.setStretchFactor(else_id,7)
        else_info_layout.addWidget(else_point)
        else_info_layout.setStretchFactor(else_point,2)
        else_info_layout.setSpacing(0)

        else_layout.addLayout(else_info_layout)
        else_layout.addWidget(self.else_aboutMe)
        else_layout.setSpacing(0)
        else_layout.setContentsMargins(5,5,5,5)
        self.setLayout(else_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = LeaderBoard(QApplication.activeWindow())
    form.show()
    exit(app.exec_())