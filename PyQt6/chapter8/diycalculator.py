#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   diycalculator.py
@Time    :   2023/06/24 15:34:59
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第8章第6节计算器

import sys
from PyQt6.QtWidgets import QApplication, QGridLayout, QSizePolicy, QToolButton, QDialog, QLCDNumber, QFrame, QMessageBox

# QLCDNumber 控件通常使用一个有符号的 32 位整数来表示数值，因此它的范围是 -2,147,483,648 到 2,147,483,647。超出会报如下错误：
# OverflowError: argument 1 overflowed: value must be in the range -2147483648 to 2147483647

class Button(QToolButton):
    def __init__(self, text, Parent=None):
        super().__init__(Parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred) # 设定控件尺寸的策略Expanding/Preferred
        self.setText(text)

    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size
    
class Calculator(QDialog):
    
    def __init__(self):
        super().__init__()
        self.lcdstring = "" # LCD显示
        self.operation = "" # 操作符
        self.currentNum = 0 # 当前数
        self.previousNum = 0 # 前一个数
        self.cresult = 0 # 结果
        self.tmp = 0 # 临时保存的结果
        self.initUI()

    def initUI(self):
        self.setWindowTitle("简单计算器")
        self.resize(400, 500)

        # LCD屏幕
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(9) # 设置LCD最多9个数字
        self.lcd.setFrameShape(QFrame.Shape.NoFrame)
        
        # 创建数字0-9按钮
        self.numButtons = []
        for i in range(10):
            self.numButtons.append(self.createButton(str(i), self.numClicked))
        
        # 创建运算符按钮
        self.plusButton = self.createButton("+", self.opClicked) # 加法
        self.minusButton = self.createButton("-", self.opClicked) # 减法
        self.timesButton = self.createButton(u"\N{MULTIPLICATION SIGN}", self.opClicked) # 乘法
        self.divButton = self.createButton(u"\N{DIVISION SIGN}", self.opClicked) # 除法
        self.pointButton = self.createButton(".", self.numClicked) # .
        self.changeSignButton = self.createButton(u"\N{PLUS-MINUS SIGN}", self.changeSignClicked) # 正负号

        # 创建计算器操作按钮
        self.backspaceButton = self.createButton("后退", self.backspaceClicked) # 后退一个数字
        self.clearButton = self.createButton("清除", self.clear) # 清除全部内容
        self.mcButton = self.createButton("MC", self.clearMemory) # 清除暂存数据
        self.mrButton = self.createButton("MR", self.loadMemory) # 读取暂存数据
        self.msButton = self.createButton("MS", self.setMemory) # 设置暂存数据
        self.mplusButton = self.createButton("M+", self.addToMemory) # 与暂存数据进行累加
        self.equalButton = self.createButton("=", self.equalClicked) # 计算结果
        self.msButton.setCheckable(True)

        # LCD的布局
        layout = QGridLayout(self)
        layout.addWidget(self.lcd, 0, 0, 3, 5)
        
        # 将0-9按钮放到各自的位置
        n = 1
        while(n < 10):
            for i in range(5, 2, -1):
                for j in range(1, 4):
                    layout.addWidget(self.numButtons[n], i, j)
                    n += 1
        layout.addWidget(self.numButtons[0], 6, 1)

        # 内存按键布局
        layout.addWidget(self.mcButton, 3, 0)
        layout.addWidget(self.mrButton, 4, 0)
        layout.addWidget(self.msButton, 5, 0)
        layout.addWidget(self.mplusButton, 6, 0)

        # 运输符号布局
        layout.addWidget(self.plusButton, 3, 4)
        layout.addWidget(self.minusButton, 4, 4)
        layout.addWidget(self.timesButton, 5, 4)
        layout.addWidget(self.divButton, 6, 4)
        layout.addWidget(self.pointButton, 6, 2)
        layout.addWidget(self.changeSignButton, 6, 3)
        layout.addWidget(self.equalButton, 7, 4)

        # 计算器操作按键布局
        layout.addWidget(self.backspaceButton, 7, 0, 1, 2)
        layout.addWidget(self.clearButton, 7, 2, 1, 2)

        self.setLayout(layout)
        self.show()
    
    def str2num(self, strnum):
        """
        字符串转数字
        strnum：字符串型数值
        """
        numResult = int(strnum) if strnum.isdigit() else float(strnum)
        return numResult

    def numClicked(self):
        """
        单击数字和小数点后的操作
        """
        if len(self.lcdstring) < 9:
            self.lcdstring = self.lcdstring + self.sender().text()
            if self.lcdstring.startswith("."):
                self.lcdstring = "0" + self.lcdstring # 不允许.开头的数字，.表示0.
            elif len(self.lcdstring) >1 and self.lcdstring.startswith("0") and  not "." in self.lcdstring:
                self.lcdstring = self.lcdstring[1:] # 不允许有0开头的数字，除非是小数
            elif self.lcdstring.count('.') > 1:
                self.lcdstring = self.lcdstring[:-1] # 不允许在数字中出现多个.
            self.lcd.display(self.lcdstring)
            self.currentNum = self.str2num(self.lcdstring) 

    def opClicked(self):
        '''
        操作符
        '''
        self.previousNum = self.currentNum
        self.currentNum = 0
        self.lcdstring = ""
        self.operation = self.sender().text()

    def equalClicked(self):
        '''
        等于
        '''
        if self.operation == "+":  # 加法
            self.cresult = self.previousNum + self.currentNum
        elif self.operation == "-": # 减法
            self.cresult = self.previousNum - self.currentNum
        elif self.operation == u"\N{MULTIPLICATION SIGN}": # 乘法
            self.cresult = self.previousNum * self.currentNum
        elif self.operation == u"\N{DIVISION SIGN}" and self.currentNum != 0: # 除法，除数不能为0
            self.cresult = self.previousNum / self.currentNum
        elif self.operation == u"\N{DIVISION SIGN}" and self.currentNum == 0:
            self.cresult = "ERROR"

        self.lcd.display(self.cresult)
        if self.cresult != "ERROR":
            self.currentNum = self.cresult
        self.lcdstring = ""
        self.operation = ""

    def changeSignClicked(self):
        """
        改变正负数
        """
        if self.currentNum > 99999999:
            QMessageBox.information(self, "提示", "位数过多，负数无法显示")
        else:
            self.currentNum *= -1
            self.lcd.display(self.currentNum)

    def backspaceClicked(self):
        """
        后退
        """
        if len(self.lcdstring) > 1:
            self.lcdstring = self.lcdstring[:-1]
            self.lcd.display(self.lcdstring)
            self.currentNum = self.str2num(self.lcdstring)
        else:
            self.currentNum, self.lcdstring = 0, "0"
            self.lcd.display(self.lcdstring)

    def clear(self):
        '''
        全部清零
        '''
        self.lcdstring = ""
        self.currentNum = 0
        self.previousNum = 0
        self.cresult = 0
        self.lcd.display(0)
        self.clearMemory()

    def clearMemory(self):
        """
        清除暂存的数字
        """
        self.tmp = 0.0
        self.msButton.setChecked(False)
        self.msButton.setEnabled(True)

    def loadMemory(self):
        """
        载入暂存的数字
        """
        self.lcd.display(self.tmp)
        self.currentNum = self.tmp
        self.lcdstring = ""

    def setMemory(self, checked):
        """
        存入待暂存的数字
        checked：判断是否选中
        """
        if checked:
            self.tmp = self.currentNum
            self.msButton.setEnabled(False)

    def addToMemory(self):
        """
        与暂存的数字累加
        """
        self.previousNum = self.tmp
        self.operation = "+"

    def createButton(self, text, function):
        """
        创建一个按钮
        text：按钮上的字符
        function：关联的槽
        """
        button = Button(text)
        button.clicked.connect(function)
        return button
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    sys.exit(app.exec())