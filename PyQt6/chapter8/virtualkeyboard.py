#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   virtualkeyboard.py
@Time    :   2023/06/22 17:13:58
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 虚拟键盘

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, QCoreApplication

class VirtualKeyboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.flag = False # "↑"按钮是否被按下的标志
        self.key2Value = {"0":Qt.Key.Key_0, "1":Qt.Key.Key_1, "2":Qt.Key.Key_2, "3":Qt.Key.Key_3, 
                          "4":Qt.Key.Key_4, "5":Qt.Key.Key_5, "6":Qt.Key.Key_6, "7":Qt.Key.Key_7, 
                          "8":Qt.Key.Key_8, "9":Qt.Key.Key_9, "A":Qt.Key.Key_A, "B":Qt.Key.Key_B, 
                          "C":Qt.Key.Key_C, "D":Qt.Key.Key_D, "E":Qt.Key.Key_E, "F":Qt.Key.Key_F, 
                          "G":Qt.Key.Key_G, "H":Qt.Key.Key_H, "I":Qt.Key.Key_I, "J":Qt.Key.Key_J, 
                          "K":Qt.Key.Key_K, "L":Qt.Key.Key_L, "M":Qt.Key.Key_M, "N":Qt.Key.Key_N, 
                          "O":Qt.Key.Key_O, "P":Qt.Key.Key_P, "Q":Qt.Key.Key_Q, "R":Qt.Key.Key_R, 
                          "S":Qt.Key.Key_S, "T":Qt.Key.Key_T, "U":Qt.Key.Key_U, "V":Qt.Key.Key_V, 
                          "W":Qt.Key.Key_W, "X":Qt.Key.Key_X, "Y":Qt.Key.Key_Y, "Z":Qt.Key.Key_Z, 
                          "←":Qt.Key.Key_Backspace}

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle("虚拟键盘")
        self.resize(300, 200)

        # 创建按键布局
        layout = QGridLayout()

        # 创建26个字母和0-9数字按键
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ←↑"  # 用于创建字母按键
        digits = "0123456789"  # 用于创建数字按键

        self.lineEdit = QLineEdit(self)
        layout.addWidget(self.lineEdit, 0, 0, 1, 6)

        # 创建字母按键
        for i, letter in enumerate(letters):
            self.button = QPushButton(letter, self)
            if letter == "↑":
                self.button.setCheckable(True)
            self.button.clicked.connect(self.keyBoard)
            layout.addWidget(self.button, i // 6 + 1, i % 6)

        # 创建数字按键
        for i, digit in enumerate(digits):
            self.button = QPushButton(digit, self)
            self.button.clicked.connect(self.keyBoard)
            layout.addWidget(self.button, i // 6 + 6, i % 6)

        # 设置按键布局
        vbox = QVBoxLayout()
        vbox.addLayout(layout)
        self.setLayout(vbox)

    def keyBoard(self):
        """
        单击按钮模拟键盘输入
        """
        text = self.sender().text() # 获得当前按键上的字符
        if text == "↑":
            self.flag = not self.flag
        else:
            if "A" <= text <= "Z" and self.flag: # 小写输入
                keyEvent = QKeyEvent(QKeyEvent.Type.KeyPress, self.key2Value[text], Qt.KeyboardModifier.NoModifier, text.lower())
            else: # 大写输入
                keyEvent = QKeyEvent(QKeyEvent.Type.KeyPress, self.key2Value[text], Qt.KeyboardModifier.NoModifier, text)
            QCoreApplication.postEvent(self.lineEdit, keyEvent)
            self.lineEdit.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VirtualKeyboard()
    window.show()
    sys.exit(app.exec())