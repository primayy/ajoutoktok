import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication

class calendarWidget(QDialog) :
    def __init__(self,parent, type) :
        super().__init__()
        self.parent = parent
        self.type = type
        self.mainLayout = QHBoxLayout()

        #달력 위젯
        self.calendar = QCalendarWidget()

        self.calendar.clicked.connect(self.calendarClicked)


        self.mainLayout.addWidget(self.calendar)
        self.setLayout(self.mainLayout)
        self.show()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def calendarClicked(self):
        if self.type == 'start':
            self.parent.btnStart.setText(self.calendar.selectedDate().toString("yyyy-MM-dd"))
        else:
            self.parent.btnFinish.setText(self.calendar.selectedDate().toString("yyyy-MM-dd"))
        self.close()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = calendarWidget()
    myWindow.show()
    app.exec_()