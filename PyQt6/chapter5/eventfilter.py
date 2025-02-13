#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   eventfilter.py
@Time    :   2023/04/26 19:55:33
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 事件过滤器

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QLabel
from PyQt6.QtCore import QEvent

class myWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.edit = QLineEdit(self)
        self.edit.move(150, 140)
        self.edit.installEventFilter(self)
        self.setWindowTitle("输入栏过滤鼠标双击事件")
        self.lable = QLabel(self)
        self.lable.setGeometry(150, 160, 200, 100)

    def eventFilter(self, object, event):
        if object == self.edit:
            if event.type() == QEvent.Type.MouseButtonDblClick:
                self.lable.setText("双击了鼠标，但是无法全选。")
                return True
        return super().eventFilter(object, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myw = myWidget()
    myw.show()
    sys.exit(app.exec())