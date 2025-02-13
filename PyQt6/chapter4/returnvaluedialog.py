#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   returnvaluedialog.py
@Time    :   2023/04/23 14:43:13
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 对话框返回值

import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMainWindow")
        self.resize(400, 300)
        self.button = QPushButton("打开一个对话框", self)
        self.button.move(50, 50)
        self.lb = QLabel(self)
        self.lb.move(100, 100)
        self.show()
        self.button.clicked.connect(self.open_dialog)

    def open_dialog(self):
        """打开对话框"""
        dialog = Dialog(self)
        result = dialog.exec()
        if result == dialog.DialogCode.Accepted:
        # if result == 1: # DialogCode.Accepted也能用1表示
            self.lb.setText("单击了“确定”按钮") # 显示单击了“确定”按钮
        elif result == dialog.DialogCode.Rejected:
        # elif result == 0: # DialogCode.Rejected也能用0表示
            self.lb.setText("单击了“取消”按钮") # 显示单击了“取消”按钮

class Dialog(QDialog):
    """对话框代码"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Dialog")
        self.resize(200, 100)
        pbok = QPushButton("确定", self)
        pbok.move(20, 50)
        pbok.clicked.connect(lambda :self.accept())
        pbCancel = QPushButton("取消", self)
        pbCancel.move(100, 50)
        pbCancel.clicked.connect(lambda :self.reject())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()