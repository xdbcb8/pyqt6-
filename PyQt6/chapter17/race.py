#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   race.py
@Time    :   2023/10/07 21:18:04
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
import sys
import os
import random
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QMessageBox
from PyQt6.QtCore import QPropertyAnimation, Qt, QSize, QTimer, QPoint, QParallelAnimationGroup, QRect, QEasingCurve
from PyQt6.QtGui import QPixmap, QFont

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class Race(QWidget):
    def __init__(self):
        super().__init__()
        self.leftTime = 3 # 剩余时间
        self.progressTotal = 0 # 赛车行驶的里程
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("PyQt6动画举例")
        self.setFixedSize(QSize(350, 650)) # 固定窗体尺寸
        self.star = QLabel(self) # 开始位置
        self.star.setPixmap(QPixmap(f"{current_dir}\\star.png"))
        self.star.move(77, 510)

        self.car = QLabel(self) # 赛车
        self.car.setPixmap(QPixmap(f"{current_dir}\\car.png"))
        self.car.move(155, 400)
        self.car.setEnabled(False) # 赛车禁用

        self.leftTimeLabel = QLabel(self) # 剩余开始时间
        fontTime = QFont()
        fontTime.setPointSize(40)
        self.leftTimeLabel.setFont(fontTime)
        self.leftTimeLabel.move(140, 200)
        self.leftTimeLabel.setText("3")

        self.progressLabel = QLabel(self) # 显示赛车里程
        fontProgress = QFont() 
        fontProgress.setPointSize(15)
        self.progressLabel.setFont(fontProgress)
        self.progressLabel.move(100, 50)

        # 赛道的布置
        self.leftTrack1 = QLabel(self)
        self.leftTrack1.setPixmap(QPixmap(f"{current_dir}\\track.png"))
        self.leftTrack1.move(20, 0)
        self.leftTrack2 = QLabel(self)
        self.leftTrack2.setPixmap(QPixmap(f"{current_dir}\\track.png"))
        self.leftTrack2.move(20, -831)
        self.rightTrack1 = QLabel(self)
        self.rightTrack1.setPixmap(QPixmap(f"{current_dir}\\track.png"))
        self.rightTrack1.move(330, 0)
        self.rightTrack2 = QLabel(self)
        self.rightTrack2.setPixmap(QPixmap(f"{current_dir}\\track.png"))
        self.rightTrack2.move(330, -831)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showLeftTime)
        self.timer.start(1000) # 每隔一秒显示一次剩余时间
        self.show()

    def showProgress(self):
        """
        显示赛车里程
        """
        self.progressTotal += 1
        self.progressLabel.setText(f"一共前进了{self.progressTotal}米")

    def showLeftTime(self):
        """
        剩余时间
        """
        self.leftTime -= 1
        if self.leftTime == -1:
            self.timer.stop()
            self.leftTimeLabel.hide()
            self.car.setEnabled(True) # 赛车启用
            self.starAnimation()
            self.trackAnimation()

            self.timerBlock = QTimer(self)
            self.timerBlock.timeout.connect(self.createBlock)
            self.timerBlock.start(7000) # 每隔7秒随机出现一个障碍物

            self.progressLabel.setText(f"一共前进了 0 米")
            self.progressLabel.adjustSize()
            self.progressTimer = QTimer(self) # 计算赛车前进的里程
            self.progressTimer.timeout.connect(self.showProgress)
            self.progressTimer.start(1000) # 每隔1秒前进1米
        else:
            self.leftTimeLabel.setText(str(self.leftTime))
        self.leftTimeLabel.adjustSize() # 自适应大小

    def starAnimation(self):
        """
        赛车起点的动画
        """
        anim = QPropertyAnimation(self.star, b"pos", self)
        anim.setDuration(3000)
        anim.setStartValue(QPoint(77, 510))
        anim.setEndValue(QPoint(77, 700))
        anim.start()

    def trackAnimation(self):
        """
        赛道动画
        """
        animLeft1 = QPropertyAnimation(self.leftTrack1, b"pos", self)
        animLeft1.setDuration(13190)
        animLeft1.setStartValue(QPoint(20, 0))
        animLeft1.setEndValue(QPoint(20, 831))

        animLeft2 = QPropertyAnimation(self.leftTrack2, b"pos", self)
        animLeft2.setDuration(13190)
        animLeft2.setStartValue(QPoint(20, -831))
        animLeft2.setEndValue(QPoint(20, 0))
        # 以上两段代码为左侧赛道

        animRight1 = QPropertyAnimation(self.rightTrack1, b"pos", self)
        animRight1.setDuration(13190)
        animRight1.setStartValue(QPoint(330, 0))
        animRight1.setEndValue(QPoint(330, 831))

        animRight2 = QPropertyAnimation(self.rightTrack2, b"pos", self)
        animRight2.setDuration(13190)
        animRight2.setStartValue(QPoint(330, -831))
        animRight2.setEndValue(QPoint(330, 0))
        # 以上两段代码为右侧赛道

        self.animgroup1 = QParallelAnimationGroup(self) # 动画分组1
        self.animgroup1.addAnimation(animLeft1)
        self.animgroup1.addAnimation(animRight1)
        self.animgroup1.setLoopCount(-1) # 循环动画
        self.animgroup1.start()

        self.animgroup2 = QParallelAnimationGroup(self) # 动画分组2
        self.animgroup2.addAnimation(animLeft2)
        self.animgroup2.addAnimation(animRight2)
        self.animgroup2.setLoopCount(-1)
        self.animgroup2.start()

    def createBlock(self):
        """
        生成随机障碍物
        """
        self.block = QLabel(self)
        self.block.setPixmap(QPixmap(f"{current_dir}\\block.png"))
        blockX = random.randint(30, 250) # 障碍物的x轴随机坐标
        blockY = random.randint(80, 200) # 障碍物的y轴随机坐标
        self.block.move(blockX, blockY)
        self.block.show() # 显示障碍物
        
        self.blockAnimation(blockX, blockY)

    def blockAnimation(self, x, y):
        """
        障碍物动画
        obj：障碍物
        x,y：分别表示障碍物的坐标
        """
        self.blockAnim = QPropertyAnimation(self.block, b"geometry", self)
        duration = int((660 - y) / 0.063) # 动画持续时间
        self.blockAnim.setDuration(duration)
        self.blockAnim.setStartValue(QRect(x, y, 30, 51))
        self.blockAnim.setEndValue(QRect(x, 660, 30, 51))
        self.blockAnim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.blockAnim.valueChanged.connect(self.crash)
        self.blockAnim.start()

    def keyPressEvent(self, event):
        """
        重写按键事件
        """
        if not self.car.isEnabled(): # 只有等到游戏开始才能移动赛车
            return
        x = self.car.pos().x() # 此时赛车的x轴坐标
        y = self.car.pos().y() # 此时赛车的y轴坐标
        if event.key() == Qt.Key.Key_Up: # 向上
            y -= 10
            if y < 80:
                y = 80
        elif event.key() == Qt.Key.Key_Down:  # 向下
            y += 10
            if y > 530:
                y = 530
        elif event.key() == Qt.Key.Key_Left:  # 向左
            x -= 10
            if x < 38:
                x = 38
        elif event.key() == Qt.Key.Key_Right:  # 向右
            x += 10
            if x > 250:
                x = 250
        self.car.move(x, y)

    def crash(self):
        """
        检查是否发生撞车
        """
        if self.car.geometry().intersects(self.block.geometry()): # 判断是否撞车
            self.blockAnim.stop()
            self.timerBlock.stop()
            self.animgroup1.stop()
            self.animgroup2.stop()
            self.progressTimer.stop()
            QMessageBox.critical(self, "游戏失败", "撞车啦！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    race = Race()
    sys.exit(app.exec())