#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   calculation.py
@Time    :   2023/04/11 18:59:48
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox

# 四则运算小游戏

class Calculation(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def createCalculation(self):
        """
        生成随机算式
        """
        num = "123456789"
        op = ["+", "-", "*", "//"]  # 随机运算符
        formula = random.choice(num) + random.choice(op) + random.choice(num)
        return formula, eval(formula)  # 返回算式和计算结果
    
    def refresh(self):
        """
        刷新算式
        """
        newFormula, self.result = self.createCalculation()
        self.lb.setText(f"请计算 {newFormula} 的结果是多少（除法是整除）？")  # 重新生成新的算式
    
    def initUI(self):
        """
        构建UI
        """
        self.resize(400, 300)  # 窗体尺寸
        self.setWindowTitle("微信公众号：学点编程吧--四则运算")  # 标题
        self.lb = QLabel(self)  # 显示算式
        self.lb.move(90, 50)
        self.inputLine = QLineEdit(self)  # 输入算式结果
        self.inputLine.move(130, 90)
        pb = QPushButton("确定", self)
        pb.move(160, 130)
        pb.clicked.connect(self.getResult)  # 点击确定按钮判断答案是否正确
        self.refresh()
        self.show()

    def getResult(self):
        """
        比较答案
        """
        calculationResult = self.inputLine.text()
        if str(self.result) == calculationResult:
            QMessageBox.information(self, "提示", "答案正确！")
            self.refresh()
            self.inputLine.clear()  # 输入的数字清除

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ca = Calculation()
    sys.exit(app.exec())

