#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spinbox.py
@Time    :   2023/07/02 11:04:41
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QSpinBox简单举例

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QSpinBox, QAbstractSpinBox, QMessageBox

class myWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QSpinBox举例")
        self.resize(250, 50)
        spbox = QSpinBox(self)
        spbox.move(80, 10)
        # spbox.setDisplayIntegerBase(16) # 设置成16进制
        spbox.setStepType(QSpinBox.StepType.AdaptiveDecimalStepType) # 设置适应性单步步长，把数值范围调整到1000~10000，可以看到明显的差异
        # spbox.setStepType(QSpinBox.StepType.DefaultStepType) # 设置默认单步步长

        # #################普通整数输入框#################
        # spbox.setRange(1000, 10000) # 数值范围1000~10000
        # spbox.setSingleStep(10) # 单步步长
        # spbox.setWrapping(True) # 可以循环调整
        # spbox.setValue(1100) # 设置当前值为1100
        # spbox.setGroupSeparatorShown(True) # 显示千位分隔符

        # ##################带前后缀的整数输入框###############
        # self.spbox2 = QSpinBox(self)
        # self.spbox2.move(50, 10)
        # self.spbox2.setValue(10)
        # self.spbox2.setRange(0, 100)
        # self.spbox2.setSingleStep(10)
        # self.spbox2.setPrefix("当前进度") # 前缀
        # self.spbox2.setSuffix("%，正在充电中……") # 后缀
        # self.spbox2.setSpecialValueText("真的一点电都没了！")
        # self.spbox2.valueChanged.connect(self.showV)

        self.show()

    def showV(self, p):
        print(self.spbox2.text(), " ", self.spbox2.cleanText())
        if p == self.spbox2.maximum():
            QMessageBox.information(self, "提示", "不能充电了，已经加满了！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywidget = myWidget()
    sys.exit(app.exec())