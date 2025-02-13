#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   diyWidget.py
@Time    :   2023/04/17 19:07:47
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 六角星窗体

import sys
import os
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class DIYWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        界面初始化
        """
        pixmap = QPixmap(f"{current_dir}\\six.png")
        self.resize(pixmap.size())
        self.setMask(pixmap.mask())  # 设置蒙版
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 清除六角星毛边

    def mousePressEvent(self, event):
        """
        鼠标按下事件
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPosition = event.globalPosition().toPoint() - self.frameGeometry().topLeft() 
            # 记录鼠标全局坐标与窗体左上坐标的差值
        elif event.button() == Qt.MouseButton.RightButton: 
            self.close() # 单击右键关闭窗体

    def mouseMoveEvent(self, event):
        """
        鼠标移动事件
        """
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.dragPosition) # 通过换算得到窗体左上角的坐标
 
    def paintEvent(self, event):
        """
        绘图事件
        """
        p = QPainter(self)
        p.drawPixmap(0, 0, QPixmap(f"{current_dir}\\six.png")) # 在窗体原点绘制六角星

if __name__ == "__main__":
    app =QApplication(sys.argv)
    diy = DIYWidget()
    diy.show()
    sys.exit(app.exec())