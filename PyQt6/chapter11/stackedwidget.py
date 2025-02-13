#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stackedwidget.py
@Time    :   2023/08/05 21:06:55
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

# 第11章第3节堆栈窗体控件

import random
import sys
from PyQt6.QtWidgets import QWidget, QApplication, QStackedWidget, QSpinBox, QLineEdit, QPushButton, QVBoxLayout, QLabel, QSplitter, QHBoxLayout

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QStackedWidget举例")
        # 第1个窗体控件
        widget1 = QWidget()
        self.spinbox1 = QSpinBox(widget1)
        self.spinbox1.setRange(1, 100)
        laytout1 = QVBoxLayout()
        laytout1.addWidget(QLabel("选第一个数？"))
        laytout1.addWidget(self.spinbox1)
        laytout1.addStretch(1)
        widget1.setLayout(laytout1)
        # 第2个窗体控件
        widget2 = QWidget()
        self.spinbox2 = QSpinBox(widget2)
        self.spinbox2.setRange(1, 100)
        laytout2 = QVBoxLayout()
        laytout2.addWidget(QLabel("选第二个数？"))
        laytout2.addWidget(self.spinbox2)
        laytout2.addStretch(1)
        widget2.setLayout(laytout2)
        # 第3个窗体控件
        widget3 = QWidget()
        self.spinbox3 = QSpinBox(widget3)
        self.spinbox3.setRange(1, 100)
        laytout3 = QVBoxLayout()
        laytout3.addWidget(QLabel("选第三个数？"))
        laytout3.addWidget(self.spinbox3)
        laytout3.addStretch(1)
        widget3.setLayout(laytout3)
        # 第4个窗体控件
        widgetAnswer =  QWidget()
        self.lineAnwer = QLineEdit(widgetAnswer)
        self.lineAnwer.setClearButtonEnabled(True)
        self.button = QPushButton("提交答案", widgetAnswer)
        laytoutAnswer = QVBoxLayout()
        self.CorrectanswerLabel = QLabel(widgetAnswer)
        laytoutAnswer.addWidget(QLabel("输入你的答案吧！"))
        laytoutAnswer.addWidget(self.lineAnwer)
        laytoutAnswer.addWidget(self.button)
        laytoutAnswer.addWidget(self.CorrectanswerLabel)
        widgetAnswer.setLayout(laytoutAnswer)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(widget1)
        self.stacked_widget.addWidget(widget2)
        self.stacked_widget.addWidget(widget3)
        self.stacked_widget.addWidget(widgetAnswer)
        # 每一步的按钮
        widgetLeft = QWidget()
        self.button1 = QPushButton("第一步", widgetLeft)
        self.button2 = QPushButton("第二步", widgetLeft)
        self.button3 = QPushButton("第三步", widgetLeft)
        self.button4 = QPushButton("最后", widgetLeft)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
        vleftLayout = QVBoxLayout(widgetLeft)
        vleftLayout.addWidget(QLabel("猜猜最终的数字是什么？"))
        vleftLayout.addWidget(self.button1)
        vleftLayout.addWidget(self.button2)
        vleftLayout.addWidget(self.button3)
        vleftLayout.addWidget(self.button4)
        widgetLeft.setLayout(vleftLayout)
        # 分裂器
        splitter = QSplitter(self)
        splitter.addWidget(widgetLeft)
        splitter.addWidget(self.stacked_widget)

        hlayout = QHBoxLayout(self)
        hlayout.addWidget(splitter)
        self.setLayout(hlayout)
        
        self.show()
        # 记录每次选择的数字
        self.spinbox1.valueChanged.connect(self.nextT)
        self.spinbox2.valueChanged.connect(self.nextS)
        self.spinbox3.valueChanged.connect(self.nextF)
        # 操作每个步骤
        self.button2.clicked.connect(self.Step2)
        self.button3.clicked.connect(self.Step3)
        self.button4.clicked.connect(self.Step4)
        self.button.clicked.connect(self.getAnswer)

    # 第1个数
    def nextT(self):
        self.button2.setEnabled(True)
        self.button1.setEnabled(False)
        self.one = self.spinbox1.value()
    # 第2个数
    def nextS(self):
        self.button3.setEnabled(True)
        self.button2.setEnabled(False)
        self.two = self.spinbox2.value()
    # 第3个数
    def nextF(self):
        self.button4.setEnabled(True)
        self.button3.setEnabled(False)
        self.three = self.spinbox3.value()

    # 进入第2个窗体
    def Step2(self):
        self.stacked_widget.setCurrentIndex(1)

    # 进入第3个窗体
    def Step3(self):
        self.stacked_widget.setCurrentIndex(2)

    # 进入第4个窗体
    def Step4(self):
        self.stacked_widget.setCurrentIndex(3)

    def getAnswer(self):
        """
        获得答案
        """
        answerUser = self.lineAnwer.text() # 用户输入的答案
        if not answerUser:
            return
        op = random.choice(['+', '-', '*', '/']) # 随机抽取运算符
        answerStr = str(self.one) + op + str(self.two) + op + str(self.three)
        if int(answerUser) == eval(answerStr):
            self.CorrectanswerLabel.setText("回答正确！")
        else:
            self.CorrectanswerLabel.setText(f"你输了！正确答案是：\n{answerStr} = {eval(answerStr)}")
        self.button.setEnabled(False) #输入答案后就不能再提交了

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())