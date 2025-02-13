#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   calendarwidget.py
@Time    :   2023/07/08 10:47:10
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QCalendarWidget简单举例

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QCalendarWidget
from PyQt6.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCalendarWidget举例")
        self.resize(300, 200)
        calendar = QCalendarWidget(self)
        # calendar.setGridVisible(True)
        calendar.setFirstDayOfWeek(Qt.DayOfWeek.Sunday)
        # calendar.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames)
        # calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())