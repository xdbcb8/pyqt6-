#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   contextmenu.py
@Time    :   2023/04/21 13:55:17
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QMenu
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QDir

# 上下文菜单（右键菜单）

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class contextMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        QDir.addSearchPath("icon", f"{current_dir}/menuIcon")
        self.resize(400, 300)
        self.setWindowTitle("上下文菜单")
        self.setWindowIcon(QIcon("icon:Title.png"))
        
        menuBar = self.menuBar()
        menuBar.addMenu("文件(&F)")
        menuBar.addMenu("设置(&S)")
        menuBar.addMenu("关于(&A)")

        self.checkAct = QAction("未勾选", self) # 勾选状态
        self.checkAct.setCheckable(True) # 可勾选

        self.show()

    def contextMenuEvent(self, event):
        """
        上下文菜单
        """
        contextMenu = QMenu(self)
        newAct = QAction(QIcon("icon:new.png"), "新建...", self)
        saveAct = QAction(QIcon("icon:save.png"), "保存", self)
        exitAct = QAction(QIcon("icon:exit.png"), "退出", self)
        contextMenu.addActions([newAct, saveAct, exitAct, self.checkAct])
        # 在鼠标右键点击位置显示上下文菜单并获取用户选择的动作
        # mapToGlobal()将鼠标事件的本地坐标转换为全局屏幕坐标
        # exec()方法显示菜单并阻塞等待用户选择，返回用户选择的动作对象
        action = contextMenu.exec(self.mapToGlobal(event.pos()))
        if action == exitAct:
            QApplication.instance().quit() # 退出
        elif action == self.checkAct:
            if self.checkAct.isChecked():
                self.checkAct.setChecked(True) # 勾选状态改变
                self.checkAct.setText("已勾选")
            else:
                self.checkAct.setChecked(False)
                self.checkAct.setText("未勾选")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = contextMenu()
    sys.exit(app.exec())
