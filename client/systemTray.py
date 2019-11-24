import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent

        #트레이 메뉴
        trayIconMenu = QMenu()

        trayOpen = QAction("열기",self)
        trayOpen.triggered.connect(self.parent.show)

        trayLogout = QAction("로그아웃",self)


        trayQuit = QAction("종료",self)
        trayQuit.triggered.connect(self.parent.quitClicked)

        #트레이에 메뉴 추가
        trayIconMenu.addAction(trayOpen)
        trayIconMenu.addAction(trayLogout)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(trayQuit)


        #트레이 기본 설정
        self.setIcon(QIcon('./icon/add.png'))
        self.setToolTip('아주똑똑')

        self.setContextMenu(trayIconMenu)

        self.activated.connect(self.iconActivated)
        self.show()

    def iconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.parent.show()