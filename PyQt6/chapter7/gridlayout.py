#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gridlayout.py
@Time    :   2023/06/08 17:28:32
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 网格布局举例——模拟小键盘
# 完整程序位于本书配套资料的PyQt6\chapter7\gridlayout.py中

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QSizePolicy, QToolButton

class Button(QToolButton):
    """
    自定义QToolButton类
    """
    def __init__(self, text, Parent=None):
        super().__init__(Parent)
        self.setText(text) # 设置按钮上的字符
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred) # 设定控件尺寸的策略Expanding/Preferred

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(350, 300)
        self.setWindowTitle("栅格布局：小键盘模拟")
        digitButtons = []
        for i in range(10):  # 构造0-9这10个数字按钮
            digitButtons.append(Button(str(i), self))
        
        lockButton = Button("Num\nLock", self)
        divButton = Button("/", self)
        timesButton = Button("*", self)
        minusButton = Button("-", self)
        plusButton = Button("+", self)
        enterButton = Button("Enter", self)
        pointButton = Button(".", self)

        # 将按钮放到各自的位置
        layout = QGridLayout(self) # 创建网络布局
        layout.addWidget(lockButton, 0, 0)
        layout.addWidget(divButton, 0, 1)
        layout.addWidget(timesButton, 0, 2)
        layout.addWidget(minusButton, 0, 3)
        layout.addWidget(plusButton, 1, 3, 2, 1) # 跨行的布局
        layout.addWidget(enterButton, 3, 3, 2, 1) # 跨行的布局
        layout.addWidget(pointButton, 4, 2)
        layout.addWidget(digitButtons[0], 4, 0, 1, 2) # 跨列的布局

        # 使用循环的方式将数字按钮1～9分别按照特定的坐标放在相应的单元格中
        n = 1
        while(n < 10):
            for i in range(3, 0, -1):
                for j in range(0, 3):
                    layout.addWidget(digitButtons[n], i, j)
                    n += 1
        
        self.setLayout(layout)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())