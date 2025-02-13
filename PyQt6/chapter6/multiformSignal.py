#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   multiformSignal.py
@Time    :   2023/05/19 15:59:47
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 使用信号与槽机制传递

import sys
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

class SubWidget(QDialog):
    send_text = pyqtSignal(str)  # 新建用于传值的信号

    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.initUI()
    
    def initUI(self):
        """构建界面"""
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
        bt.clicked.connect(self.reject) # 单击“取消”按钮关闭对话框

    def send2main(self):
        """对话框信息发送到主窗体"""
        ntext = self.line_edit.text()
        self.send_text.emit(ntext)  # 将输入栏的内容发射出去
        self.accept() # 单击“发送”按钮关闭对话框窗体

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
        sub_window = SubWidget(self)
        sub_window.send_text.connect(self.receive_text)  # 收到对话框发送的信号
        sub_window.exec()

    def receive_text(self, text):
        """显示收到的内容"""
        self.label.setText(f"收到的对话框信息：{text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainW = MainWidget()
    mainW.show()
    sys.exit(app.exec())