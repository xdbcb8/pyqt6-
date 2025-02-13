#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogPwd.py
@Time    :   2024/02/24 11:46:00
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog, QLineEdit, QMessageBox
from Ui_DialogPwd import Ui_Dialog_pwd
from datamanagement import PwdManagement
from main import MainWindowFunction

# 登录

class Dialog_pwd(QDialog, Ui_Dialog_pwd):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pwdM = PwdManagement()
        self.initData()

    def initData(self):
        """
        数据初始化
        """
        self.pwd_old = self.pwdM.queryPwd() # 查询数据库中的密码

    def showMainWindowAndHideSelf(self):
        """
        显示主窗口
        """
        self.main = MainWindowFunction()  
        self.main.show()  
        self.hide() # 密码输入窗口隐藏

    @pyqtSlot(bool)
    def on_checkBox_showPWD_clicked(self, checked):
        """
        设置密码是可见
        checked：勾选密码可见
        """
        if checked:
            self.lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

    @pyqtSlot()
    def on_pushButton_ok_clicked(self):
        """
        登录
        """
        if not self.pwd_old: # 如果密码不存在
            self.showMainWindowAndHideSelf()
        else:
            pwd = self.lineEdit.text() # 输入的密码
            iscompare = self.pwdM.comparePwd(pwd) # 查询密码是否正确
            if not iscompare:
                QMessageBox.information(self, "提示", "密码不正确！")
            else:
                self.showMainWindowAndHideSelf()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()