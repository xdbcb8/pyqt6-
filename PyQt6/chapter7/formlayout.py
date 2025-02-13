#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   formlayout.py
@Time    :   2023/06/12 06:22:50
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

# 表单布局

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QFormLayout, QLabel, QLineEdit, QTextEdit, QGridLayout
                             
class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(300, 200)
        self.setWindowTitle("表单布局")
        nameLineEdit = QLineEdit("")
        addLineEdit = QLineEdit("")
        introductionLineEdit = QTextEdit("")

        # 表单布局方式
        formlayout = QFormLayout(self)
        formlayout.addRow("姓名(&N)", nameLineEdit)
        formlayout.addRow("电话(&T)", addLineEdit)
        formlayout.addRow("简介(&I)", introductionLineEdit)
        self.setLayout(formlayout)

        #  网格布局方式
        # gridlayout = QGridLayout(self)
        # nameLabel = QLabel("姓名(&N)")
        # addLabel = QLabel("电话(&T)")
        # introductionLabel = QLabel("简介(&I)")
        # nameLabel.setBuddy(nameLineEdit)  # 编辑伙伴，即将标签和具体的控件相连接
        # addLabel.setBuddy(addLineEdit)
        # introductionLabel.setBuddy(introductionLineEdit)
        # gridlayout.addWidget(nameLabel, 0, 0)
        # gridlayout.addWidget(nameLineEdit, 0, 1)
        # gridlayout.addWidget(addLabel, 1, 0)
        # gridlayout.addWidget(addLineEdit, 1, 1)
        # gridlayout.addWidget(introductionLabel, 2, 0)
        # gridlayout.addWidget(introductionLineEdit, 2, 1)
        # self.setLayout(gridlayout)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exit(app.exec())