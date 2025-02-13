#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pushbutton4.py
@Time    :   2023/06/22 07:03:39
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QPushButton举例：互斥开关按钮

import sys
from PyQt6.QtWidgets import QPushButton, QApplication, QWidget, QLabel, QVBoxLayout

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.show()
        self.resize(152, 188)
        self.label = QLabel("    ", self)

        bt1 = QPushButton("1", self)
        bt2 = QPushButton("2", self)
        bt3 = QPushButton("3", self)

        bt1.setCheckable(True)
        bt2.setCheckable(True)
        bt3.setCheckable(True)

        bt1.setAutoExclusive(True)
        bt2.setAutoExclusive(True)
        bt3.setAutoExclusive(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("互斥开关按钮"))
        layout.addWidget(bt1)
        layout.addWidget(bt2)
        layout.addWidget(bt3)
        layout.addWidget(self.label)

        bt1.clicked.connect(self.shownumber)
        bt2.clicked.connect(self.shownumber)
        bt3.clicked.connect(self.shownumber)

    def shownumber(self):
        """
        显示开关上的数字
        """
        number = self.sender().text()
        self.label.setText(number)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())