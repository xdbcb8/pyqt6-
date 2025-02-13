#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogPwdSettingFunction.py
@Time    :   2024/01/30 20:05:54
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog, QLineEdit, QMessageBox
from Ui_DialogPwdSetting import Ui_Dialog_pwd_setting
from datamanagement import PwdManagement

# 密码设置

class Dialog_pwd_settingFunction(QDialog, Ui_Dialog_pwd_setting):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pwdM = PwdManagement()
        self.pwd_old = self.pwdM.queryPwd() # 查询数据库中是否存有密码

    def settingPWD(self, PM, pwd):
        """
        设置密码
        """
        issettingok = PM.settingPwd(pwd)
        if issettingok == "success":
            QMessageBox.information(self, "提示", "密码修改成功！")
            self.accept()
        elif issettingok == "execut_pwd_error":
            QMessageBox.warning(self, "提示", "密码修改失败！")

    @pyqtSlot(bool)
    def on_checkBox_showPWD_clicked(self, checked):
        """
        密码显示明文
        """
        if checked:
            self.lineEdit_pwd_old.setEchoMode(QLineEdit.EchoMode.Normal)
            self.lineEdit_pwd_new.setEchoMode(QLineEdit.EchoMode.Normal)
            self.lineEdit_pwd_new2.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_pwd_old.setEchoMode(QLineEdit.EchoMode.Password)
            self.lineEdit_pwd_new.setEchoMode(QLineEdit.EchoMode.Password)
            self.lineEdit_pwd_new2.setEchoMode(QLineEdit.EchoMode.Password)

    @pyqtSlot()
    def on_pushButton_ok_clicked(self):
        """
        设置密码
        """
        oldpwd = self.lineEdit_pwd_old.text() # 旧密码
        newpwd = self.lineEdit_pwd_new.text() # 新密码
        newpwd2 = self.lineEdit_pwd_new2.text() # 新密码确认
        if self.pwd_old and (not oldpwd):
            QMessageBox.information(self, "提示", "请输入旧密码！")
        else:
            if newpwd != newpwd2 or not all([newpwd, newpwd2]):
                QMessageBox.information(self, "提示", "新密码两次密码不一致或存在为空的情况！")
            elif not self.pwd_old: # 原密码为空的情况
                self.settingPWD(self.pwdM, newpwd)
            else:
                isok = self.pwdM.comparePwd(oldpwd)
                if not isok:
                    QMessageBox.warning(self, "提示", "旧密码不正确！")
                else:
                    self.settingPWD(self.pwdM, newpwd)