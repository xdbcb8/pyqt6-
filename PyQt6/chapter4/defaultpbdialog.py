#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   defaultpbdialog.py
@Time    :   2023/04/23 14:12:18
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 默认按钮

import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMainWindow")
        self.resize(400, 300)
        self.button = QPushButton("开一个对话框", self)
        self.button.move(50, 50)
        self.show()
        self.button.clicked.connect(self.open_dialog)

    def open_dialog(self):
        """打开对话框"""
        dialog = Dialog(self)
        dialog.exec()

class Dialog(QDialog):
    """对话框代码"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Dialog")
        self.resize(200, 100)
        pb = QPushButton("关闭", self)
        pb.move(50, 50)
        pb.setDefault(True) # 默认按钮
        pb.clicked.connect(lambda :self.close()) # 关闭对话框

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()