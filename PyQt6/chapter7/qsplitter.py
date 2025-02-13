#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   qsplitter.py
@Time    :   2023/06/13 14:40:48
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 分裂器

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QSplitter, QComboBox, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

class MyWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("QSplitter——分裂器")
        self.resize(300, 200)

        vbox = QVBoxLayout(self)

        # 创建一个分裂器并加入到垂直布局当中
        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Vertical) # 垂直分隔
        vbox.addWidget(splitter)

        up = QComboBox(splitter)
        up.addItems(["one", "two", "three"])
        up.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding) # 水平方向Preferred，垂直方向Expanding（可以调整高度）
        down = QTextEdit(splitter)

        # 分裂器增加up和down两个控件
        splitter.addWidget(up)
        splitter.addWidget(down)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())
