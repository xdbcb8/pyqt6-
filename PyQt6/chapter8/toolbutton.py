#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   toolbutton.py
@Time    :   2023/06/22 10:36:01
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QToolButton类简单举例

import sys
import os
from PyQt6.QtWidgets import QToolButton, QApplication, QWidget, QLabel, QVBoxLayout, QMenu
from PyQt6.QtGui import QIcon, QAction, QKeySequence
from PyQt6.QtCore import Qt

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.show()
        self.resize(100, 50)

        button = QToolButton(self)
        # button.setIcon(QIcon(f"{current_dir}\\toolbtnicon.png"))
        # button.setAutoRaise(True) # 是否自动上浮
        button.setText("工具按钮")

        # ###################工具按钮的样式#####################
        # button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonFollowStyle)
        # button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        # button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        # button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        # button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # ##################箭头的样式#########################
        # button.setArrowType(Qt.ArrowType.NoArrow)
        # button.setArrowType(Qt.ArrowType.UpArrow)
        # button.setArrowType(Qt.ArrowType.DownArrow)
        # button.setArrowType(Qt.ArrowType.LeftArrow)
        # button.setArrowType(Qt.ArrowType.RightArrow)

        # ################菜单的样式###########################
        menu = QMenu()
        openAct = QAction("打开(&O)", self)
        openAct.setShortcut(QKeySequence.StandardKey.Open)
        newAct = QAction("新建...(&N)", self)
        newAct.setShortcut(QKeySequence.StandardKey.New)
        menu.addSeparator()
        saveAct = QAction("保存(&S)", self)
        saveAct.setShortcut(QKeySequence.StandardKey.Save)
        saveasAct = QAction("另保存为...(&S)", self)
        saveasAct.setShortcut("Ctrl+Shift+S")
        menu.addSeparator()
        exitAct = QAction("退出(&E)", self)
        exitAct.setShortcut("Ctrl+E")
        menu.addActions([openAct, newAct, saveAct, saveasAct, exitAct])
        button.setMenu(menu)
        # button.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        # button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("ToolButton按钮"))
        layout.addWidget(button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())