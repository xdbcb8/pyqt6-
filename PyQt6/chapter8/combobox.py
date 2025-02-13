#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   combobox.py
@Time    :   2023/07/03 17:36:34
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# QComboBox简单举例

import sys
import os
from PyQt6.QtWidgets import QWidget, QApplication, QComboBox, QLabel, QVBoxLayout
from PyQt6.QtGui import QIcon

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.setWindowTitle("QComboBox举例")
        combobox = QComboBox(self)
        infomation = ["选项一", "选项二", "选项三"]
        combobox.addItems(infomation) # 增加选项列表
        combobox.insertItem(3, QIcon(f"{current_dir}\\toolbtnicon.png"), "这个选项是有图标的哦") # 插入一个带图标的选项
        self.label1 = QLabel("你选中了：", self)
        self.label2 = QLabel("当前待选择项：", self)

        # 布局
        vlayout= QVBoxLayout(self)
        vlayout.addWidget(combobox)
        vlayout.addStretch(1)
        vlayout.addWidget(self.label1)
        vlayout.addWidget(self.label2)
        self.setLayout(vlayout)

        combobox.textActivated.connect(self.showActivated)
        combobox.textHighlighted.connect(self.showHighlighted)
        self.show()

    def showActivated(self, Activatedtext):
        """
        选中后在窗体显示出来
        Activatedtext：选中的文本
        """
        self.label1.setText(f"你曾经选中过：{Activatedtext}")

    def showHighlighted(self, Highlightedtext):
        """
        光标在选项上移动在窗体显示出来
        Highlightedtext：光标在上面的文本
        """
        self.label2.setText(f"当前待选择项：{Highlightedtext}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())