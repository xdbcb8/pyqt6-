#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   diysignalNopar.py
@Time    :   2023/05/08 15:45:38
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

# 无参数自定义信号与槽函数的使用

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, QObject

class MyCustomSignal(QObject):
    diy_signal = pyqtSignal()  # 定义一个自定义信号

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.setWindowTitle("自定义无参数信号")

        btn = QPushButton("发射自定义信号", self)
        btn.move(100, 50)
        btn.clicked.connect(self.btn_click)

        self.label = QLabel(self)  # 创建一个QLabel控件，用于显示信号
        self.label.setGeometry(100, 100, 100, 100)

        # 实例化一个自定义信号
        self.my_custom_signal = MyCustomSignal()
        # 将自定义信号连接到QLabel控件的槽方法中
        self.my_custom_signal.diy_signal.connect(self.show_signal)
        self.show()

    def btn_click(self):
        """发送自定义信号"""
        self.my_custom_signal.diy_signal.emit()

    def show_signal(self):
        """在QLabel控件中显示自定义信号"""
        self.label.setText("收到自定义信号!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())