#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   diysignalPar.py
@Time    :   2023/05/08 15:46:01
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

# 带参数自定义信号与槽函数的使用

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout
from PyQt6.QtCore import pyqtSignal, QObject

class MyCustomSignal(QObject):
    diy_signal_int = pyqtSignal(int)  # 定义一个int信号
    diy_signal_str = pyqtSignal(str)  # 定义一个str信号
    diy_signal_int_str = pyqtSignal(int, str)  # 定义一个int,str信号，一次传递两个参数
    diy_signal_int_str2 = pyqtSignal([int], [str])  # 定义一个重载信号，信号名称一致，但是可以传递两种类型[int],[str]

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.setWindowTitle("自定义有参数信号")
        layout = QGridLayout(self)  #栅格布局
        bt_int = QPushButton("int传递", self)
        bt_str = QPushButton("str传递", self)
        bt_int_str = QPushButton("int,str双参数传递", self)
        bt_int_str2_int = QPushButton("重载信号中的int传递", self)
        bt_int_str2_str = QPushButton("重载信号中的的str传递", self)
        self.label = QLabel(self)  # 创建一个QLabel控件，用于显示信号

        layout.addWidget(bt_int, 0, 0)
        layout.addWidget(bt_str, 0, 1)
        layout.addWidget(bt_int_str, 1, 0)
        layout.addWidget(bt_int_str2_int, 2, 0)
        layout.addWidget(bt_int_str2_str, 2, 1)
        layout.addWidget(self.label, 3, 0, 1, 2)
        self.setLayout(layout)

        bt_int.clicked.connect(lambda: self.btn_click(0))
        bt_str.clicked.connect(lambda: self.btn_click(1))
        bt_int_str.clicked.connect(lambda: self.btn_click(2))
        bt_int_str2_int.clicked.connect(lambda: self.btn_click(3))
        bt_int_str2_str.clicked.connect(lambda: self.btn_click(4))
        # 发出最后两个信号时，可以看到其名称是一样的，但是携带的参数类型不一致。这就是重载信号的妙用。

        # 实例化自定义信号
        self.my_custom_signal = MyCustomSignal()
        # 将自定义信号连接到QLabel控件的槽函数中
        self.my_custom_signal.diy_signal_int.connect(self.show_signal)
        self.my_custom_signal.diy_signal_str.connect(self.show_signal)
        self.my_custom_signal.diy_signal_int_str.connect(self.show_signal_2)
        self.my_custom_signal.diy_signal_int_str2[int].connect(self.show_signal)
        self.my_custom_signal.diy_signal_int_str2[str].connect(self.show_signal)
        self.show()

    def btn_click(self, p):
        """发送自定义信号"""
        if p == 0:
            self.my_custom_signal.diy_signal_int.emit(10)
        elif p == 1:
            self.my_custom_signal.diy_signal_str.emit("示例字符串")
        elif p == 2:
            self.my_custom_signal.diy_signal_int_str.emit(100, "示例字符串2")
        elif p == 3:
            self.my_custom_signal.diy_signal_int_str2[int].emit(1000)
        elif p == 4:
            self.my_custom_signal.diy_signal_int_str2[str].emit("示例字符串3")

    def show_signal(self, p):
        """在QLabel控件中显示自定义信号"""
        self.label.setText(f"收到自定义信号，参数：{p}，类型：{type(p)}")

    def show_signal_2(self, p1, p2):
        """在QLabel控件中显示自定义信号"""
        self.label.setText(f"收到自定义信号，参数：{p1}，{p2}，\n类型：{type(p1)}，{type(p2)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())