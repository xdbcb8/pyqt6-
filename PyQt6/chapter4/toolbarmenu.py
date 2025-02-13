#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   toolbarmenu.py
@Time    :   2023/04/21 18:38:21
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 工具栏

import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtCore import QDir, Qt

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class toolBarMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        QDir.addSearchPath("icon", f"{current_dir}/menuIcon")
        self.resize(400, 300)
        self.setWindowTitle("工具栏")
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

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("文件(&F)")
        fileMenu.addAction(openAct)
        fileMenu.addSeparator()
        fileMenu.addActions([saveAct, saveasAct])
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)
        menuBar.addMenu("设置(&S)")
        menuBar.addMenu("关于(&A)")

        toolbar = self.addToolBar("工具栏")
        # toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon) # 文字在图标下方
        # toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)  # 只有文字
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)  # 文字在图标旁边
        toolbar.addAction(newAct)
        toolbar.addAction(openAct)
        toolbar.addAction(saveAct)

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = toolBarMenu()
    sys.exit(app.exec())
