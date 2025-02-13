#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   lcdnumber.py
@Time    :   2023/07/09 15:15:36
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QLCDNumber简单举例

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QLCDNumber, QVBoxLayout

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLCDNumber举例")
        lcd1 = QLCDNumber()
        lcd2 = QLCDNumber()
        lcd3 = QLCDNumber()
        lcd1.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        lcd2.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        lcd3.setSegmentStyle(QLCDNumber.SegmentStyle.Outline)
        vlayout = QVBoxLayout(self)
        vlayout.addWidget(lcd1)
        vlayout.addWidget(lcd2)
        vlayout.addWidget(lcd3)
        self.setLayout(vlayout)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())