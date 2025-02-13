#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   passwd.py
@Time    :   2023/05/05 17:33:08
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 多控件内置信号与槽的使用

import sys
from PyQt6.QtCore import QSignalMapper
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QMessageBox

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.passwd = ""  # 得到的密码
        self.correctPwd = "321"  # 正确的密码
        self.initUI()

    def initUI(self):
        self.setWindowTitle("多控件的信号与槽连接")

        layout = QGridLayout()
        self.label = QLabel(self) 
        layout.addWidget(self.label, 0, 0, 1, 3)

        signal_mapper = QSignalMapper(self)  # 信号映射

        for i in range(12):
            button = QPushButton(f"{i}")
            layout.addWidget(button, (i//3)+1, i%3)
            signal_mapper.setMapping(button, i) # 将每一个按钮与索引像对应
            button.clicked.connect(signal_mapper.map)
            if i == 10:
                button.setText("Backward")
            elif i == 11:
                button.setText("Clear")
        self.setLayout(layout)

        signal_mapper.mappedInt.connect(self.getPwd)

    def getPwd(self, index):
        """
        显示密码
        """
        if 0 <= index <= 9:
            self.passwd += str(index)
            self.label.setText(f"当前密码：{self.passwd}")
            if self.passwd == self.correctPwd:
                QMessageBox.information(self, "提示", "密码正确！")
        elif index == 10:
            self.passwd = self.passwd[0:-1]
            self.label.setText(f"当前密码：{self.passwd}")
        elif index == 11:
            self.label.clear()  # 密码全部清除
            self.passwd = ""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
