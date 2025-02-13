#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   simplepasswd.py
@Time    :   2023/05/05 17:32:52
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 自定义参数内置信号与槽的使用：lambda函数

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMessageBox

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.passwd = ""  # 得到的密码
        self.correctPwd = "321" # 正确的密码
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.setWindowTitle("自定义参数内置信号与槽的使用")
        pb1 = QPushButton("1", self)
        pb2 = QPushButton("2", self)
        pb3 = QPushButton("3", self)
        pb1.move(150, 100)
        pb2.move(150, 150)
        pb3.move(150, 200)
        self.label = QLabel(self)  # 用于显示密码
        self.label.setGeometry(100, 50, 300, 50)
        self.show()

        pb1.clicked.connect(lambda:self.getPwd("1"))
        pb2.clicked.connect(lambda:self.getPwd("2"))
        pb3.clicked.connect(lambda:self.getPwd("3"))

    def getPwd(self, pwd):
        """
        显示密码
        """
        self.passwd += pwd
        self.label.setText(f"当前密码：{self.passwd}")
        if self.passwd == self.correctPwd:
            QMessageBox.information(self, "提示", "密码正确！")
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.RightButton:
            self.label.clear()  # 单击鼠标右键清除
            self.passwd = ""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())
