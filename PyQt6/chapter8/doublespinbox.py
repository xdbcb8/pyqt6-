#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   doublespinbox.py
@Time    :   2023/07/02 19:12:16
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QDoubleSpinBox简单举例

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QDoubleSpinBox, QLabel, QSpinBox, QGridLayout
        
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 100)
        self.setWindowTitle("QDoubleSpinBox举例")
        
        self.doublespinbox = QDoubleSpinBox(self)
        self.doublespinbox.setRange(0, 1) # 数值范围
        self.doublespinbox.setDecimals(1) # 初始精度为1
        self.doublespinbox.setSingleStep(0.1) # 初始单步步长

        self.label1 = QLabel(f"单步步长：{0.1}", self)
        label2 = QLabel("QDoubleSpinBox精度设置为：", self)

        self.spinbox = QSpinBox(self)
        self.spinbox.setRange(1, 8) # QDoubleSpinbox可调整的精度范围1~8

        # 布局
        layout = QGridLayout(self)
        layout.addWidget(self.doublespinbox, 0, 0)
        layout.addWidget(self.label1, 1, 0)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(self.spinbox, 2, 1)
        self.setLayout(layout)
        
        self.spinbox.valueChanged.connect(self.setDecimal)
        self.show()
        
    def setDecimal(self, value):
        '''
        设置精度
        '''
        singleStep = 1.0/pow(10, value) # 精度
        self.doublespinbox.setDecimals(value) # 设置精度
        self.label1.setText(f"单步步长：{singleStep:.{value}f}")
        self.doublespinbox.setSingleStep(singleStep)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())