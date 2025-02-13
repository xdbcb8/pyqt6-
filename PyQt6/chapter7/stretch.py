#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stretch.py
@Time    :   2023/06/08 10:34:39
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 可拉伸的空白间隔

import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication,  QHBoxLayout

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("拉伸系数")
        self.resize(700, 100)
        bt1 = QPushButton("1",self)
        bt2 = QPushButton("2",self)
        bt3 = QPushButton("3",self)
        bt4 = QPushButton("4",self)

        layout = QHBoxLayout(self)
        layout.addWidget(bt1) # 增加一个按钮
        layout.addStretch(1) # 增加拉伸系数
        layout.addWidget(bt2)
        layout.addStretch(2) # 增加拉伸系数
        layout.addWidget(bt3)
        layout.addStretch(3) # 增加拉伸系数
        layout.addWidget(bt4)
        self.setLayout(layout) # 设置布局方式

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exit(app.exec())