#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mousedraw.py
@Time    :   2023/04/29 07:04:46
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 涂鸦板

import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt

class drawingTablet(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.paths = [[]]  # 可以记录多组线段坐标
        self.setWindowTitle("涂鸦板")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.red, 2))  # 红色，线宽：2像素
        for path in self.paths:
            for i in range(len(path)-1):
                painter.drawLine(path[i], path[i + 1])

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.paths[-1].append(event.pos())  # 记录最近一次划线的坐标
        elif event.buttons() == Qt.MouseButton.RightButton:
            self.paths.clear()  # 按鼠标右键清除绘画
        self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.paths[-1].append(event.pos()) # 记录最近一次划线的坐标
            self.update()

    def mouseReleaseEvent(self, event):
        self.paths.append([]) # 释放鼠标按键意味着新的绘画开始，所以要新增记录坐标的列表，默认为空列表

if __name__ == "__main__":   
    app = QApplication(sys.argv)
    drawing = drawingTablet()
    drawing.show()
    sys.exit(app.exec())