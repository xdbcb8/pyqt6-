#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   datetimeedit.py
@Time    :   2023/07/07 21:03:32
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QDateTimeEdit举例：多种类型的日期和时间

import sys
from PyQt6.QtCore import QLocale
from PyQt6.QtWidgets import QDateTimeEdit, QDateEdit, QTimeEdit, QDialog, QApplication, QFormLayout

class MyWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.setWindowTitle("DateTimeEdit综合举例")

        # 日期时间选择
        dateTimeEdit = QDateTimeEdit(self)
        dateTimeEditPOP = QDateTimeEdit(self)
        dateTimeEditPOP.setCalendarPopup(True) # 日历选择
        # 日期选择
        dateEdit = QDateEdit(self)
        dateEditZH = QDateEdit(self)
        dateEditZH.setDisplayFormat("yyyy-MMM-ddd")
        locale = QLocale(QLocale.Language.English) # 英文样式
        dateEditE = QDateEdit(self)
        dateEditE.setLocale(locale)
        dateEditE.setDisplayFormat("yyyy-MMM-ddd")
        # 时间选择
        time = QTimeEdit(self)
        timeA = QTimeEdit(self)
        timeA.setDisplayFormat("hh:mm:ssA")
        # 布局
        layout = QFormLayout(self)
        layout.addRow("普通日期时间选择", dateTimeEdit)
        layout.addRow("日历日期时间选择", dateTimeEditPOP)
        layout.addRow("普通日期选择", dateEdit)
        layout.addRow("中文日期选择", dateEditZH)
        layout.addRow("英文日期选择", dateEditE)
        layout.addRow("普通时间选择", time)
        layout.addRow("上/下午时间选择", timeA)
        self.setLayout(layout)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywidget = MyWidget()
    sys.exit(app.exec())