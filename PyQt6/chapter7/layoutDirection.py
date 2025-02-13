#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spacing.py
@Time    :   2023/06/08 10:55:42
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 箱式布局

import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication,  QBoxLayout

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("创建布局时指定方向")
        self.resize(700, 100)
        bt1 = QPushButton("1",self)
        bt2 = QPushButton("2",self)
        bt3 = QPushButton("3",self)
        bt4 = QPushButton("4",self)

        layout = QBoxLayout(QBoxLayout.Direction.LeftToRight, self) # 从左到右
        # layout = QBoxLayout(QBoxLayout.Direction.RightToLeft, self) # 从右到左
        # layout = QBoxLayout(QBoxLayout.Direction.TopToBottom, self) # 从上到下
        # layout = QBoxLayout(QBoxLayout.Direction.BottomToTop, self) # 从下到上
        layout.addWidget(bt1)
        layout.addWidget(bt2)
        layout.addWidget(bt3)
        layout.addWidget(bt4)
        self.setLayout(layout) # 设置布局方式

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exit(app.exec())