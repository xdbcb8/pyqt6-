#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spacing.py
@Time    :   2023/06/08 10:55:42
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 创建一个空白间隔

import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication,  QHBoxLayout

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("空白空间")
        self.resize(700, 100)
        bt1 = QPushButton("1",self)
        bt2 = QPushButton("2",self)
        bt3 = QPushButton("3",self)
        bt4 = QPushButton("4",self)

        layout = QHBoxLayout(self)
        layout.addWidget(bt1) # 增加一个按钮
        layout.addSpacing(20) # 增加间隔距离为20像素
        layout.addWidget(bt2)
        layout.addSpacing(40) # 增加间隔距离为40像素
        layout.addWidget(bt3)
        layout.addSpacing(80) # 增加间隔距离为80像素
        layout.addWidget(bt4)
        self.setLayout(layout)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exit(app.exec())