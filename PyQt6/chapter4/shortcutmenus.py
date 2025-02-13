#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   shortcutmenus.py
@Time    :   2023/04/20 17:27:47
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 菜单：增加图标、快捷键并实现退出功能

import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtCore import QDir

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class CMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        QDir.addSearchPath("icon", f"{current_dir}/menuIcon")
        self.resize(400, 300)
        self.setWindowTitle("创建菜单")
        self.setWindowIcon(QIcon("icon:Title.png"))

        openAct = QAction(QIcon("icon:open.png"), "打开(&O)", self)
        openAct.setShortcut(QKeySequence.StandardKey.Open)
        newAct = QAction(QIcon("icon:new.png"), "新建...(&N)", self)
        newAct.setShortcut(QKeySequence.StandardKey.New)
        saveAct = QAction(QIcon("icon:save.png"), "保存(&S)", self)
        saveAct.setShortcut(QKeySequence.StandardKey.Save)
        saveasAct = QAction(QIcon("icon:saveas.png"), "另保存为...(&S)", self)
        saveasAct.setShortcut("Ctrl+Shift+S")
        exitAct = QAction(QIcon("icon:exit.png"), "退出(&E)", self)
        exitAct.setShortcut("Ctrl+E")
        exitAct.triggered.connect(QApplication.instance().quit)

        menuBar = self.menuBar() # 菜单栏
        fileMenu = menuBar.addMenu("文件(&F)")
        fileMenu.addAction(openAct)
        fileMenu.addSeparator()
        fileMenu.addActions([saveAct, saveasAct])
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)
        menuBar.addMenu("设置(&S)")
        menuBar.addMenu("关于(&A)")

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = CMenu()
    sys.exit(app.exec())
