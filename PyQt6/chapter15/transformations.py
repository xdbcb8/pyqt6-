#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   transformations.py
@Time    :   2023/09/13 10:29:31
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第15章第1节QPainter坐标的操作

import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QFont

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.setWindowTitle('旋转、缩放和平移示例')
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(QFont("Arial", 20))
        # painter.rotate(30) # 旋转
        # painter.scale(2, 2) # 放大
        # painter.translate(100, 100) # 平移坐标系
        painter.shear(0.5, 0.5) # 围绕原点扭转坐标系
        painter.drawText(QPoint(80, 70), "我爱PyQt") # 写字

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())