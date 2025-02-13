#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   eventhandler.py
@Time    :   2023/04/26 18:48:54
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 自定义复选框

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QCheckBox
from PyQt6.QtCore import Qt

class diyCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
    
    def mousePressEvent(self, event):
        """让鼠标右键也能够勾选复选框"""
        if event.button() == Qt.MouseButton.RightButton:
            if self.checkState() == Qt.CheckState.Unchecked:
                self.setChecked(True)
            elif self.checkState() == Qt.CheckState.Checked:
                self.setChecked(False)
            self.setText("单击我的是鼠标右键")
        else:
            super().mousePressEvent(event)
            self.setText("单击我的是鼠标左键")

class myWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        cb = diyCheckBox(self)
        cb.setText("这是一个复选框           ")
        cb.move(180, 140)
        self.setWindowTitle("让鼠标右键也能勾选复选框")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myw = myWidget()
    myw.show()
    sys.exit(app.exec())

