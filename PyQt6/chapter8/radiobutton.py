#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   radiobutton.py
@Time    :   2023/06/29 06:53:35
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
"""
# QRadioButton简单举例

import sys
from PyQt6.QtWidgets import QWidget, QRadioButton, QApplication, QPushButton, QMessageBox, QButtonGroup, QGridLayout, QVBoxLayout, QSizePolicy

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.resize(320, 180)
        self.setWindowTitle("单选按钮")
        rb11 = QRadioButton("你是", self)
        rb12 = QRadioButton("我是", self)
        rb13 = QRadioButton("他是", self)
        rb21 = QRadioButton("苹果", self)
        rb22 = QRadioButton("桔子", self)
        rb23 = QRadioButton("香蕉", self)
        
        bt1 = QPushButton("提交", self)
        bt1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed) # 按钮尺寸限制住
        
        #单选按钮组1，后面的数字是按钮组id
        self.bg1 = QButtonGroup(self)
        self.bg1.addButton(rb11, 11)
        self.bg1.addButton(rb12, 12)
        self.bg1.addButton(rb13, 13)
        
        #单选按钮组2
        self.bg2 = QButtonGroup(self)
        self.bg2.addButton(rb21, 21)
        self.bg2.addButton(rb22, 22)
        self.bg2.addButton(rb23, 23)
        
        # 布局
        vlayout1 = QVBoxLayout()
        vlayout1.addWidget(rb11)
        vlayout1.addWidget(rb12)
        vlayout1.addWidget(rb13)

        vlayout2 = QVBoxLayout()
        vlayout2.addWidget(rb21)
        vlayout2.addWidget(rb22)
        vlayout2.addWidget(rb23)

        layout = QGridLayout(self)
        layout.addLayout(vlayout1, 0, 0)
        layout.addLayout(vlayout2, 0, 1)
        layout.addWidget(bt1, 1, 0)
        self.setLayout(layout)

        # 相关信息
        self.info1 = ""
        self.info2 = ""
        
        self.bg1.buttonClicked.connect(self.rbclicked)
        self.bg2.buttonClicked.connect(self.rbclicked)

        bt1.clicked.connect(self.submit)
        
        self.show()
        
    def submit(self):
        """
        提交
        """
        if self.info1 == "" or self.info2 == "":
            QMessageBox.information(self, "What?", "还有选项尚未选择，赶快选择一个吧！")
        else:
            QMessageBox.information(self, "What?", self.info1 + self.info2)

    def rbclicked(self):
        """
        将单选组1（self.bg1）和单选组2（self.bg2）中的各选择一个将值赋给self.info1和self.info2
        """
        sender = self.sender()
        if sender == self.bg1:
            if self.bg1.checkedId() == 11: # 若按钮组的id为11，self.info1赋值为“你是”，下同
                self.info1 = "你是"
            elif self.bg1.checkedId() == 12:
                self.info1 = "我是"
            elif self.bg1.checkedId() == 13:
                self.info1 = "他是"
            else:
                self.info1 = ""
        else:
            if self.bg2.checkedId() == 21:
                self.info2 = "苹果"
            elif self.bg2.checkedId() == 22:
                self.info2 = "桔子"
            elif self.bg2.checkedId() == 23:
                self.info2 = "香蕉"
            else:
                self.info2 = ""
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())