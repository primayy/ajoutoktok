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
        alarm_groupbox.setMinimumSize(300,300)


        #강의 목록 그리기
        setting_label = QLabel('개인 설정')
        setting_label.setStyleSheet("font: 16pt 나눔스퀘어라운드 Regular;background:#eef5f6;color:#42808a")
        #horizon_line = QLabel('─────────────────────')
            #구분선
        horizon_line = QLabel()
        horizon_img = QPixmap('./ui/afterlogin_ui/horizon_line.png')
        horizon_img = horizon_img.scaled(310,12,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        horizon_line.setPixmap(horizon_img)
        horizon_line.setAlignment(Qt.AlignTop)

        alarm_widget_label = QLabel('알림 위젯')

        alarm_sound_label = QLabel('소리 기능')
        alarm_sound_label.setAlignment(Qt.AlignLeft)

        # 위젯 on/off 버튼
        self.widget_on_off_button = QPushButton()
        self.widget_on_off_button.setMinimumHeight(50)
        self.widget_on_off_button.setMinimumWidth(50)
        self.widget_on_off_button.setFocusPolicy(Qt.NoFocus)
        self.widget_on_off_button.setStyleSheet('''
                                QPushButton{image:url(./icon/alarm_on.png); border:0px; width:50px; height:50px;}
                                ''')
        self.widget_on_off_button_status = True
        self.widget_on_off_button.clicked.connect(self.widget_button_toggle)

        # 소리 on/off 버튼
        self.sound_on_off_button = QPushButton()
        self.sound_on_off_button.setMinimumHeight(50)
        self.sound_on_off_button.setMinimumWidth(50)
        self.sound_on_off_button.setFocusPolicy(Qt.NoFocus)
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