#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dockwidget.py
@Time    :   2023/08/06 19:31:26
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

# 第11章第5节QMdiArea多窗体收纳

import sys
import os
from PyQt6.QtWidgets import QDockWidget, QPushButton, QApplication, QMainWindow, QTextEdit, QLabel
from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QPixmap

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDockWidget举例")
        self.resize(350, 230)
        QDir.addSearchPath("res", f"{current_dir}\images")
        dockLeft = QDockWidget("左边", self)
        dockRight = QDockWidget("右边", self)

        pic = QLabel(self)
        pic.setPixmap(QPixmap("res:2.png"))
        pic.setScaledContents(True)

        button = QPushButton("点这里")
        dockLeft.setWidget(pic)
        dockRight.setWidget(button)  # 新建一个按钮放在QDockWidget对象上
        dockLeft.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable) # 扑克牌无法关闭

        dockRight.setFloating(True) # 需要QDockWidget就是浮动的，而不是我们把它拉出来，可以这样设置

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit) # 新建一个QTextEdit小部件设置为主窗口的中央控件

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dockRight) # 将给定的dockwidget添加到指定的区域，右侧
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dockLeft) # 将给定的dockwidget添加到指定的区域，左侧
        button.clicked.connect(self.showme)
        self.show()

    def showme(self):
        '''
        点击按钮触发
        '''
        self.textEdit.append("点啦！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())