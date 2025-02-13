#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   timer.py
@Time    :   2023/09/05 06:22:05
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

# 第14章第2节挑战记忆力小游戏

import sys
import random
from PyQt6.QtWidgets import QWidget, QApplication, QToolButton, QLabel, QGridLayout, QSizePolicy, QMessageBox, QMenu
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont, QAction

class Button(QToolButton):
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred) # 设定控件尺寸的策略Expanding/Preferred

    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buttonList = [] # 按钮列表
        self.guessNumList = [] # 随机数字列表
        self.button2NUmList = [] # 按钮和数字对应关系列表
        self.correctNum = -1 # 需要猜的数字
        self.leftTime = 3 # 剩余时间
        self.cnt = 0 # 猜对的次数
        self.initUI()
        self.initData()

    def initUI(self):
        """
        界面
        """
        self.setWindowTitle("QTimer举例")
        self.resize(700, 600)
        self.oklabel = QLabel("你猜对了 0 次", self)
        self.fontSetting(self.oklabel, 12)
        self.button1 = Button(self)
        self.button2 = Button(self)
        self.button3 = Button(self)
        self.button4 = Button(self)
        self.button5 = Button(self)
        self.button6 = Button(self)
        self.button7 = Button(self)
        self.button8 = Button(self)
        self.label = QLabel(self)
        # 布局
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1)
        layout.addWidget(self.button1, 0, 3)
        layout.addWidget(self.button2, 1, 1)
        layout.addWidget(self.button3, 1, 5)
        layout.addWidget(self.button4, 3, 0)
        layout.addWidget(self.button5, 3, 6)
        layout.addWidget(self.button6, 5, 1)
        layout.addWidget(self.button7, 5, 5)
        layout.addWidget(self.button8, 6, 3)
        layout.addWidget(self.label, 3, 2, 1, 3)
        self.setLayout(layout)
        self.show()

        for i in range(1, 9):  # 将按钮添加到按钮列表中
            self.buttonList.append(eval(f"self.button{i}"))
            eval(f"self.button{i}.clicked.connect(self.guessAnswer)")

    def isEnableButton(self, flag):
        """
        设置按钮是否禁用
        flag：True为启用，反之禁用
        """
        if flag:
            for button in self.buttonList:
                button.setEnabled(True)
        else:
            for button in self.buttonList:
                button.setEnabled(False)

    def fontSetting(self, widget, size):
        """
        设置字体大小
        widget：要设置大小的控件
        size：字体大小
        """
        font = QFont()
        font.setPointSize(size)
        widget.setFont(font)

    def buttonSetting(self):
        """
        设置按钮上对应的数字
        """
        self.isEnableButton(False)
        for item in self.button2NUmList:
            button = item[0]
            number =item[1]
            self.fontSetting(button, 15)
            button.setText(str(number))

    def initData(self):
        """
        数据初始化
        """
        self.fontSetting(self.label, 15)
        self.label.setText("你有3秒钟时间\n可以记住按钮上的数字！")
        self.guessNumList = random.sample(range(0, 10), 8) # 随机抽取8个数字
        self.button2NUmList = list(zip(self.buttonList, self.guessNumList)) # 将按钮和数字组合
        self.buttonSetting()
        self.correctNum = random.choice(self.guessNumList) # 随机给出需要猜的数字
        QTimer.singleShot(2000, self.begin) # 单次计时

    def begin(self):
        """
        游戏开始
        """
        self.label.clear()
        self.fontSetting(self.label, 40)
        self.label.setText(f"{self.leftTime}...")
        timer2 = QTimer(self)
        timer2.start(1000)
        timer2.timeout.connect(lambda:self.remember(timer2))

    def remember(self, timer):
        """
        记忆数字
        timer：定时器
        """
        self.leftTime -= 1
        if self.leftTime > 0:
            self.label.setText(f"{self.leftTime}...") # 展示剩余时间
        elif self.leftTime == 0: # 剩余时间为0时，定时器停止
            timer.stop()
            for button in self.buttonList:
                button.setText("")
            self.label.clear()
            self.fontSetting(self.label, 15)
            self.label.setText(f"数字 {self.correctNum} 是哪个按钮？") # 告诉你具体要猜哪个数字
            self.isEnableButton(True)

    def getCorrectButton(self):
        """
        得到待猜数字对应的按钮对象
        """
        for item in self.button2NUmList:
            if item[1] == self.correctNum:
                return item[0]

    def guessAnswer(self):
        """
        判断数字是否猜正确
        """
        buttonObj = self.sender()
        correctButton = self.getCorrectButton()
        if buttonObj == correctButton:
            self.cnt += 1
            QMessageBox.information(self, "结果", "猜对了，你的记忆力真好！")
            self.oklabel.setText(f"你猜对了 {self.cnt} 次")
        else:
            QMessageBox.information(self, "结果", "哈哈，猜错了，来看看正确答案吧！")
        self.buttonSetting()

    def contextMenuEvent(self, event):
        """
        单击鼠标右键，重新开始游戏
        """
        menu = QMenu(self)
        restartAction = QAction("重新开始", menu)
        menu.addAction(restartAction)
        restartAction.triggered.connect(self.restartGame)
        menu.popup(self.mapToGlobal(event.pos()))

    def restartGame(self):
        """
        重新开始游戏
        """
        self.leftTime = 3 # 重置剩余时间
        self.guessNumList.clear() #  重置随机数字
        self.button2NUmList.clear() # 重置按钮和数字对应关系
        self.initData()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())