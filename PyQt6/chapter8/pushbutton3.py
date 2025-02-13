#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pushbutton3.py
@Time    :   2023/06/22 07:03:39
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QPushButton举例：开关按钮

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

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("开关按钮"))
        layout.addWidget(bt1)
        layout.addWidget(bt2)
        layout.addWidget(bt3)
        layout.addWidget(self.label)

        self.password = '' # 需要显示的字符串

        bt1.clicked.connect(self.setPassword)
        bt2.clicked.connect(self.setPassword)
        bt3.clicked.connect(self.setPassword)

    def setPassword(self, pressed):
        """
        显示按钮上的数字
        pressed：bool，判断此时按钮是否被按下
        """
        number = self.sender().text() # 按钮上的数字
        if pressed:
            if len(self.password) < 3:  # 窗体上显示的数字长度不能超过3位
                self.password += number
        else:
            self.password = self.password.replace(number, "") # 弹起按钮后该按钮上的数字就会在窗体上消失

        self.label.setText(self.password) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())