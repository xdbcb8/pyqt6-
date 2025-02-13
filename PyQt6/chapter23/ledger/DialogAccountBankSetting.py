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
from Ui_DialogAccountBankSetting import Ui_Dialog
from datamanagement import AccountManagement

# 储蓄卡设置

class DialogAccountBankSettingFunction(QDialog, Ui_Dialog):
    
    bankaccountSignal = pyqtSignal(str ,str) # 储蓄卡信息信号

    def __init__(self, isMS, parent=None):
        super().__init__(parent)
        self.isMS = isMS # 判断是修改还是设置储蓄卡，1是修改，0是新增
        self.bank = "" # 储蓄卡银行
        self.bankid = "" # 储蓄卡银行ID
        self.setupUi(self)
        self.initData()

    def initData(self):
        if self.isMS == 1:
            self.setWindowTitle("修改储蓄卡信息")
        bankList = [] # 临时存储银行信息
        self.accountM = AccountManagement()
        banks = self.accountM.loadAllBanks()
        for bankItem in banks:
            bankList.append(bankItem[0])
        bankList.append("其他银行")
        self.comboBox_bank.addItems(bankList)

    def setBankInfo(self, bank, bankID):
        """
        bank：银行卡信息
        bankID：银行卡后四位
        """
        self.bank = bank
        self.bankid = bankID
        self.comboBox_bank.setCurrentText(bank)
        self.lineEdit_bankID.setText(bankID)

    @pyqtSlot(str)
    def on_comboBox_bank_textActivated(self, text):
        """
        选择银行
        """
        if text == "其他银行":
            isok = QInputDialog.getText(self, "银行名称", "填写银行的名称")
            if isok[1]:
                bankText = isok[0] # 银行名称
                if self.comboBox_bank.findText(bankText, Qt.MatchFlag.MatchExactly) != -1:
                    QMessageBox.information(self, "提示", "不要输入重复的银行名称！")
                    self.comboBox_bank.setCurrentIndex(0)
                else:
                    if bankText: # 设置新银行插入的位置
                        index = self.comboBox_bank.count()-1
                        self.comboBox_bank.insertItem(index, bankText)
                        self.comboBox_bank.setCurrentText(bankText)
                    else: # 未输入银行名称
                        self.comboBox_bank.setCurrentIndex(0)
            else: # 单击“取消”按钮
                self.comboBox_bank.setCurrentIndex(0)
    
    @pyqtSlot()
    def on_pushButton_bank_ok_clicked(self):
        """
        添加储蓄卡信息
        """
        bankID = self.lineEdit_bankID.text() # 银行卡后4位
        if 0 < len(bankID) < 4:
            QMessageBox.information(self, "提示", "卡号后4位长度不够！")
        elif not bankID:
            QMessageBox.information(self, "提示", "卡号后4位没有填写！")
        else:
            bank = self.comboBox_bank.currentText()
            if "银行" not in bank:
                bank = bank + "银行"
            subaccountBank = f"{bank}（{bankID}）" # 储蓄卡的信息
            if self.isMS == 0: # 新增储蓄卡
                isok = self.accountM.addSubAccount(subaccountBank, "金融账户")
                if isok == "existed":
                    QMessageBox.warning(self, "警告", "有重复的银行卡！")
                elif isok == "success":
                    self.bankaccountSignal.emit(subaccountBank, "金融账户")
                    self.accept()
                elif isok == "execut_subaccount_error":
                    QMessageBox.warning(self, "警告", "银行卡添加失败！")
            else: # 修改储蓄卡
                oldsubaccountBank = f"{self.bank}（{self.bankid}）"
                if subaccountBank != oldsubaccountBank:
                    self.bankaccountSignal.emit(subaccountBank, "金融账户")
                self.accept()