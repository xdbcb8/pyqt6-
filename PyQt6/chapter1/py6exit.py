#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   py6exit.py
@Time    :   2023/3/23 11:03:18
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton#, qApp
from PyQt6.QtCore import QCoreApplication

# 退出

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 200)
        self.setWindowTitle("微信公众号：学点编程吧")
        pb = QPushButton('退出', self)
        pb.move(150, 100)
        pb.clicked.connect(self.exit)
        self.show()
    
    def exit(self):
       QCoreApplication.instance().quit()
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())