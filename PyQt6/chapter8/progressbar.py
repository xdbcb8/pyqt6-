#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   progressbar.py
@Time    :   2023/07/06 21:58:41
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QProgressBar简单举例：赛马

import sys
import random
from PyQt6.QtWidgets import QWidget, QApplication, QProgressBar, QMessageBox, QVBoxLayout, QToolButton
from PyQt6.QtCore import QTimer

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 200)
        self.setWindowTitle("QProgressBar举例——跑马大赛")
        self.pb11runway = 0 # 第一组第一匹马的跑步长度
        self.pb12runway = 0 # 第一组第二匹马的跑步长度
        self.pb21runway = 0 # 第二组第一匹马的跑步长度
        self.pb22runway = 0 # 第二组第二匹马的跑步长度
        self.pb11 = QProgressBar(self) # 代表第一组第一匹马
        self.pb12 = QProgressBar(self) # 代表第一组第二匹马
        self.pb21 = QProgressBar(self) # 代表第二组第一匹马
        self.pb22 = QProgressBar(self) # 代表第二组第二匹马
        self.pb21.setInvertedAppearance(True) # 第二组行进方向和第一组是反的
        self.pb22.setInvertedAppearance(True)
        pb3 = QProgressBar(self)
        pb3.setRange(0, 0)  # 没啥用，只是为了演示赛事非常紧张，很忙的样子
        self.button = QToolButton(self)
        self.button.setText("比赛开始")

        # 布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.pb11)
        layout.addWidget(self.pb12)
        layout.addStretch()
        layout.addWidget(self.pb21)
        layout.addWidget(self.pb22)
        layout.addWidget(self.button)
        layout.addWidget(pb3)
        self.setLayout(layout)

        self.button.clicked.connect(self.start)

        self.show()
    
    def start(self):
        """
        比赛开始
        """
        self.button.setEnabled(False) # 开始按钮禁用
        self.timer = QTimer(self) # 设定一个定时器
        self.timer.timeout.connect(self.running)
        self.timer.start(1000) # 每隔1秒所有马匹行动一次

    def running(self):
        """
        赛马了
        """
        # 两组赛道不同马匹的瞬时速度
        randompb11 = random.randrange(1, 8)
        randompb12 = random.randrange(1, 8)
        randompb21 = random.randrange(1, 8)
        randompb22 = random.randrange(1, 8)
        # # 两组赛道不同马匹的跑步长度的累加
        self.pb11runway += randompb11
        self.pb12runway += randompb12
        self.pb21runway += randompb21
        self.pb22runway += randompb22
        self.pb11.setValue(self.pb11runway if self.pb11runway <= 100 else 100) # 进度条的最大值是100，超过100的，强制为100
        self.pb12.setValue(self.pb12runway if self.pb12runway <= 100 else 100)
        self.pb21.setValue(self.pb21runway if self.pb21runway <= 100 else 100)
        self.pb22.setValue(self.pb22runway if self.pb22runway <= 100 else 100)

        if self.pb11.value() == self.pb11.maximum():
            QMessageBox.information(self, "喜报", "恭喜第一组第一匹马获得冠军！")
            self.reset()
        elif self.pb12.value() == self.pb12.maximum():
            QMessageBox.information(self, "喜报", "恭喜第一组第二匹马获得冠军！")
            self.reset()
        elif self.pb21.value() == self.pb21.maximum():
            QMessageBox.information(self, "喜报", "恭喜第二组第一匹马获得冠军！")
            self.reset()
        elif self.pb22.value() == self.pb22.maximum():
            QMessageBox.information(self, "喜报", "恭喜第二组第二匹马获得冠军！")
            self.reset()

    def reset(self):
        """
        所有的参数全部重置
        """
        self.timer.stop() # 定时器停止并删除对象
        del self.timer
        self.pb11.reset()
        self.pb12.reset()
        self.pb21.reset()
        self.pb22.reset()
        self.pb11runway = 0
        self.pb12runway = 0
        self.pb21runway = 0
        self.pb22runway = 0
        self.button.setEnabled(True) # 开始按钮重新启用

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = MyWidget()
    sys.exit(app.exec())