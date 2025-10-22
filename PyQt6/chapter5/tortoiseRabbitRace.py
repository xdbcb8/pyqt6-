#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tortoiseRabbitRace.py
@Time    :   2023/04/29 06:13:34
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 龟兔赛跑
# 完整程序位于本书配套资料的PyQt6\chapter5\tortoiseRabbitRace.py中

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

current_dir = os.path.dirname(os.path.abspath(__file__))

class Track(QWidget):
    def __init__(self):
        super().__init__()
        self.xt, self.xr = 0, 0  # 记录乌龟和兔子起始位置x轴的坐标，self.xt代表乌龟，self.xr代表兔子。
        self.initUI()

    def initUI(self):
        self.setWindowTitle("龟兔赛跑")
        self.setFixedSize(500, 150)  # 赛道的窗体固定为500×150 px

        # 以前的代码，显示的是乌龟和兔子的文字
        # self.tortoise = QLabel("<b>乌龟</b>", self)
        # self.rabbit = QLabel("<b>兔子</b>", self)
        # self.tortoise.setGeometry(self.xt, 20, 30, 30)  # 乌龟的起始位置
        # self.rabbit.setGeometry(self.xr, 80, 30, 30)  # 兔子的起始位置

        # 创建乌龟和兔子的图片显示
        self.tortoise = QLabel(self)
        self.rabbit = QLabel(self)
        self.tortoise.setPixmap(QPixmap(f'{current_dir}\\tortoise.png'))
        self.rabbit.setPixmap(QPixmap(f'{current_dir}\\rabbit.png'))

        # 设置位置
        self.tortoise.move(self.xt, 0)  # 乌龟的起始位置
        self.rabbit.move(self.xr, 70)  # 兔子的起始位置
        
        self.show()

    def running(self, runner):
        """
        跑步
        runner：乌龟还是兔子
        """
        if runner == self.tortoise:
            self.xt += 30 # 乌龟每次移动的x坐标增加30px
            runner.move(self.xt, 0)
        else:
            self.xr += 30
            runner.move(self.xr, 70)

    def resetMatch(self):
        """
        重置比赛
        """
        self.xt, self.xr = 0, 0
        self.tortoise.move(self.xt, 0)  # 乌龟的起始位置
        self.rabbit.move(self.xr, 70)  # 兔子的起始位置

    def matchResults(self):
        """
        比赛结果判断
        """
        if self.xt >= 500:
            QMessageBox.information(self, "比赛结果", "恭喜乌龟获得胜利，比赛重新开始！")
            self.resetMatch()
        elif self.xr >= 500:
            QMessageBox.information(self, "比赛结果", "恭喜兔子获得胜利，比赛重新开始！")
            self.resetMatch()

    def keyPressEvent(self, event):
        """
        重写按键事件
        """
        if event.key() == Qt.Key.Key_D: # 乌龟的按键
            self.running(self.tortoise)
        elif event.key() == Qt.Key.Key_Right:  # 兔子的按键
            self.running(self.rabbit)
        self.matchResults() # 判断比赛结果
        return super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    race = Track()
    sys.exit(app.exec())
