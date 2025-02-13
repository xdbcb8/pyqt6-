#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   simple.py
@Time    :   2023/05/05 09:57:38
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 默认参数内置信号与槽的使用

import sys
from PyQt6.QtWidgets import QApplication, QProgressBar, QSlider, QWidget
from PyQt6.QtCore import Qt

class SimpleEx(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.resize(400, 300)
        self.setWindowTitle("信号与槽简单示例")
        self.bar = QProgressBar(self)
        self.bar.setGeometry(80, 50, 300, 20)
        slider = QSlider(self)
        slider.setMaximum(100)  # 水平滑块最大值设定为100
        slider.setOrientation(Qt.Orientation.Horizontal)  # 水平方向
        slider.move(100, 100)
        self.show()
        slider.valueChanged.connect(self.setProgress)  # 与进度条联动

    def setProgress(self, v):
        self.bar.setValue(v)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SimpleEx()
    sys.exit(app.exec())