#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   py6.py
@Time    :   2023/3/23 11:02:57
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import QRect

# 创建一个GUI程序
app = QApplication(sys.argv)

# 创建一个窗体
firstwindow = QWidget()
firstwindow.resize(320, 240)
firstwindow.setWindowTitle("微信公众号：学点编程吧")

# 创建一个标签并显示在窗体上
mylabel = QLabel(firstwindow)
mylabel.setText("第 一 个 PyQt 6 窗体!")
mylabel.setGeometry(QRect(100, 50, 150, 100))

firstwindow.show()

sys.exit(app.exec())