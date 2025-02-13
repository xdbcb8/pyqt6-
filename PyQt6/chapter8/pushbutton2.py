#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pushbutton2.py
@Time    :   2023/06/22 07:03:32
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QPushButton举例：发送验证码

import sys
from PyQt6.QtWidgets import QPushButton, QApplication, QWidget
from PyQt6.QtCore import QTimer


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.time = 20 # 等待的时间
        self.resize(300, 200)
        self.setWindowTitle("倒计时按钮")
        self.button = QPushButton("发送验证码...", self)
        self.button.move(100, 50)
        self.button.clicked.connect(self.emitCode)

        self.show()

    def emitCode(self):
        """
        发送验证码
        """
        self.button.setEnabled(False)
        self.button.setText("20秒后重发...")
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.Refresh)

    def Refresh(self):
        """
        等待验证码
        """
        self.time -= 1
        if self.time > 0:
            self.button.setText(f"{self.time}秒后重发...")
        else:
            self.button.setText("发送验证码...")
            self.button.setEnabled(True)
            self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())