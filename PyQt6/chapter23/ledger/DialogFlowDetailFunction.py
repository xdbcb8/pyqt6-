#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogFlowDetailFunction.py
@Time    :   2024/02/04 12:31:16
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, pyqtSignal, QDateTime
from PyQt6.QtWidgets import QDialog, QMessageBox
from Ui_DialogFlowDetail import Ui_Dialog
from DialogAccountFunction import Dialog_Account_Function
from DialogChargeClassificationFunction import DialogChargeClassificationFunction
from datamanagement import FlowFunds

# 流水详情

class DialogFlowDetailFunction(QDialog, Ui_Dialog):

    successSignal = pyqtSignal() # 流水更新成功的信号

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setupUi(self)
        self.id = "" # 流水id
        self.flag = "" # 收、支的标志
        self.flowfundsM = FlowFunds()
        self.subaccount = self.lineEdit_account.text()
        self.subclassification = self.lineEdit_classification.text()

    def setData(self, id, account, subaccount, classification, subclassification, money, beizhu, dateTime):
        """
        设置数据
        id：id编号
        account：一级账户
        subaccount：二级账户
        classification：一级分类
        subclassification：二级分类
        money：金额
        beizhu：备注
        dateTime：日期
        """
        if money > 0:
            self.flag = "in"
        else:
            self.flag = "out"
        self.doubleSpinBox_money.setValue(money)
        self.lineEdit_account.setText(f"{account}>{subaccount}")
        self.lineEdit_classification.setText(f"{classification}>{subclassification}")
        self.lineEdit_beizhu.setText(beizhu)
        self.dateTimeEdit.setDateTime(QDateTime.fromString(dateTime, "yyyy-MM-dd HH:mm"))
        self.id = id

    def setAccount(self, suba):
        """
        设置账户
        suba：二级账户
        """
        self.lineEdit_account.setText(suba)

    def setClassification(self, subc):
        """
        设置分类
        subc：二级分类
        """
        self.lineEdit_classification.setText(subc)

    @pyqtSlot()
    def on_toolButton_account_clicked(self):
        """
        修改账户
        """
        accountM = Dialog_Account_Function(self)
        accountM.subaccountSignal.connect(self.setAccount)
        accountM.exec()
    
    @pyqtSlot()
    def on_toolButton_classification_clicked(self):
        """
        修改分类
        """
        classificationM = DialogChargeClassificationFunction(self.flag, self)
        classificationM.subclassificationSignal.connect(self.setClassification)
        classificationM.exec()

    @pyqtSlot()
    def on_pushButton_del_clicked(self):
        """
        删除流水表
        """
        yorn = QMessageBox.question(self, "询问", "确定删除吗？这会影响整个账户的统计，请谨慎！", defaultButton=QMessageBox.StandardButton.No)
        if yorn == QMessageBox.StandardButton.Yes:
            isok = self.flowfundsM.delFlowfunds(self.id)
            if isok == "success":
                QMessageBox.information(self, "提示", "删除成功！")
                self.successSignal.emit()
                self.accept()
            elif isok == "execut_flowfunds_error":
                QMessageBox.warning(self, "警告", "流水表删除失败！")

    @pyqtSlot()
    def on_pushButton_modify_clicked(self):
        """
        修改流水表
        """
        aName = self.lineEdit_account.text().split('>')[0]
        subaName = self.lineEdit_account.text().split('>')[1]
        cName = self.lineEdit_classification.text().split('>')[0]
        subcName = self.lineEdit_classification.text().split('>')[1]
        money = self.doubleSpinBox_money.value()
        beizhu = self.lineEdit_beizhu.text()
        dateTime = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:MM")
        if self.flag == "out" and money > 0: # 避免随意输入金额导致的错误
            money = -1 * money
        if self.flag == "in" and money < 0:
            money = -1 * money
        isok = self.flowfundsM.modifyFlowfunds(self.id, aName, subaName, cName, subcName, money, beizhu, dateTime)
        if isok == "execut_flowfunds_error":
            QMessageBox.warning(self, "警告", "流水表修改失败！")
        elif isok == "success":
            QMessageBox.information(self, "提示", "流水表修改成功！")
            self.successSignal.emit()