import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class alarm(QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout=QVBoxLayout()
        self.title = QHBoxLayout()
        group = QLabel('알림')
        horizon_line = QLabel('─────────────────────')
        btn_remove_all = QPushButton('모두 삭제')
        group.setStyleSheet('''
                font-weight:bold;
                font-size:16pt''')
        viewer = QListWidget(self)

        viewer.setMinimumSize(300, 500)
        viewer.setStyleSheet('''
                # QListWidget:item:hover{background:white};
                # QListWidget:item:selected:active{background:white}
                ''')

        item = QListWidgetItem(viewer)
        # custom_widget = lecture_group('add', studid, QApplication.activeWindow())
        # item.setSizeHint(custom_widget.sizeHint())
        # self.viewer.setItemWidget(item, custom_widget)
        viewer.addItem(item)
        self.title.addWidget(group)
        self.title.addWidget(btn_remove_all,alignment=QtCore.Qt.AlignRight)
        self.mainLayout.addLayout(self.title)
        self.mainLayout.addWidget(horizon_line)
        self.mainLayout.addWidget(viewer)
        self.setLayout(self.mainLayout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = alarm()
    form.show()
    exit(app.exec_())