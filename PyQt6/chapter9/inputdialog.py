#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   inputdialog.py
@Time    :   2023/07/13 12:45:47
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第9章第5节QInputDialog

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QInputDialog, QLabel, QToolButton, QGridLayout, QTextBrowser

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 370)
        self.setWindowTitle("QInputDialog举例")
        name = QLabel("姓名：", self)
        sex = QLabel("性别：", self)
        age = QLabel("年龄：", self)
        height = QLabel("身高（单位：米）：", self)
        resume = QLabel("个人简介：", self)
        self.nameL = QLabel(self)
        self.ageL = QLabel(self)
        self.sexL = QLabel(self)
        self.heightL = QLabel(self)
        self.resumeT = QTextBrowser(self)
        nameButton = QToolButton(self)
        nameButton.setText("...")
        ageButton = QToolButton(self)
        ageButton.setText("...")
        sexButton = QToolButton(self)
        sexButton.setText("...")
        heightButton = QToolButton(self)
        heightButton.setText("...")
        resumeButton = QToolButton(self)
        resumeButton.setText("...")

        layout = QGridLayout(self)
        layout.addWidget(name, 0, 0)
        layout.addWidget(self.nameL, 0, 1)
        layout.addWidget(nameButton, 0, 2)
        layout.addWidget(sex, 1, 0)
        layout.addWidget(self.sexL, 1, 1)
        layout.addWidget(sexButton, 1, 2)
        layout.addWidget(age, 2, 0)
        layout.addWidget(self.ageL, 2, 1)
        layout.addWidget(ageButton, 2, 2)
        layout.addWidget(height, 3, 0)
        layout.addWidget(self.heightL, 3, 1)
        layout.addWidget(heightButton, 3, 2)
        layout.addWidget(resume, 4, 0)
        layout.addWidget(self.resumeT, 4, 1)
        layout.addWidget(resumeButton, 4, 2)
        self.setLayout(layout)
        self.show()

        nameButton.clicked.connect(self.doActionName)
        sexButton.clicked.connect(self.doActionSex)
        ageButton.clicked.connect(self.doActionAge)
        heightButton.clicked.connect(self.doActionHeight)
        resumeButton.clicked.connect(self.doActionResume)

    def doActionName(self):
        """
        获取用户输入的文本
        """
        name, ok = QInputDialog.getText(self, "QInputDialog.getText()", "姓名：", text="在这里输入你的姓名")
        if ok:
            self.nameL.setText(name)

    def doActionSex(self):
        """
        获取用户选择的选项
        """
        sex, ok = QInputDialog.getItem(self, "QInputDialog.getItem()", "性别：", ['男', '女'], current=1)
        if ok:
            self.sexL.setText(sex)

    def doActionAge(self):
        """
        获取用户输入的整数
        """
        age, ok = QInputDialog.getInt(self, "QInputDialog.getInt()", "年龄：", 10, 8, 20, step=1)
        if ok:
            self.ageL.setText(f"{age}")

    def doActionHeight(self):
        """
        获取用户输入的小数
        """
        height, ok = QInputDialog.getDouble(self, "QInputDialog.getDouble()", "身高（单位：米）", 1.3, 1.1, 2.0, 1, step=0.1)
        if ok:
            self.heightL.setText(f"{height:.1f}") # 保留1位小数

    def doActionResume(self):
        """
        获取用户输入的Markdown文本
        """
        resume, ok = QInputDialog.getMultiLineText(self, "QInputDialog.getMultiLineText()", "个人简历", "在这里写上自己的个人简介")
        if ok:
            self.resumeT.setMarkdown(resume) # 支持通用部分Markdown语法

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())

# 示例Markdown文本(不含""")
"""
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
- 列表一
- 列表二
- 列表三
---
*这是斜体*

**粗体**
"""
