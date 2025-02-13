#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   qqmock.py
@Time    :   2023/06/26 19:00:59
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# QQ登录模拟

import sys
import os
import random
from PyQt6.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout, QFormLayout, QApplication, QToolButton, 
                             QDialog, QMessageBox, QLineEdit, QDialogButtonBox, QListWidget, QListWidgetItem, QComboBox)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QEvent, pyqtSignal

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class DialogAddUser(QDialog):
    """自定义新增联系人对话框"""
    newUserSignal = pyqtSignal(str, str, str) # 新用户的信号
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.initUI()

    def initUI(self):
        self.iconpath = "default.png"
        self.qq = str(random.randint(33333333, 88888888)) # 随机QQ号
    
        self.resize(200, 100)
        self.setWindowTitle("新增用户")
        self.nameLine = QLineEdit(self)
        layout = QFormLayout(self)
        layout.addRow("新用户名(&N)", self.nameLine)
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel) # 增加ok和Cancel按钮
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        buttonBox.accepted.connect(self.AddNew)
        buttonBox.rejected.connect(self.reject) # 对话框中的取消

    def AddNew(self):
        """
        新增用户
        """
        self.username = self.nameLine.text() # 新用户名
        if self.username == "":
            QMessageBox.warning(self, "警告", "联系人姓名为空")
            self.nameLine.setFocus()
        else:
            if 'A' <= self.username[0].upper() <= 'Z':
                self.iconpath = self.username[0].upper() + ".png" # 选择的头像是根据用户名首字母确定的
            self.newUserSignal.emit(self.qq, self.username, self.iconpath)
            self.accept()

class ComboBoxItem(QWidget):
    '''下拉框每个小部件'''
    itemOpSignal = pyqtSignal(str) # 自定义str信号

    def __init__(self, qq, username, user_icon):
        '''
        一些初始设置
        '''
        super().__init__()
        self.username = username # 用户名
        self.qq = qq # QQ号
        self.user_icon = user_icon # 头像
        self.initUi()

    def initUi(self):
        '''
        界面初始设置
        '''
        lb_username = QLabel(self.username, self)
        lb_qq = QLabel(self.qq, self)
        lb_icon = QLabel(self)
        lb_icon.setPixmap(QPixmap(f"{current_dir}\\qqres\\{self.user_icon}"))
        self.bt_close = QToolButton(self)
        self.bt_close.setIcon(QIcon(f"{current_dir}\\qqres\\close.ico"))
        self.bt_close.setAutoRaise(True)

        vlayout = QVBoxLayout()
        vlayout.addWidget(lb_username)
        vlayout.addWidget(lb_qq)

        hlayout = QHBoxLayout()
        hlayout.addWidget(lb_icon)
        hlayout.addLayout(vlayout)
        hlayout.addStretch(1)
        hlayout.addWidget(self.bt_close)
        hlayout.setContentsMargins(5, 5, 5, 5)  # 设置要在布局周围使用的边距。
        hlayout.setSpacing(5) # 此属性保存布局内的窗口小部件之间的间距

        self.setLayout(hlayout)

        self.bt_close.installEventFilter(self)
        self.installEventFilter(self) # 为bt_close按钮和ComboBoxItem自身安装事件过滤器

    def eventFilter(self, object, event):
        '''
        事件过滤器
        '''
        if object is self:
            if event.type() == QEvent.Type.Enter:
                self.setStyleSheet("QWidget{color:white}") # 鼠标指针移出后用户名和账户呈现白色
            elif event.type() == QEvent.Type.Leave:
                self.setStyleSheet("QWidget{color:black}") # 鼠标指针移出后用户名和账户呈现黑色
            # 当我们把鼠标移入后颜色会变化哦
        elif object is self.bt_close:
            if event.type() == QEvent.Type.MouseButtonPress:  
                self.itemOpSignal.emit(self.qq) # 点击删除账号按钮，发出信号
        return super().eventFilter(object, event)

class ChooseUser(QDialog):
    """
    像QQ一样选择用户
    """

    def __init__(self):
        """
        一些初始设置
        """
        super().__init__()
        self.initUI()
        self.storage_qq = [] # 这个列表是存储每个联系人QQ号

    def initUI(self):
        self.resize(300, 200)
        self.setWindowTitle("模拟QQ选择登录用户")

        # 界面布局
        layout = QVBoxLayout(self)
        layout.addStretch(1)
        self.comboBox = QComboBox(self)
        self.comboBox.setEditable(True) # 可编辑
        self.comboBox.setInsertPolicy(QComboBox.InsertPolicy.NoInsert) # 不允许插入字符串
        self.comboBox.activated.connect(self.chooseQQ)
        self.button = QToolButton(self)
        self.button.setText("新增")
        self.button.clicked.connect(self.addNew)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.comboBox)
        hLayout.addWidget(self.button)
        layout.addLayout(hLayout)
        layout.addStretch(1)
        self.setLayout(layout)
        self.show()
        self.setmode()

    def setmode(self):
        '''
        设置模型
        '''
        self.setStyleSheet("""
            QComboBox QAbstractItemView::item{
            min-height: 60px;
            min-width: 60px;
            outline:0px;
            }
            """) # 这里设置了QComboBoxItem的尺寸
        self.listw = QListWidget()
        self.comboBox.setModel(self.listw.model())
        self.comboBox.setView(self.listw) # QListWidget设置为QComboBox的View，QListWidget的Model设置为QComboBox的Model
    
    def addNew(self):
        """
        新增用户
        """

        user = DialogAddUser(self) # 新增用户对话框
        user.newUserSignal.connect(self.getUserInfo)
        user.exec()

    def getUserInfo(self, qq, name, icon):
        """
        在QComboBox中显示新增加的用户
        """
        item = ComboBoxItem(qq, name, icon)
        item.itemOpSignal.connect(self.itemDel)
        self.storage_qq.append(qq)
        self.listwitem = QListWidgetItem(self.listw) # 用给定的父项(self.listw)构造指定类型的空列表项目

        self.listw.setItemWidget(self.listwitem, item) # 将小部件设置为在给定项目中显示。也就是将我们自定义的Item显示在self.listwitem中
    
    def itemDel(self, qq):
        """
        删除用户
        qq：用户的QQ号
        """
        indexqq = self.storage_qq.index(qq)
        # 根据得到的QQ号得到相应的索引，然后根据索引删除self.listw的项目
        self.listw.takeItem(indexqq)
        # storage_qq列表中存储的数据
        del self.storage_qq[indexqq]

    def chooseQQ(self, index):
        """
        将item的索引带过来，选择显示QQ号
        index：QQ账号的索引
        """
        qq = self.storage_qq[index]
        # 输入栏中显示选中的QQ号
        self.comboBox.setEditText(qq)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ChooseUser()
    sys.exit(app.exec())