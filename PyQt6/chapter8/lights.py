#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   lights.py
@Time    :   2023/06/23 18:47:30
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第8章第6节红绿灯

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class Light(QWidget):
    """
    本程序红绿灯切换，采用手动和自动相结合的方式，否则全部自动切换总是差一秒。
    """
    def __init__(self):
        super().__init__()
        self.flag = -1 # 红绿灯的标志，-1绿色，0黄色，1红色
        self.sec = 0  # 计时器
        self.initUI()

    def initUI(self):
        self.setWindowTitle("红绿灯模拟")
        self.resize(400, 200)

        # 窗体背景颜色为黑色
        pal = self.palette() # QPalette类包含控件状态的颜色组
        pal.setColor(self.backgroundRole(), Qt.GlobalColor.black) # 背景为黑色
        self.setPalette(pal)
        
        # 红绿灯安排起，初始均为黑色
        self.red = QLabel(self)
        self.red.setPixmap(QPixmap(f"{current_dir}\\black.png"))
        self.yellow = QLabel(self)
        self.yellow.setPixmap(QPixmap(f"{current_dir}\\black.png"))
        self.green = QLabel(self)
        self.green.setPixmap(QPixmap(f"{current_dir}\\black.png"))

        # 红绿灯及剩余时间的布局
        layout = QGridLayout(self)
        layout.addWidget(self.red, 0, 0)
        layout.addWidget(self.yellow, 0, 1)
        layout.addWidget(self.green, 0, 2)
        self.info = QLabel(self)
        layout.addWidget(self.info, 1, 0, 1, 6)
        self.setLayout(layout)
        # 剩余时间采用样式表的方式，设置个性化字体，颜色为白色，字体大小为22pt
        self.info.setStyleSheet("font: 22pt;color: rgb(255, 255, 255);")

        # 手动立即让红绿灯运行一次
        self.changeColor(0)
        
        # 设定定时器
        timer = QTimer(self)
        timer.start(1000)
        timer.timeout.connect(lambda:self.changeColor(1))
        self.show()

    def settiingColor(self, color):
        """
        红绿灯切换
        color：红绿灯的颜色
        """
        if color == "green":
            self.green.setPixmap(QPixmap(f"{current_dir}\\green.png"))
            self.red.setPixmap(QPixmap(f"{current_dir}\\black.png"))
            self.yellow.setPixmap(QPixmap(f"{current_dir}\\black.png"))
        elif color == "red":
            self.green.setPixmap(QPixmap(f"{current_dir}\\black.png"))
            self.red.setPixmap(QPixmap(f"{current_dir}\\red.png"))
            self.yellow.setPixmap(QPixmap(f"{current_dir}\\black.png"))
        else:
            self.green.setPixmap(QPixmap(f"{current_dir}\\black.png"))
            self.red.setPixmap(QPixmap(f"{current_dir}\\black.png"))
            self.yellow.setPixmap(QPixmap(f"{current_dir}\\yellow.png"))
    
    def settingLight(self, color, time):
        """
        显示具体的红绿灯
        color：颜色
        time：当前已经运行的时间
        """
        self.settiingColor(color)
        if color == "yellow": # 黄灯显示3秒
            leftTime = 3 - time
        else:
            leftTime = 10 - time # 红绿灯显示10秒
        if 1 <= leftTime <= 3:
            self.info.setText(f"剩余：{str(leftTime)}秒") # 3秒内显示剩余时间
        elif leftTime == 0: # 当剩余时间为0时，红绿灯的标志加1；当剩余时间大于1是，红绿灯的标志将自动转换为-1
            self.flag += 1
            if self.flag > 1:
                self.flag = -1
            # 剩余时间的文字和秒数全部清除
            self.info.clear()
            self.sec = 0
            # 手动再切换一次红绿灯
            self.changeColor(0)

    def changeColor(self, auto):
        """
        红绿灯的切换控制
        auto：手动控制和自动控制，0为手动切换，1为自动切换
        """
        if auto == 1: # 自动切换时时间加1
            self.sec += 1
        if self.flag == -1:
            self.settingLight("green", self.sec)
        elif self.flag == 0:
            self.settingLight("yellow", self.sec)
        else:
            self.settingLight("red", self.sec)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    light = Light()
    sys.exit(app.exec())
        