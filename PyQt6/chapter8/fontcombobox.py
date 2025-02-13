#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   fontcombobox.py
@Time    :   2023/07/04 21:00:17
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QFontComboBox简单举例

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFontComboBox, QComboBox
from PyQt6.QtGui import QFont, QFontDatabase

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.resize(300, 200)
        self.setWindowTitle("QFontComboBox举例")

        self.label = QLabel("微信公众号：学点编程吧")
        # 字体下拉框设置
        font_combo = QFontComboBox(self)
        font_combo.setWritingSystem(QFontDatabase.WritingSystem.SimplifiedChinese)  # 设置只显示简体中文字体
        font_combo.setFontFilters(QFontComboBox.FontFilter.ScalableFonts)  # 过滤只显示可缩放字体
        # 字体大小下拉框设置
        self.size_combo = QComboBox(self)
        self.size_combo.addItems(["10", "12", "14", "16", "18", "20", "22", "24", "26", "28"])
        # 应用字体下拉框当前字体给标签，大小设置为下拉框当前的数值
        self._font = font_combo.currentFont()
        self._font.setPointSize(int(self.size_combo.currentText())) # 返回的数值是str类型的，需要转换成int类型
        self.label.setFont(self._font)

        font_combo.currentFontChanged.connect(self.update_font)
        self.size_combo.textActivated.connect(self.update_font)
        # 布局
        vlayout = QVBoxLayout(self)
        vlayout.addWidget(font_combo)
        vlayout.addWidget(self.size_combo)
        vlayout.addWidget(self.label)
        self.setLayout(vlayout)

        self.show()

    def update_font(self, var):
        """
        更新标签的字体
        var；字体样式或者字体大小
        """
        if isinstance(var, QFont): # 判断传递过来的参数是否为QFont类型
            self._font = var
            self._font.setPointSize(int(self.size_combo.currentText()))
        else:
            self._font.setPointSize(int(var))
        self.label.setFont(self._font)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())
    
