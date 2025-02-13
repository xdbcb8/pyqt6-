#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   statusbarmenu.py
@Time    :   2023/04/21 19:43:45
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 状态栏

import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QAction

class statusBarMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        self.resize(400, 300)
        self.setWindowTitle("状态栏")
        menu = self.menuBar().addMenu("文件(&F)")
        menu.addAction(QAction("打开(&O)", self))
        menu.addAction(QAction("新建...(&N)", self))
        menu.addAction(QAction("退出(&E)", self))
        self.menuBar().addMenu("设置(&S)")
        self.menuBar().addMenu("关于(&A)")
        self.statusBar().showMessage("我就是状态栏")
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = statusBarMenu()
    sys.exit(app.exec())
