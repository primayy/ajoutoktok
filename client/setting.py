import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import profile

class setting(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.title = QHBoxLayout()
        self.line = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.initUi()

    def initUi(self):
        pf = profile.profile(self.parent)

        #로그아웃 버튼
        logoutbtn = QPushButton()
        logoutbtn.setMaximumHeight(32)
        logoutbtn.setMaximumWidth(42)
        logoutbtn.setStyleSheet(''' QPushButton{image:url(./icon/logout.png); border: 0px; width:32px; height:42px}        
                                        QPushButton:hover{background:rgba(0,0,0,0); border:0px}
                                        ''')

        alarm_groupbox = QGroupBox('알림')
        alarm_groupbox.setMinimumSize(300,320)

        setting_label = QLabel('설정')
        setting_label.setAlignment(Qt.AlignLeft)
        setting_label.setStyleSheet('''font-weight: Bold; font-size: 16pt''')

        horizon_line = QLabel('─────────────────────')
        horizon_line.setAlignment(Qt.AlignCenter)

        alarm_widget_label = QLabel('알림 위젯')
        # alarm_widget_label.setAlignment(Qt.AlignLeft)

        alarm_sound_label = QLabel('소리 기능')
        alarm_sound_label.setAlignment(Qt.AlignLeft)

        # 위젯 on/off 버튼
        self.widget_on_off_button = QPushButton()
        self.widget_on_off_button.setMinimumHeight(50)
        self.widget_on_off_button.setMinimumWidth(50)
        self.widget_on_off_button.setStyleSheet('''
                                QPushButton{image:url(./icon/alarm_on.png); border:0px; width:50px; height:50px;}
                                ''')
        self.widget_on_off_button_status = True
        self.widget_on_off_button.clicked.connect(self.widget_button_toggle)

        # 소리 on/off 버튼
        self.sound_on_off_button = QPushButton()
        self.sound_on_off_button.setMinimumHeight(50)
        self.sound_on_off_button.setMinimumWidth(50)
        self.sound_on_off_button.setStyleSheet('''
                                QPushButton{image:url(./icon/alarm_on.png); border:0px; width:50px; height:50px;}
                                ''')
        self.sound_on_off_button.setCheckable(True)
        self.sound_on_off_button_status = True
        self.sound_on_off_button.clicked.connect(self.sound_button_toggle)


        self.title.addWidget(setting_label)
        self.title.addWidget(logoutbtn)

        self.line.addWidget(alarm_widget_label)
        self.line.addWidget(self.widget_on_off_button,alignment=(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop))
        self.line.addWidget(alarm_sound_label)
        self.line.addWidget(self.sound_on_off_button,alignment=(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop))
        self.line.addStretch(1)

        alarm_groupbox.setLayout(self.line)

        self.mainLayout.addLayout(self.title)
        self.mainLayout.addWidget(horizon_line)
        self.mainLayout.addWidget(pf, alignment=QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(alarm_groupbox)
        self.mainLayout.addStretch(1)

    def widget_button_toggle(self):
        if (self.widget_on_off_button_status == True):
            self.widget_on_off_button.setStyleSheet('''
                                QPushButton{image:url(./icon/alarm_off.png); border:0px; width:50px; height:50px;}                        
                                ''')
            self.widget_on_off_button_status = False
        elif (self.widget_on_off_button_status == False):
            self.widget_on_off_button.setStyleSheet('''
                                QPushButton{image:url(./icon/alarm_on.png); border:0px; width:50px; height:50px;}        
                                ''')
            self.widget_on_off_button_status = True

    def sound_button_toggle(self):
        if (self.sound_on_off_button_status == True):
            self.sound_on_off_button.setStyleSheet('''
                                QPushButton{image:url(./icon/alarm_off.png); border:0px; width:50px; height:50px;}                        
                                ''')
            self.sound_on_off_button_status = False
        elif (self.sound_on_off_button_status == False):
            self.sound_on_off_button.setStyleSheet('''
                                QPushButton{image:url(./icon/alarm_on.png); border:0px; width:50px; height:50px;}        
                                ''')
            self.sound_on_off_button_status = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = setting()
    form.show()
    exit(app.exec_())