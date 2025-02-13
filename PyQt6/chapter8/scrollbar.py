#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   scrollbar.py
@Time    :   2023/07/06 17:47:41
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# QScrollBar简单举例

import sys
from PyQt6.QtWidgets import QApplication, QScrollBar, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.setWindowTitle("QScrollBar举例")
        scroll_bar = QScrollBar(self)
        scroll_bar.setMaximum(20)  # 设置最大值为20
        scroll_bar.setMinimum(0)  # 设置最小值为0
        scroll_bar.setPageStep(2)  # 设置点击滑块的页面步长为2
        scroll_bar.setOrientation(Qt.Orientation.Horizontal)  # 设置为水平方向

        # 布局
        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        layout.addWidget(self.label)
        layout.addWidget(scroll_bar)
        self.setLayout(layout)

        self.show()

        scroll_bar.valueChanged.connect(self.on_value_changed)

    def on_value_changed(self, value):
        """
        value：滚动条值
        """
        font = QFont()
        font.setPointSize(20)
        self.label.setText(str(value))
        self.label.setFont(font) # 字体大小设置成20

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    sys.exit(app.exec())
