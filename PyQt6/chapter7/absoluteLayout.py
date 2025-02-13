#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   absoluteLayout.py
@Time    :   2023/05/29 18:45:15
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 绝对位置

import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.setWindowTitle("绝对位置")

        bt1 = QPushButton("剪刀",self)
        bt1.move(50,250)

        bt2 = QPushButton("石头",self)
        bt2.move(150,250)

        bt3 = QPushButton("布",self)
        bt3.move(250,250)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exit(app.exec())