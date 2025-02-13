#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogChargeToAccountFunction.py
@Time    :   2024/02/26 18:35:00
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, QDateTime, pyqtSignal
from PyQt6.QtWidgets import QDialog, QMessageBox
from Ui_DialogChargeToAccount import Ui_Dialog_charge2account
from DialogAccountFunction import Dialog_Account_Function
from DialogChargeClassificationFunction import DialogChargeClassificationFunction
from datamanagement import AccountManagement, ClassificationManagement, FlowFunds

# 记账

class DialogCharge2AccountFunction(QDialog, Ui_Dialog_charge2account):

    dosignal = pyqtSignal() # 记了一笔账的信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.accountIO = "" # 转账的标志
        self.updateCurrentDateTime(0) # 记账对话框出现后即对支出记录时间更新
        self.loadRecentAC()

    def loadRecentAC(self):
        """
        载入最近使用的账户和支出/收入分类
        """
        # 载入最近使用的账户
        self.accountM = AccountManagement()
        subRecentAccountList = self.accountM.loadAllRecentSubAccount()
        if subRecentAccountList:
            if len(subRecentAccountList) >= 2: # 最近使用的账户是2个及以上，取前两个，这里用在转账的账户
                self.account, self.subaccount = f"{subRecentAccountList[0][0]}>{subRecentAccountList[0][1]}", f"{subRecentAccountList[1][0]}>{subRecentAccountList[1][1]}"
            else:
                self.account, self.subaccount = f"{subRecentAccountList[0][0]}>{subRecentAccountList[0][1]}", ""
        else: # 没有最近使用账户
            self.account, self.subaccount = "", ""
        self.updateAccount(0, self.account, self.subaccount)

        # 载入最近使用的支出/收入分类
        self.classificationM = ClassificationManagement()
        subClassificationListOut = self.classificationM.loadAllRecentClassification('out') # 支出
        if subClassificationListOut:
            expandClassification = f"{subClassificationListOut[0][0]}>{subClassificationListOut[0][1]}"
            self.updateClassification(0, expandClassification)
        subClassificationListIn = self.classificationM.loadAllRecentClassification('in') # 收入
        if subClassificationListIn:
            incomeClassification = f"{subClassificationListIn[0][0]}>{subClassificationListIn[0][1]}"
            self.updateClassification(1, incomeClassification)

    def currentTabAccountSetting(self, account):
        """
        账户的选择
        account：合并的账户名称
        """
        index = self.tabWidget_charge.currentIndex()
        self.updateAccount(index, account, "")

    def currentTabClassificationSetting(self, classification):
        """
        支出/收入分类的选择
        classification：分类名称
        """
        index = self.tabWidget_charge.currentIndex()
        self.updateClassification(index, classification)

    def updateClassification(self, index, classification):
        """
        显示最近使用的支出/收入分类
        index：选项卡的索引
        classification：分类名称
        """
        if index == 0:
            self.lineEdit_classificaiton_expend.setText(classification)
        elif index == 1:
            self.lineEdit_classificaiton_income.setText(classification)

    def updateCurrentDateTime(self, index):
        """
        显示当前选项卡中的日期时间
        index：选项卡的索引
        """
        currentDateTime = QDateTime.currentDateTime() # 当前日期时间
        if index == 0:
            self.dateTimeEdit_expend.setDateTime(currentDateTime) # 支出日期时间更新
        elif index == 1:
            self.dateTimeEdit_income.setDateTime(currentDateTime) # 收入日期时间更新
        elif index == 2:
            self.dateTimeEdit_transfer.setDateTime(currentDateTime) # 转账日期时间更新
        elif index == 3:
            self.dateTimeEdit_balance.setDateTime(currentDateTime) # 余额调整日期时间更新

    def updateAccount(self, index, account1, account2):
        """
        显示最近使用的账户
        index：选项卡的索引
        account1：第一个最近使用的账户
        account2：第二个最近使用的账户
        """
        if index == 0: # 支出
            self.lineEdit_account_expend.setText(account1)
        elif index == 1: # 收入
            self.lineEdit_account_income.setText(account1)
        elif index == 2: # 转账
            if all([account1, account2]):
                self.lineEdit_account_transfer_out.setText(account1)
                self.lineEdit_account_transfer_in.setText(account2)
            else: # 只对单一账户进行选择
                if self.accountIO == "out":
                    self.lineEdit_account_transfer_out.setText(account1)
                else:
                    self.lineEdit_account_transfer_in.setText(account1)
        elif index == 3:
            self.lineEdit_account_balance.setText(account1)
            subaccount = account1.split('>')[1] # 二级账户
            self.updateSubAccountbalance(subaccount)
        
    def updateSubAccountbalance(self, subaccount):
        """
        显示二级账户的余额
        """
        subaccountbalanceList = self.accountM.loadAllSubAccountBalance(subaccount)
        if subaccountbalanceList:
            self.subaccountbalance_old = subaccountbalanceList[0][0] # 二级账户的余额
            self.doubleSpinBox_balance.setValue(self.subaccountbalance_old)
        else:
            self.subaccountbalance_old = 0
            self.doubleSpinBox_balance.setValue(0)

    def updateFlowFunds(self, subaName, subcName, money, bz, dT):
        """
        更新流水
        subaName：二级账户
        subcName：二级支出/收入分类
        money：交易金额
        bz：备注
        dT：日期时间
        """
        flowfundM = FlowFunds()
        isok = flowfundM.addFlowfunds(subaName, subcName, money, bz, dT)
        if isok == "execut_flowfunds_error":
            QMessageBox.warning(self, "警告", "流水表数据库操作失败！")
            return
        elif isok =="success":
            return isok

    def updateRecentAccount(self, subac, datetime):
        """
        新增最近使用的账户记录
        subac：二级账户
        datetime：记录的日期时间
        """
        isok = self.accountM.addRecentAccount(subac, datetime)
        if isok == "execut_recentaccount_error":
            QMessageBox.warning(self, "警告", "最近账户表数据库操作失败！")
        elif isok == "success":
            return isok

    def updateRecentClassification(self, subcla, flag, datetime):
        """
        新增最近使用的支出/收入分类记录
        subcla：二级分类
        flag：标记支出或者收入
        datetime：记录的日期时间
        """
        isok = self.classificationM.addRecentClassification(subcla, flag, datetime)
        if isok == "execut_recentclassificaiton_error":
            QMessageBox.warning(self, "警告", "最近支出/收入分类表数据库操作失败！")
        elif isok == "success":
            return isok

    @pyqtSlot(int)
    def on_tabWidget_charge_currentChanged(self, index):
        """
        选项卡的切换
        index：选项卡索引
        """
        self.updateCurrentDateTime(index)
        self.updateAccount(index, self.account, self.subaccount)

    @pyqtSlot()
    def on_toolButton_account_expend_clicked(self):
        """
        支出账户选择
        """
        account = Dialog_Account_Function(self)
        account.subaccountSignal.connect(self.currentTabAccountSetting)
        account.exec()

    @pyqtSlot()
    def on_toolButton_account_income_clicked(self):
        """
        收入账户选择
        """
        account = Dialog_Account_Function(self)
        account.subaccountSignal.connect(self.currentTabAccountSetting)
        account.exec()

    @pyqtSlot()
    def on_toolButton_account_transfer_in_clicked(self):
        """
        转入账户选择
        """
        self.accountIO = "in"
        account = Dialog_Account_Function(self)
        account.subaccountSignal.connect(self.currentTabAccountSetting)
        account.exec()

    @pyqtSlot()
    def on_toolButton_account_transfer_out_clicked(self):
        """
        转出账户选择
        """
        self.accountIO = "out"
        account = Dialog_Account_Function(self)
        account.subaccountSignal.connect(self.currentTabAccountSetting)
        account.exec()

    @pyqtSlot()
    def on_toolButton_transfer_clicked(self):
        """
        转入、转出账户互换
        """
        transferIn = self.lineEdit_account_transfer_in.text() # 转入账户
        transferOut = self.lineEdit_account_transfer_out.text() # 转出账户
        self.lineEdit_account_transfer_in.setText(transferOut)
        self.lineEdit_account_transfer_out.setText(transferIn)
    
    @pyqtSlot()
    def on_toolButton_account_balance_clicked(self):
        """
        余额账户选择
        """
        account = Dialog_Account_Function(self)
        account.subaccountSignal.connect(self.currentTabAccountSetting)
        account.exec()

    @pyqtSlot()
    def on_toolButton_classificaiton_expend_clicked(self):
        """
        支出分类选择
        """
        classification = DialogChargeClassificationFunction("out", self)
        classification.subclassificationSignal.connect(self.currentTabClassificationSetting)
        classification.exec()

    @pyqtSlot()
    def on_toolButton_classificaiton_income_clicked(self):
        """
        收入分类选择
        """
        classification = DialogChargeClassificationFunction("in", self)
        classification.subclassificationSignal.connect(self.currentTabClassificationSetting)
        classification.exec()

    @pyqtSlot()
    def on_pushButton_ok_clicked(self):
        """
        确定按钮
        """
        index = self.tabWidget_charge.currentIndex() # 当前标签页的索引
        if index == 0: # 支出记录
            subaccountName  = self.lineEdit_account_expend.text().split('>')[1] # 二级账户
            subclassificationName= self.lineEdit_classificaiton_expend.text().split('>')[1] # 二级支出分类
            money = self.doubleSpinBox_expend.value() * -1 # 支出的钱
            beizhu = self.lineEdit_remark_expend.text() # 备注
            dateTimestr = self.dateTimeEdit_expend.dateTime().toString("yyyy-MM-dd HH:mm") # 记录的日期时间
            if money == 0: # 金额为0忽略操作
                return
            isok = self.updateFlowFunds(subaccountName, subclassificationName, money, beizhu, dateTimestr) # 更新流水
            if isok == "success":
                isok2 = self.updateRecentAccount(subaccountName, dateTimestr) # 更新最近使用的账户
                if isok2 == "success":
                    self.updateRecentClassification(subclassificationName, "out", dateTimestr) # 更新最近使用的支出分类
        elif index == 1: # 收入记录
            subaccountName  = self.lineEdit_account_income.text().split('>')[1] # 二级账户
            subclassificationName= self.lineEdit_classificaiton_income.text().split('>')[1] # 二级支出分类
            money = self.doubleSpinBox_income.value() # 收入的钱
            beizhu = self.lineEdit_remark_income.text() # 备注
            dateTimestr = self.dateTimeEdit_income.dateTime().toString("yyyy-MM-dd HH:mm") # 记录的日期时间
            if money == 0: # 金额为0忽略操作
                return
            isok = self.updateFlowFunds(subaccountName, subclassificationName, money, beizhu, dateTimestr) # 更新流水
            if isok == "success":
                isok2 = self.updateRecentAccount(subaccountName, dateTimestr) # 更新最近使用的账户
                if isok2 == "success":
                    self.updateRecentClassification(subclassificationName, "in", dateTimestr) # 更新最近使用的收入分类
        elif index == 2:# 转账记录
            subaccountName_in  = self.lineEdit_account_transfer_in.text().split('>')[1] # 二级转入账户
            subaccountName_out  = self.lineEdit_account_transfer_out.text().split('>')[1] # 二级转出账户
            subclassificationName = "" # 二级支出分类为空字符串，转账不涉及
            moneyout = self.doubleSpinBox_transfer.value() * -1 # 转出的钱
            moneyin = self.doubleSpinBox_transfer.value() # 转入的钱
            beizhu = self.lineEdit_remark_transfer.text() # 备注
            dateTimestr = self.dateTimeEdit_transfer.dateTime().toString("yyyy-MM-dd HH:mm") # 记录的日期时间
            if moneyin == 0: # 金额为0忽略操作
                return
            isok_in = self.updateFlowFunds(subaccountName_in, subclassificationName, moneyin, beizhu, dateTimestr) # 需要更新两次流水，即转出、转入
            isok_out = self.updateFlowFunds(subaccountName_out, subclassificationName, moneyout, beizhu, dateTimestr)
            if isok_in == "success" and isok_out == "success":
                self.updateRecentAccount(subaccountName_in, dateTimestr) # 更新最新账户
                self.updateRecentAccount(subaccountName_out, dateTimestr)                  
        elif index == 3: # 可以修改账户余额
            balance = self.doubleSpinBox_balance.value()
            subaccountName = self.lineEdit_account_balance.text().split('>')[1] # 二级账户
            if balance == self.subaccountbalance_old: # 余额没有发生变化则忽略操作
                return
            difference = balance - self.subaccountbalance_old # 现在账户的余额与之前余额的差距
            dateTimestr = self.dateTimeEdit_balance.dateTime().toString("yyyy-MM-dd HH:mm") # 记录的日期时间
            subclassificationName = "" # 二级支出分类均为空字符串，余额修改不涉及
            beizhu = self.lineEdit_remark_balance.text()
            self.updateFlowFunds(subaccountName, subclassificationName, difference, beizhu, dateTimestr)
        self.dosignal.emit() # 记了一笔账，就发出该信号