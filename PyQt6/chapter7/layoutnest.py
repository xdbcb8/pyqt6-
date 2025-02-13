#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   layoutnest.py
@Time    :   2023/06/13 09:57:14
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 嵌套布局

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QStackedLayout, QLabel, QVBoxLayout, QComboBox
from PyQt6.QtGui import QPixmap

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("嵌套布局")
        self.resize(300, 200)

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

        # 创建下拉框，有三个选项
        combox = QComboBox(self)
        items = ["第一幅", "第二幅", "第三幅"]
        combox.addItems(items)
        combox.activated.connect(self.nextPage)

        # 创建QStackedLayout，并将标签添加到其中
        self.stackLayout = QStackedLayout()
        self.stackLayout.addWidget(label1)
        self.stackLayout.addWidget(label2)
        self.stackLayout.addWidget(label3)

        # 将QVBoxLayout设置为主窗体的布局
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(combox)
        mainLayout.addLayout(self.stackLayout)
        self.setLayout(mainLayout)
        self.show()

    def nextPage(self, index):
        """下拉框筛选画面"""
        self.stackLayout.setCurrentIndex(index) # 设置当前展示的画面

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())