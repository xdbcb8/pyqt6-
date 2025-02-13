#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   abstractspinbox.py
@Time    :   2023/06/30 19:32:55
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# QAbstractSpinBox举例

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QSpinBox, QAbstractSpinBox, QStyleFactory

class myWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QAbstractSpinBox属性方法举例")
        self.resize(400, 50)
        spbox = QSpinBox(self)
        spbox.move(100, 10)
        spbox.setRange(0, 100)
        spbox.setSingleStep(10)
        # ##############按钮样式###############
        # spbox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        spbox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        # spbox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        # print(QStyleFactory.keys()) # 查看当前的操作系统样式

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyle("windowsvista")
    # app.setStyle("windows")
    app.setStyle("Fusion")
    widget = myWindow()
    sys.exit(app.exec())
