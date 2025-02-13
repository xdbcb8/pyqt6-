#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   py5circle.py
@Time    :   2023/3/23 11:02:25
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

# PyQt5 画圆

class Circle(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.resize(320, 240)
        self.setWindowTitle("画圆圈")
        self.show()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.red) # 设置红色笔
        painter.setBrush(Qt.red) # 设置红色画刷
        painter.drawEllipse(100, 50, 100, 100) # 画圆
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    circle = Circle()
    sys.exit(app.exec())