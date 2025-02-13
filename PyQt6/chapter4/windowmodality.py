#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   windowmodality.py
@Time    :   2023/04/23 14:12:11
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 对话框的模态与非模态

import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PyQt6.QtCore import Qt

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
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        # dialog.setWindowModality(Qt.WindowModality.NonModal)
        # dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.show()

class Dialog(QDialog):
    """对话框代码"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Dialog")
        self.resize(200, 100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()