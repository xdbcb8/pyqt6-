#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   py6circle.py
@Time    :   2023/3/23 11:03:07
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter

# PyQt6 画圆

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
        painter.setPen(Qt.GlobalColor.red) # 设置红色笔
        painter.setBrush(Qt.GlobalColor.red) # 设置红色画刷
        painter.drawEllipse(100, 50, 100, 100) # 画圆
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    circle = Circle()
    sys.exit(app.exec())