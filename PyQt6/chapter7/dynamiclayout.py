#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dynamiclayout.py
@Time    :   2023/06/13 16:02:58
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 简单的表单

import sys
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QWidget, QApplication, QFormLayout, QLineEdit, QTextEdit,
                             QComboBox, QVBoxLayout, QDialog, QDialogButtonBox,
                             QPushButton, QGroupBox, QRadioButton, QCheckBox)

class InputDialog(QDialog):

    propertyNameSignal = pyqtSignal(str, int) # 单行或多行信息发送的信号
    propertyOpSignal = pyqtSignal(list, int) # 单选或多选发送的信号

    def __init__(self, flag, Parent=None):
        super().__init__(Parent)
        self.flag = flag # 用户选择添加的控件类型
        self.dataOp = [] # 暂存选项内容
        self.initUi()

    def initUi(self):
        """
        对话框界面初始化
        """
        self.layout = QFormLayout(self) # 表格布局
        self.lineEdit = QLineEdit("")
        self.layout.addRow("属性名称(&N)", self.lineEdit)
        if self.flag == 0:
            self.setWindowTitle("单行文本框输入")
        elif self.flag == 1:
            self.setWindowTitle("多行文本框输入")
        elif self.flag == 2:
            self.setWindowTitle("设置单选按钮")
        elif self.flag == 3:
            self.setWindowTitle("设置多选框")
        if self.flag in [2, 3]:
            btn = QPushButton("增加选项", self)
            btn.clicked.connect(self.addOp)
            self.layout.addWidget(btn)
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel) # 增加OK和取消按钮
        self.layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.getInfo)
        buttonBox.rejected.connect(self.reject) # 对话框中的取消

    def addOp(self):
        """
        新增选项
        """
        newLineop = QLineEdit(self)
        newLineop.setFocus() # 设置焦点
        self.dataOp.append(newLineop)
        self.layout.insertRow(1, f"选项{len(self.dataOp)}", newLineop) # 新增一个选项

    def getInfo(self):
        """
        发送属性及选项
        """
        propertyName = self.lineEdit.text() # 获得该属性的名称
        if len(self.dataOp) > 0: # 表明用户生成了待选项
            opList = []
            for item in self.dataOp:
                opList.append(item.text())
            self.propertyOpSignal.emit([propertyName, opList], self.flag) # 将该行的名称和选项内容发射出去
        else: # 表明用户没有生成待选项
            self.propertyNameSignal.emit(propertyName, self.flag) # 将该行的名称发射出去
        self.accept() # 对话框中的接受

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        构造界面，用于实现对话框控件的布局
        """
        self.resize(400, 300)
        self.setWindowTitle("动态布局")
        self.combox = QComboBox(self)
        self.combox.addItems(["", "单行文本框", "多行文本框", "单选按钮", "多选框", "OK-Cancel按钮箱"])
        self.combox.activated.connect(self.createDialog)
        layout = QVBoxLayout(self)
        layout.addWidget(self.combox)
        self.formLayout = QFormLayout()
        layout.addLayout(self.formLayout)
        self.setLayout(layout)
        self.show()

    def textInputDialog(self, flag):
        """
        单行文本框/多行文本框
        flag：0就是单行文本框，否则就是多行文本框
        """
        inputDialog = InputDialog(flag, self)
        if flag in [0, 1]:
            inputDialog.propertyNameSignal.connect(self.setTextInput) # 单行或多行
        else:
            inputDialog.propertyOpSignal.connect(self.setTextInput) # 单选或多选
        inputDialog.exec()

    def setTextInput(self, info, flag):
        """
        根据类型创建单行或者多行输入
        info：表示传递过来的信息。单行或多行的，info是字符型，代表该行的名称。单选或多选，info是列表，传递第0项代表该行的名称，第1项代表选项内容列表。
        flag=0：单行输入标志
        flag=1：多行输入标志
        flag=2：单选标志
        flag=3：多选标志
        """
        if flag == 0:
            lineInput = QLineEdit(self)
            self.formLayout.addRow(info, lineInput)
        elif flag == 1:
            textInput = QTextEdit(self)
            self.formLayout.addRow(info, textInput)
        elif flag == 2:
            propertyName = info[0]
            group1 = QGroupBox(self) # 将单选项组成作为一组
            vbox = QVBoxLayout()
            for itemradio in info[1]:
                radio = QRadioButton(itemradio, self)
                vbox.addWidget(radio)
            group1.setLayout(vbox)
            self.formLayout.addRow(propertyName, group1)
        elif flag == 3:
            propertyName = info[0]
            group2 = QGroupBox(self) # 将多选项组成作为一组
            vbox = QVBoxLayout()
            for itemcheck in info[1]:
                check = QCheckBox(itemcheck, self)
                vbox.addWidget(check)
            group2.setLayout(vbox)
            self.formLayout.addRow(propertyName, group2)

    def createDialog(self, index):
        """
        根据选项创建对话框
        """
        if index == 1: # 选择单行输入
            self.textInputDialog(0)
        elif index == 2: # 选择多行输入
            self.textInputDialog(1)
        elif index == 3: # 选择单选
            self.textInputDialog(2)
        elif index == 4: # 选择多选
            self.textInputDialog(3)
        elif index == 5: # 选择OK-Cancel按钮箱
            self.combox.setEnabled(False) # 下拉框禁用，不能再选了
            buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            self.formLayout.addWidget(buttonBox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    app.exit(app.exec())