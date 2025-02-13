#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   diyspinbox.py
@Time    :   2023/07/02 16:30:48
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 自定义QSpinBox

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QSpinBox, QLabel, QVBoxLayout

class MonthSpinBox(QSpinBox):
    def __init__(self, Parent = None):
        super().__init__(Parent)

    def textFromValue(self, value):
        months = ["一月", "二月", "三月", "四月", "五月", "六月",
                  "七月", "八月", "九月", "十月", "十一月", "十二月"]
        return months[value-1]
    
    def valueFromText(self, text):
        months = ["一月", "二月", "三月", "四月", "M五月", "六月",
                  "七月", "八月", "九月", "十月", "十一月", "十二月"]
        return months.index(text) + 1
    

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(250, 100)
        self.setWindowTitle("自定义整数输入框")
        month = MonthSpinBox(self)
        month.setRange(1, 12)
        month.valueChanged.connect(self.showV)
        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(month)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.show()

    def showV(self, n):
        self.label.setText(f"当前月份返回值：{n}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())