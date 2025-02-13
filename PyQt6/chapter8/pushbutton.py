#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pushbutton.py
@Time    :   2023/06/18 17:13:51
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QPushButton举例：菜单

import os
import sys
from PyQt6.QtWidgets import QPushButton, QApplication, QMenu, QWidget
from PyQt6.QtGui import QIcon

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.setWindowTitle("普通按钮")
        button1 = QPushButton(self)
        button1.move(100, 50)
        button1.setText("第一个按钮")
        # button1.setIcon(QIcon(f"{current_dir}\\Buttonicon.png"))
        button2 = QPushButton(self)
        button2.move(100,100)
        button2.setText("第二个按钮")
        button2.setFlat(True)
        # menu = QMenu()
        # menu.addAction("第一个菜单")
        # menu.addSeparator()
        # menu.addAction("第二个菜单")
        # menu.addSeparator()
        # menu.addAction("第三个菜单")
        # button1.setMenu(menu)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())