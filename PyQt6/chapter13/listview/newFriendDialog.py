#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   newFriendDialog.py
@Time    :   2023/08/13 12:51:22
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第13章第1节QListView--新增好友对话框

import os
import codecs
import random
from PyQt6.QtWidgets import (QDialog, QDialogButtonBox, QGridLayout, QLineEdit, QRadioButton, 
                             QPushButton, QLabel, QFileDialog, QGroupBox)
from PyQt6.QtCore import pyqtSignal

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class NewFriend(QDialog):
    friendItem = pyqtSignal(str, str) # 传递新好友名称和头像路径的信号
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.frineName = "" # 好友名称
        self.iconpath = "" # 头像路径
        self.initUI()
        self.loadrandomNamePic()

    def initUI(self):
        self.setWindowTitle("新增好友")
        group1 = QGroupBox(self)
        group1.setTitle("好友名称")
        self.radio1 = QRadioButton("随机名称", group1)
        self.radio1.setChecked(True)
        self.radio2 = QRadioButton("自定义名称", group1)
        self.newFriendName = QLineEdit(group1)
        self.newFriendName.setClearButtonEnabled(True)
        self.newFriendName.setEnabled(False)
        group2 = QGroupBox(self)
        group2.setTitle("头像选择")
        self.radio3 = QRadioButton("默认", group2)
        self.radio3.setChecked(True)
        self.radio4 = QRadioButton("选择图标", group2)
        self.button = QPushButton("浏览", group2)
        self.button.setEnabled(False)
        buttonbox = QDialogButtonBox(self)
        OKButton = buttonbox.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        CancelButton = buttonbox.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)

        # 好友名称布局
        grouplayout1 = QGridLayout(group1)
        grouplayout1.addWidget(self.radio1, 0, 0)
        grouplayout1.addWidget(self.radio2, 0, 1)
        grouplayout1.addWidget(self.newFriendName, 1, 0, 1, 2)
        group1.setLayout(grouplayout1)
        # 好友头像布局
        grouplayout2 = QGridLayout(group2)
        grouplayout2.addWidget(QLabel("好友图标（建议不要超过70*70像素）"), 0, 0, 1, 3)
        grouplayout2.addWidget(self.radio3, 1, 0)
        grouplayout2.addWidget(self.radio4, 1, 1)
        grouplayout2.addWidget(self.button, 1, 2)
        group2.setLayout(grouplayout2)
        # 总体布局
        layout = QGridLayout(self)
        layout.addWidget(group1, 0, 0, 3, 3)
        layout.addWidget(group2, 4, 0, 3, 3)
        layout.addWidget(buttonbox, 7, 1, 1, 2)
        self.setLayout(layout)

        # 信号与槽连接
        self.radio1.clicked.connect(self.setLineEdit)
        self.radio2.clicked.connect(self.setLineEdit)
        self.radio3.clicked.connect(self.setButton)
        self.radio4.clicked.connect(self.setButton)
        self.button.clicked.connect(self.getIcon)
        OKButton.clicked.connect(self.addNewFriend)
        CancelButton.clicked.connect(self.reject)
        self.newFriendName.editingFinished.connect(self.setdiyName)

    def setdiyName(self):
        """
        设置好友名称为用户自定义名称
        """
        if self.newFriendName.text():
            self.frineName = self.newFriendName.text()

    def loadrandomNamePic(self):
        """
        载入好友名称和头像
        """
        with codecs.open(f"{current_dir}\\qqres\\name.txt", "r", "utf-8") as f:
            nameList = f.read().split("\r\n")
            self.frineName = random.choice(nameList) # 随机姓名
            self.iconpath = f"{current_dir}\\qqres\\{self.frineName[0]}.png" # 随机姓名对应的头像

    def setLineEdit(self):
        """
        好友名称设置为随机或者自定义
        """
        if self.sender() == self.radio1:
            self.newFriendName.setEnabled(False)
            self.newFriendName.clear()
            self.loadrandomNamePic()
        else:
            self.newFriendName.setEnabled(True)

    def setButton(self):
        """
        头像设置为随机或自定义
        """
        if self.sender() == self.radio3:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def getIcon(self):
        """
        手动选择头像
        """
        fname = QFileDialog.getOpenFileName(self, "打开文件", "./", "图片文件 (*.png *.jpg)")
        if fname[0]:
            self.iconpath = fname[0]

    def addNewFriend(self):
        """
        向主窗体发送新增好友信号
        """
        if all([self.frineName, self.iconpath]):
            self.friendItem.emit(self.frineName, self.iconpath)
            self.accept()