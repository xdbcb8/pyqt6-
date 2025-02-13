#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   errormessage.py
@Time    :   2023/07/11 11:26:26
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第9章第2节QErrorMessage

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QErrorMessage, QPushButton

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.setWindowTitle("QErrorMessage举例")
        button = QPushButton("打开错误消息", self)
        button.clicked.connect(self.getError)
        button.move(100, 100)
        self.show()

    def getError(self):
        error_message = QErrorMessage(self)
        error_message.setWindowTitle("哎呀，报错！")
        error_message.showMessage("不用找了，这个地方真的错了！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())