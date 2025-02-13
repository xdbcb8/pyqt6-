#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stackedlayout.py
@Time    :   2023/06/12 18:16:03
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 堆栈布局

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QStackedLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.currentPage = 0 # 当前展示的索引
        self.initUI()

    def initUI(self):
        self.setWindowTitle("堆栈布局")
        self.resize(400, 200)

        # 三个标签加载图片
        label1 = QLabel(self)
        label1.setPixmap(QPixmap(f"{current_dir}\\1.png")) # 加载图片1
        label1.setScaledContents(True)  # 设置图片将会按比例缩小或放大以适应 QLabel 的大小
        label2 = QLabel(self)
        label2.setPixmap(QPixmap(f"{current_dir}\\2.png"))
        label2.setScaledContents(True)
        label3 = QLabel(self)
        label3.setPixmap(QPixmap(f"{current_dir}\\3.png"))
        label3.setScaledContents(True)

        # 设置一个定时器，每隔一秒调用一次nextPage槽
        timer = QTimer(self)
        timer.timeout.connect(self.nextPage)
        timer.start(1000)

        # 创建QStackedLayout，并将标签添加到其中
        self.stackLayout = QStackedLayout(self)
        self.stackLayout.addWidget(label1)
        self.stackLayout.addWidget(label2)
        self.stackLayout.addWidget(label3)

        # 将QStackedLayout设置为主窗口的布局
        self.setLayout(self.stackLayout)
        self.show()

    def nextPage(self):
        """每隔一秒切换一次画面"""
        self.stackLayout.setCurrentIndex(self.currentPage) # 设置当前展示的画面
        if self.currentPage == 2:
            self.currentPage = 0
        else:
            self.currentPage += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())