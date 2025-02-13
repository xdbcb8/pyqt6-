#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   slider.py
@Time    :   2023/07/06 12:08:21
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# QSlider简单举例

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QSlider, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.setWindowTitle("QSlider举例")
        self.sld1 = QSlider(Qt.Orientation.Vertical, self) # 垂直方向
        self.sld2 = QSlider(Qt.Orientation.Horizontal, self) # 水平方向
        self.sld3 = QSlider(Qt.Orientation.Horizontal, self)
        self.sld3.setTickPosition(QSlider.TickPosition.TicksBelow) # 刻度线在下方
        self.sld3.setTickInterval(1) # 间隔设置为1
        self.sld1.setRange(10, 30) # 滑块的值范围
        self.sld2.setRange(10, 30)
        self.sld3.setRange(10, 30)
        self.sldList = [self.sld1, self.sld2, self.sld3] # 构建一个由三个滑块对象组成的列表
        self.label = QLabel("微信公众号：学点编程吧", self)
        
        # 布局
        layout = QGridLayout(self)
        layout.addWidget(self.sld2, 0, 0)
        layout.addWidget(self.sld3, 1, 0)
        layout.addWidget(self.label, 2, 0)
        layout.addWidget(self.sld1, 0, 1, 3, 1)
        self.setLayout(layout)

        self.sld1.valueChanged.connect(self.changevalue)
        self.sld2.valueChanged.connect(self.changevalue)
        self.sld3.valueChanged.connect(self.changevalue)

        self.show()
    
    def changevalue(self, value):
        """
        滑块拖动时，标签上的字体随之变化
        value：滑块当前值
        """
        # 剔除当前拖动的滑块，剩余的滑块组成一个新的列表
        new_sld_list = [item for item in self.sldList if item != self.sender()]
        for newItem in new_sld_list: # 对剩下的两个滑块的当前值进行设置
            newItem.setValue(value)
        font = QFont()
        font.setPointSize(value)
        self.label.setFont(font) # 设置标签字体的大小
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = MyWidget()
    sys.exit(app.exec())