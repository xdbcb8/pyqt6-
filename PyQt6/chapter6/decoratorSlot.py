#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   decoratorSlot.py
@Time    :   2023/05/16 11:03:59
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 装饰器槽

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout
from PyQt6.QtCore import pyqtSlot, QMetaObject

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.resize(400, 300)
        self.setWindowTitle("装饰器槽")
        vlayout = QGridLayout(self)
        line = QLineEdit(self)
        line.setObjectName("lineinput") # 设置输入栏对象名称
        btn1 = QPushButton("按钮1", self)
        btn1.setObjectName("button1") # 设置按钮对象名称
        btn2 = QPushButton("按钮2", self)
        btn2.setObjectName("button2")
        self.label = QLabel(self)
        vlayout.addWidget(line, 0, 0, 1, 3)
        vlayout.addWidget(btn1, 1, 1)
        vlayout.addWidget(btn2, 2, 1)
        vlayout.addWidget(self.label, 3, 0, 3, 1)
        self.setLayout(vlayout)
        self.show()
        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def on_button1_clicked(self): # 按钮1
        self.label.setText("收到 按钮1 的单击信号")

    @pyqtSlot()
    def on_button2_clicked(self): # 按钮2
        self.label.setText("收到 按钮2 的单击信号")

    @pyqtSlot(str) # 输入栏
    def on_lineinput_textChanged(self, text):
        self.label.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())
