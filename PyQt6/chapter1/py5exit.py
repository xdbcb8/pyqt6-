#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   py5exit.py
@Time    :   2023/3/23 11:02:42
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, qApp

# PyQt5退出

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 200)
        self.setWindowTitle("微信公众号：学点编程吧")
        pb = QPushButton('退出', self)
        pb.move(150, 100)
        pb.clicked.connect(self.exit) # 按下退出按钮后窗口关闭
        self.show()
    
    def exit(self):
       qApp.quit()
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())