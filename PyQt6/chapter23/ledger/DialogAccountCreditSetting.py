#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogAccountBankSetting.py
@Time    :   2024/01/30 08:58:18
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt6.QtWidgets import QDialog, QInputDialog, QMessageBox
from datamanagement import AccountManagement
from Ui_DialogAccountCreditSetting import Ui_Dialog

# 信用卡设置

class DialogAccountCreditSettingFunction(QDialog, Ui_Dialog):

    creditaccountSignal = pyqtSignal(str ,str) # 信用卡信息信号

    def __init__(self, isMS, parent=None):
        super().__init__(parent)
        self.isMS = isMS # 判断是修改还是设置信用卡
        self.credit = "" # 信用卡银行
        self.creditid = "" # 信用卡银行ID
        self.setupUi(self)
        self.initData()

    def initData(self):
        """
        数据初始化
        """
        if self.isMS == 1:
            self.setWindowTitle("修改信用卡信息")
        bankList = []
        self.accountM = AccountManagement()
        banks = self.accountM.loadAllBanks()
        for bankItem in banks:
            bankList.append(bankItem[0])
        bankList.append("其他银行")
        self.comboBox_Credit.addItems(bankList)

    def setCreditInfo(self, credit, creditID):
        """
        credit：信用卡信息
        creditID：信用卡后四位
        """
        self.credit = credit.replace("信用卡", "")
        self.creditid = creditID
        self.comboBox_Credit.setCurrentText(self.credit)
        self.lineEdit_CreditID.setText(self.creditid)

    @pyqtSlot(str)
    def on_comboBox_Credit_textActivated(self, text):
        """
        信用卡发行行
        """
        if text == "其他银行":
            isok = QInputDialog.getText(self, "银行名称", "填写银行的名称")
            if isok[1]: 
                bankText = isok[0] # 银行名称
                if self.comboBox_Credit.findText(bankText, Qt.MatchFlag.MatchExactly) != -1:
                    QMessageBox.information(self, "提示", "不要输入重复的银行名称！")
                    self.comboBox_Credit.setCurrentIndex(0)
                else:
                    if bankText: # 设置新银行插入的位置
                        index = self.comboBox_Credit.count()-1
                        self.comboBox_Credit.insertItem(index, bankText)
                        self.comboBox_Credit.setCurrentText(bankText)
                    else: # 未输入银行名称
                        self.comboBox_Credit.setCurrentIndex(0)
            else: # 单击“取消”按钮
                self.comboBox_Credit.setCurrentIndex(0)

    @pyqtSlot()
    def on_pushButton_credit_ok_clicked(self):
        """
        添加信用卡
        """
        bankID = self.lineEdit_CreditID.text() # 银行卡后4位
        if 0 < len(bankID) < 4:
            QMessageBox.information(self, "提示", "卡号后4位长度不够！")
        elif not bankID:
            QMessageBox.information(self, "提示", "卡号后4位没有填写！")
        else:
            bank = self.comboBox_Credit.currentText()
            subaccountCredit = f"{bank}信用卡（{bankID}）"
            if self.isMS == 0: # 新增信用卡
                isok = self.accountM.addSubAccount(subaccountCredit, "信用卡")
                if isok == "existed":
                    QMessageBox.warning(self, "警告", "有重复的信用卡！")
                elif isok == "success":
                    self.creditaccountSignal.emit(subaccountCredit, "信用卡")
                    self.accept()
                elif isok == "execut_subaccount_error":
                    QMessageBox.warning(self, "警告", "信用卡添加失败！")
            else: # 修改信用卡
                oldsubaccountCredit = f"{self.credit}（{self.creditid}）"
                if subaccountCredit != oldsubaccountCredit:
                    self.creditaccountSignal.emit(subaccountCredit, "信用卡")
                self.accept()