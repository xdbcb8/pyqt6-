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
# 完整程序位于本书配套资料的PyQt6\chapter4\shortcutmenus.py中

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
        self.resize(400, 300)
        self.setWindowTitle("创建菜单")
        self.setWindowIcon(QIcon("icon:Title.png"))

        QDir.addSearchPath("icon", f"{current_dir}/menuIcon") # 图标目录

        openAct = QAction(QIcon("icon:open.png"), "打开(&O)", self) # 打开
        openAct.setShortcut(QKeySequence.StandardKey.Open) # 打开快捷键

        newAct = QAction(QIcon("icon:new.png"), "新建...(&N)", self) # 新建
        newAct.setShortcut(QKeySequence.StandardKey.New) # 新建快捷键

        saveAct = QAction(QIcon("icon:save.png"), "保存(&S)", self) # 保存
        saveAct.setShortcut(QKeySequence.StandardKey.Save) # 保存快捷键

        saveasAct = QAction(QIcon("icon:saveas.png"), "另保存为...(&S)", self) # 另保存为
        saveasAct.setShortcut("Ctrl+Shift+S") # 另保存为快捷键

        exitAct = QAction(QIcon("icon:exit.png"), "退出(&E)", self) # 退出
        exitAct.setShortcut("Ctrl+E") # 退出快捷键
        exitAct.triggered.connect(QApplication.instance().quit)

        menuBar = self.menuBar() # 菜单栏
        fileMenu = menuBar.addMenu("文件(&F)")
        fileMenu.addAction(newAct) # 新建
        fileMenu.addSeparator()
        fileMenu.addAction(openAct) # 打开
        fileMenu.addSeparator()
        fileMenu.addActions([saveAct, saveasAct]) # 保存、另保存为
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct) # 退出
        menuBar.addMenu("设置(&S)")
        menuBar.addMenu("关于(&A)")

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = CMenu()
    sys.exit(app.exec())
