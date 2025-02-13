#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   colordialog.py
@Time    :   2023/07/11 07:09:24
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第9章第1节QColorDialog

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QColorDialog, QLabel, QPushButton, QHBoxLayout, QSizePolicy

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.setWindowTitle("QColorDialog举例")
        self.label= QLabel()
        self.label.setAutoFillBackground(True) # 自动填充背景颜色
        button = QPushButton("选择颜色")
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed) # 固定按钮尺寸，以免变形
        hlayout = QHBoxLayout(self)
        hlayout.addWidget(self.label)
        hlayout.addWidget(button)
        button.clicked.connect(self.SelectColor)
        self.show()

    def SelectColor(self):
        """
        选择标签颜色
        """
        # 这里指定了显示Alpha通道的样式只是为了举例而已
        color = QColorDialog.getColor(title="选择喜欢的颜色吧！", options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        # color = QColorDialog.getColor(title="选择喜欢的颜色吧！") # 这样就会没有AlphaChannel选项
        if color.isValid():
            pal = self.label.palette() # QPalette类包含控件状态的颜色组
            pal.setColor(self.label.backgroundRole(), color) # 背景为选择的颜色
            self.label.setPalette(pal) # 设置背景颜色

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())