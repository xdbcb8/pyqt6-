#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   fontdialog.py
@Time    :   2023/07/12 21:08:34
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第9章第4节QFontDialog

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QFontDialog, QLabel, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QFont


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QFontDialog举例")
        self.resize(300, 200)
        self.label = QLabel("微信公众号：学点编程吧", self)
        button = QPushButton("选择字体", self)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        hlayout = QHBoxLayout(self)
        hlayout.addWidget(self.label)
        hlayout.addWidget(button)
        self.setLayout(hlayout)
        button.clicked.connect(self.selectFont)
        self.show()

    def selectFont(self):
        """
        选择字体
        """
        font, isok = QFontDialog.getFont()
        if isok:
            self.label.setFont(font)

        # font, isok = QFontDialog.getFont(QFont("黑体", 20), self, caption="选择字体abc")
        # self.label.setFont(font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())