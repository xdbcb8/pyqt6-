#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   wizard.py
@Time    :   2023/07/15 15:03:45
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第9章第8节QWizard

import sys
import os
from PyQt6.QtWidgets import QApplication, QWizard, QWizardPage, QVBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QGridLayout, QMessageBox
from PyQt6.QtGui import QPixmap

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class FirstPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("这是第一页的标题(1/3)") # 标题
        self.setSubTitle("这是第一页的子标题……") # 子标题
        labelName = QLabel("请输入姓名*：", self)
        self.nameLineEdit = QLineEdit(self)
        self.labelnickName = QLabel("请输入昵称*：", self)
        self.nicknameLineEdit = QLineEdit(self)
        # 布局
        layout = QGridLayout(self)
        layout.addWidget(labelName, 0, 0)
        layout.addWidget(self.nameLineEdit, 0, 1)
        layout.addWidget(self.labelnickName, 1, 0)
        layout.addWidget(self.nicknameLineEdit, 1, 1)
        self.setLayout(layout)
        # 将姓名和昵称保存，方便读取
        self.registerField("Name", self.nameLineEdit)
        self.registerField("nickName*", self.nicknameLineEdit) # 昵称为必填项，否则“下一步”按钮不可用，注意参数中的*号

    def validatePage(self):
        """
        这里做一个姓名填写的验证，不填写，无法到第二个页面
        和昵称其实都是必填项，但是做了两种不同的校验方式
        """
        name = self.nameLineEdit.text()
        if name.strip() == "":
            self.setSubTitle("姓名不能为空")
            return False
        else:
            return True

class SecondPage(QWizardPage):
    def __init__(self):
        super().__init__()

        self.setTitle("这是第二页的标题(2/3)")
        self.setSubTitle("这是第二页的子标题……")
        layout = QVBoxLayout(self)
        label = QLabel("填写你的性别：")
        sex = QComboBox(self)
        sex.addItems(['男', '女'])
        layout.addWidget(label)
        layout.addWidget(sex)
        self.setLayout(layout)

        self.registerField("sex", sex, "currentText", sex.currentTextChanged) # 将下拉框当前选项的文本保存到sex的field中，不这么写默认是下拉框当前选项的索引

class ThirdPage(QWizardPage):
    def __init__(self):
        super().__init__()

        self.setTitle("这是第三页的标题(3/3)")
        self.setSubTitle("这是第三页的子标题……")
        layout = QVBoxLayout(self)
        label = QLabel("填写年龄：")
        age = QSpinBox(self)
        age.setRange(10, 20)
        layout.addWidget(label)
        layout.addWidget(age)
        self.setLayout(layout)

        self.registerField("age", age) # 保存年龄age的

class MyWizard(QWizard):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("简单向导")
        # 引导对话框样式
        self.setWizardStyle(QWizard.WizardStyle.ClassicStyle) # 经典样式，我只有win电脑，有苹果电脑的可以试试其他样式
        self.setPixmap(QWizard.WizardPixmap.LogoPixmap, QPixmap(f"{current_dir}\logo.png")) # Logo
        self.setPixmap(QWizard.WizardPixmap.WatermarkPixmap, QPixmap(f"{current_dir}\water.png")) # 水印
        # 不在起始页显示“上一步”按钮，显示“帮助”按钮，水印图一直向下扩展到窗口边缘
        self.setOption(QWizard.WizardOption.NoBackButtonOnStartPage | QWizard.WizardOption.HaveHelpButton | QWizard.WizardOption.ExtendedWatermarkPixmap)
        # 给几个按钮加上中文
        self.setButtonText(QWizard.WizardButton.BackButton, "上一步")
        self.setButtonText(QWizard.WizardButton.NextButton, "下一步")
        self.setButtonText(QWizard.WizardButton.CancelButton, "取消")
        self.setButtonText(QWizard.WizardButton.HelpButton, "帮助")
        self.setButtonText(QWizard.WizardButton.FinishButton, "完成")
        # 增加页面
        page1 = FirstPage()
        page2 = SecondPage()
        page3 = ThirdPage()
        self.addPage(page1)
        self.addPage(page2)
        self.addPage(page3)
        self.show()
        # 单击帮助按钮
        self.helpRequested.connect(self.getHelp)

    def getHelp(self):
        """
        模拟获得帮助
        """
        QMessageBox.information(self, "提示", "这是帮助文档！")

    def accept(self):
        """
        单击“完成”按钮后，将全部页面填写的字段用消息对话框展示出来
        """
        text = f'姓名：{self.field("Name")}\n昵称：{self.field("nickName")}\n性别：{self.field("sex")}\n年龄：{self.field("age")}岁'
        QMessageBox.information(self, "结果", text)
        super().accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWizard()
    sys.exit(app.exec())