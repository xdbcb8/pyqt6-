#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dynamiclayout2.py
@Time    :   2023/4/27 16:25:45
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 这是另一种动态布局方式，代码供参考。

import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton

class MyDialog(QDialog):
    """
    实现更多控件的显示，实现动态布局
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Dialog")
        self.setFixedSize(300, 150)

        # 创建控件
        self.label1 = QLabel("姓名：")
        self.line_edit1 = QLineEdit()
        self.label2 = QLabel("性别：")
        self.combo_box1 = QComboBox()
        self.combo_box1.addItems(["男", "女"])
        self.more_button = QPushButton("更多")
        self.label3 = QLabel("年龄：")
        self.line_edit2 = QLineEdit()

        # 创建布局
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.line_edit1)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.combo_box1)
        layout2.addWidget(self.more_button)

        layout3 = QHBoxLayout()
        layout3.addWidget(self.label3)
        layout3.addWidget(self.line_edit2)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addLayout(layout3)

        # 连接信号槽
        self.more_button.clicked.connect(self.show_more_controls)

        self.setLayout(main_layout)

        self.show()

    def show_more_controls(self):
        """
        显示更多控件
        """
        self.label4 = QLabel("地址：")
        self.line_edit3 = QLineEdit()
        self.label5 = QLabel("电话：")
        self.line_edit4 = QLineEdit()

        layout4 = QHBoxLayout()
        layout4.addWidget(self.label4)
        layout4.addWidget(self.line_edit3)

        layout5 = QHBoxLayout()
        layout5.addWidget(self.label5)
        layout5.addWidget(self.line_edit4)

        self.layout().addLayout(layout4)
        self.layout().addLayout(layout5)
        self.more_button.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = MyDialog()
    app.exec()