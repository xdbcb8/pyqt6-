#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dial.py
@Time    :   2023/07/06 13:28:50
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# QDial举例：左轮手枪游戏

import sys
import random
from PyQt6.QtWidgets import QWidget, QApplication, QDial, QToolButton, QHBoxLayout, QVBoxLayout, QMessageBox

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initData()
        self.initUI()

    def initData(self):
        """
        数据初始化
        """
        self.target = random.randrange(0, 6) # 目标随机数
        self.random_list = random.sample(range(0, 6), 6) # 让拨号盘每次的值都对应列表中的一个数字，这个对应数字每次是随机的
        self.currentValue = 0 # 当前值

    def initUI(self):
        self.resize(300, 200)
        self.setWindowTitle("QDial举例--左轮手枪游戏")
        self.pistol = QDial(self) # 用拨号盘表示左轮手枪
        self.pistol.setRange(0, 5) # 设置范围
        self.pistol.setNotchesVisible(True) # 槽口可见
        self.pistol.setEnabled(False) # 开始的时候禁用
        self.button_start = QToolButton(self)
        self.button_start.setText("开动扳机")
        self.button_start.setAutoRaise(True) # 自动悬浮
        self.button_reset = QToolButton(self)
        self.button_reset.setText("重新开始")
        self.button_reset.setEnabled(False) # 开始时禁用
        # 布局
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.button_start)
        vlayout.addWidget(self.button_reset)
        hlayout = QHBoxLayout(self)
        hlayout.addWidget(self.pistol)
        hlayout.addLayout(vlayout)
        self.setLayout(hlayout)

        self.button_start.clicked.connect(self.shoot)
        self.button_reset.clicked.connect(self.reset)
        
        self.show()
    
    def shoot(self):
        """
        射击
        """
        self.pistol.setEnabled(True)
        self.pistol.setValue(self.currentValue) # 每“开枪一次”，让转盘转动一次，就像左轮手枪转盘转动一样
        # 和目标随机数字一致就弹窗
        if self.random_list[self.currentValue] == self.target:
            QMessageBox.critical(self, "哎呀", "你中枪了！")
            self.button_reset.setEnabled(True)
            self.button_start.setEnabled(False)
        self.currentValue += 1

    def reset(self):
        """
        重新开始
        """
        self.initData()
        self.pistol.setValue(self.currentValue)
        self.button_start.setEnabled(True)
        self.button_reset.setEnabled(False)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = MyWidget()
    sys.exit(app.exec())