#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   multiformShare.py
@Time    :   2023/05/19 16:00:04
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 使用QSettings类传递

import sys
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QSettings

class SubWidget(QDialog):

    def __init__(self, settings, Parent=None):
        super().__init__(Parent)
        self.settings = settings # 将QSettings对象作为子对话框中的实例变量
        self.initUI()
        
    def initUI(self):
        """对话框界面"""
        self.resize(200, 100)
        self.setWindowTitle("子对话框窗体")
        self.line_edit = QLineEdit(self)
        sendbt = QPushButton("发送", self)
        bt = QPushButton("取消", self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.line_edit)
        layout.addWidget(sendbt)
        layout.addWidget(bt)
        self.setLayout(layout)
        sendbt.clicked.connect(self.send2main)
        bt.clicked.connect(self.reject)

    def send2main(self):
        """对话框信息发送到主窗体"""
        ntext = self.line_edit.text()
        self.settings.setValue("info", ntext)
        self.accept()

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        """界面构建"""
        self.setWindowTitle("主窗体")
        self.resize(300, 200)
        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        button = QPushButton("打开子对话框", self)
        layout.addWidget(self.label)
        layout.addWidget(button)
        self.setLayout(layout)
        button.clicked.connect(self.open_subwindow)

    def open_subwindow(self):
        """新建对话框"""
        settings = QSettings("Myapp", "Multiform")
        sub_window = SubWidget(settings, self)
        res = sub_window.exec()
        if res == 1: # res为1，表明单击了子对话框中的“发送”按钮。非1就是表明，单击了子对话的“取消”按钮。
            self.label.setText(f"收到的对话框信息：{settings.value('info')}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainW = MainWidget()
    mainW.show()
    sys.exit(app.exec())