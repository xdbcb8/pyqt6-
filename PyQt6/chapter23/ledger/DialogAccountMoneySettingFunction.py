#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogAccountMoneySettingFunction.py
@Time    :   2024/02/01 12:58:00
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt6.QtWidgets import QDialog, QInputDialog, QMessageBox
from Ui_DialogAccountMoneySetting import Ui_Dialog
from datamanagement import AccountManagement

# 现金账户设置

class DialogAccountMoneySettingFunction(QDialog, Ui_Dialog):

    moneySignal = pyqtSignal(str, str) # 现金账户信号

    def __init__(self, isMS, parent=None):
        super().__init__(parent)
        self.isMS = isMS # 判断是修改还是设置现金账户
        self.money = "" # 币种名称
        self.moneyAccountName = "" # 现金账户名称
        self.setupUi(self)
        if self.isMS == 1:
            self.setWindowTitle("修改现金账户信息")

    def setMoneyInfo(self, money, moneyaccount):
        """
        money：币种信息
        moneyaccount：现金账户名称
        """
        self.money = money
        self.moneyAccountName = moneyaccount
        self.comboBox_Money.setCurrentText(money)
        self.lineEdit_money.setText(moneyaccount)     

    @pyqtSlot(str)
    def on_comboBox_Money_textActivated(self, text):
        """
        选择币种
        """
        if text == "其他币种":
            moneyD = QInputDialog.getText(self, "选择币种", "输入一个现金币种！")
            if moneyD[1]:
                money = moneyD[0] # 币种名称
                if self.comboBox_Money.findText(money, Qt.MatchFlag.MatchExactly) != -1:
                    QMessageBox.information(self, "提示", "不要输入重复的币种名称！")
                    self.comboBox_Money.setCurrentIndex(0)
                else:
                    if money: # 币种不能为空
                        index = self.comboBox_Money.count()-1
                        self.comboBox_Money.insertItem(index, money)
                        self.comboBox_Money.setCurrentText(money)
                    else: # 未输入币种名称
                        self.comboBox_Money.setCurrentIndex(0)
            else: # 单击“取消”按钮
                self.comboBox_Money.setCurrentIndex(0)

    @pyqtSlot()
    def on_pushButton_Money_ok_clicked(self):
        """
        添加现金账户
        """
        moneyAccountName = self.lineEdit_money.text() # 现金账户名称
        if not moneyAccountName:
            QMessageBox.information(self, "提示", "现金账户名称为空！")
        else:
            money = self.comboBox_Money.currentText() # 币种
            subaccountmoney = f"{money}（{moneyAccountName}）"
            if self.isMS == 0: # 新增现金账户
                accountM = AccountManagement()
                isok = accountM.addSubAccount(subaccountmoney, "现金账户")
                if isok == "existed":
                    QMessageBox.warning(self, "警告", "有重复的现金账户！")
                elif isok == "success":
                    self.moneySignal.emit(subaccountmoney, "现金账户")
                    self.accept()
                elif isok == "execut_subaccount_error":
                    QMessageBox.warning(self, "警告", "现金账户添加失败！")
            else: # 修改现金账户
                oldmoneysubaccount = f"{self.money}（{self.moneyAccountName}）"
                if subaccountmoney != oldmoneysubaccount:
                    self.moneySignal.emit(subaccountmoney, "现金账户")
                self.accept()