#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   eventexample.py
@Time    :   2023/04/28 11:11:42
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 事件演示

import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QLineEdit
from PyQt6.QtCore import QEvent, Qt

class Text(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("event()方法如何传递事件的")
        self.resize(400, 30)
    
    def event(self, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_T:
                currentTime = datetime.strftime(datetime.now(), "%Y-%m-%d, %H:%M:%S")
                print(f"{currentTime} 按T键!")
                return True
        # return False # 其他的事件都不会被响应，直接导致输入不可用
        return super().event(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    text = Text()
    text.show()
    sys.exit(app.exec())