#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   firstWindows_pb.py
@Time    :   2023/04/07 15:17:08
@Author  :   yangff 
@Version :   1.0
@微信公众号:  xdbcb8
'''

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtCore import QCoreApplication

# 退出

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.resize(400, 300)
        self.setWindowTitle("微信公众号：学点编程吧")
        bp = QPushButton("退出", self)  # 新增'退出'按钮
        bp.move(150, 100)  # 按钮在窗体的位置
        bp.clicked.connect(QCoreApplication.instance().quit)  # 点击按钮后就会退出窗体
        self.show()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = Example()
   sys.exit(app.exec())