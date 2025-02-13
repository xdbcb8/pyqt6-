#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogAccountSettingFunction.py
@Time    :   2024/01/31 12:39:46
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QDialog, QMenu, QInputDialog, QMessageBox, QRadioButton, QVBoxLayout, QDialogButtonBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QAction
from Ui_DialogAccountSetting import Ui_DialogAccount_Setting
from datamanagement import AccountManagement
from DialogAccountBankSetting import DialogAccountBankSettingFunction
from DialogAccountCreditSetting import DialogAccountCreditSettingFunction
from DialogAccountMoneySettingFunction import DialogAccountMoneySettingFunction

# 账户设置

class CreditSelectDialog(QDialog):
    """
    添加信用卡二级账户：是银行信用卡还是其他借贷账户
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.choice = 1 # 默认是添加银行信用卡
        self.initUi()
    
    def initUi(self):
        self.setWindowTitle("信用卡的类型选择")
        op1 = QRadioButton("银行信用卡", self)
        op1.setChecked(True)
        op2 = QRadioButton("其他借贷账户", self)
        buttonbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)  
        layout = QVBoxLayout(self)
        layout.addWidget(op1)
        layout.addWidget(op2)
        layout.addWidget(buttonbox)
        self.setLayout(layout)

        # 连接信号与槽  
        buttonbox.accepted.connect(self.getResult)  # OK 按钮被点击时关闭对话框并接受
        buttonbox.rejected.connect(self.reject)  # Cancel 按钮被点击时关闭对话框并拒绝

        op1.clicked.connect(self.settype)
        op2.clicked.connect(self.settype)

    def getResult(self):
        self.done(self.choice)

    def settype(self):
        if self.sender().text() == "银行信用卡":
            self.choice = 1
        else:
            self.choice = 2 # "其他借贷账户"

class DialogAccountSettingFunction(QDialog, Ui_DialogAccount_Setting):
    """
    账户设置主程序
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.initData()

    def createmodel(self):
        # 创建一个标准模型  
        model = QStandardItemModel()
        # 设置模型的列名  
        model.setHorizontalHeaderLabels(["账户分类"])
    
        # 创建树形结构
        self.root_item = model.invisibleRootItem() # 根节点

        # 创建账户节点
        # 一级账户
        accountList = self.loadAccount(1)
        for accountItem in accountList:
            itemstr = accountItem[0]
            item = QStandardItem(itemstr)
            if itemstr == "信用卡":
                item.setToolTip("花呗、白条等借贷账户请加在“信用卡”这个账户下！")
            # 二级账户
            subaccountList = self.loadAccount(2, itemstr)
            if subaccountList:
                for child in subaccountList:
                    childItem = QStandardItem(child[0])
                    item.appendRow(childItem)
            self.root_item.appendRow(item)
        expandIndex = model.indexFromItem(self.root_item.child(0)) # 返回第一个一级账户节点的索引
        return model, expandIndex
    
    def initData(self):
        """
        数据初始化
        """
        self.accountM = AccountManagement() # 账户设置的对象
        self.model, expandIndex = self.createmodel()
        self.AccountSettingTree.setModel(self.model)
        self.AccountSettingTree.expand(expandIndex) # 将第一个一级账户节点展开
        qss = """
        QTreeView {  
            font-family: 'Microsoft YaHei';  
            font-size: 11pt;  
        }

        QTreeView::branch {  
            font-family: 'Microsoft YaHei';  
            font-size: 11pt;  
        }

        QHeaderView::section {  
            font-family: 'Microsoft YaHei';  
            font-size: 11pt;  
        }
        """
        self.AccountSettingTree.setStyleSheet(qss) # 设置QSS样式
        self.AccountSettingTree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.AccountSettingTree.customContextMenuRequested.connect(self.treecontextMenuEvent) # 节点上的右键菜单

    def loadAccount(self, level, accountName=""):
        """
        载入一二级账户信息
        level：账户等级
        accountName：一级账户名称
        """
        if level == 1:
            accounts = self.accountM.loadAllAccount()
        elif level == 2:
            accounts = self.accountM.loadAllSubAccount(accountName)
        return accounts
    
    def treecontextMenuEvent(self, pos):
        """
        右键菜单
        """
        hitIndex = self.AccountSettingTree.indexAt(pos) # 返回鼠标指针相对于接收事件的小部件的位置
        if hitIndex.isValid():
            hitItem = self.model.itemFromIndex(hitIndex)
            if not hitItem.parent():
                accountMenu = QMenu(self) # 一级账户上的右键菜单
                addAccountAct = QAction("添加一级账户", accountMenu)
                renameAccountAct = QAction("重命名一级账户", accountMenu)
                delAccountAct = QAction("删除该一级账户", accountMenu)
                addSubAccountAct = QAction("添加二级账户", accountMenu)
                if hitItem.rowCount() != 0: # 有子节点的根节点
                    accountMenu.addActions([addAccountAct, renameAccountAct, delAccountAct])
                else: # 无子节点的根节点
                    accountMenu.addActions([addAccountAct, renameAccountAct, delAccountAct, addSubAccountAct])
                    addSubAccountAct.triggered.connect(lambda:self.accountFunciton(3, self.root_item, hitItem))
                if hitItem.text() in ["现金账户","金融账户","信用卡","投资账户", "虚拟账户"]:
                    renameAccountAct.setEnabled(False) # 这几个一级账户不能重命名和删除
                    delAccountAct.setEnabled(False)
                else:
                    renameAccountAct.setEnabled(True)
                    delAccountAct.setEnabled(True)
                accountMenu.popup(self.AccountSettingTree.viewport().mapToGlobal(pos)) # 弹出菜单
                addAccountAct.triggered.connect(lambda:self.accountFunciton(0, self.root_item))
                renameAccountAct.triggered.connect(lambda:self.accountFunciton(1, self.root_item, hitItem))
                delAccountAct.triggered.connect(lambda:self.accountFunciton(2, self.root_item, hitItem))
            else:
                subaccountMenu = QMenu(self) # 二级账户上的右键菜单
                addSubAccount = QAction("添加二级账户", subaccountMenu)
                renameSubAccount = QAction("重命名二级账户", subaccountMenu)
                delSubAccount = QAction("删除该二级账户", subaccountMenu)
                if hitItem.parent().rowCount() == 1: # 每个一级账户至少保留一个二级账户
                    delSubAccount.setEnabled(False)
                else:
                    delSubAccount.setEnabled(True)
                subaccountMenu.addActions([addSubAccount, renameSubAccount, delSubAccount])
                subaccountMenu.popup(self.AccountSettingTree.viewport().mapToGlobal(pos)) # 弹出菜单
                addSubAccount.triggered.connect(lambda:self.accountFunciton(3, self.root_item, hitItem.parent()))
                renameSubAccount.triggered.connect(lambda:self.accountFunciton(4, self.root_item, hitItem))
                delSubAccount.triggered.connect(lambda:self.accountFunciton(5, hitItem.parent(), hitItem))

    def accountFunciton(self, flag, root, accountItem=None):
        """
        二级账户操作
        flag：不同一级账户对应不同的添加方式
        root：根节点或一级节点
        accountItem：一级节点或二级节点
        """
        if flag == 0: # 添加一级账户
            accoutNameD = QInputDialog.getText(self, "添加一级账户", "添加一级账户的名称")
            if accoutNameD[1]:
                newaccountName = accoutNameD[0] # 添加的账户名称
                if not newaccountName:
                    QMessageBox.information(self, "提示", "新的一级账户名称不能为空！")
                else:
                    self.addAcountMenu(self.accountM, newaccountName, root)
        elif flag == 1: # 重命名一级账户
            accoutNameDN = QInputDialog.getText(self, "重命名一级账户", "请填写新的一级账户的名称")
            if accoutNameDN[1]:
                newaccountName = accoutNameDN[0] # 新的账户名称
                if not newaccountName:
                    QMessageBox.information(self, "提示", "新的一级账户名称不能为空！")
                else:
                    self.renameAcountMenu(self.accountM, accountItem, newaccountName)
        elif flag == 2: # 删除一级账户
            yesorno = QMessageBox.question(self, "删除一级账户", "确认删除吗？删除账户会影响整个记账程序的记录，请务必谨慎！", defaultButton=QMessageBox.StandardButton.No)
            if yesorno == QMessageBox.StandardButton.Yes:
                if accountItem.rowCount() == 0:
                    self.delAcountMenu(self.accountM, accountItem, root)
                else:
                    for i in range(accountItem.rowCount()):
                        childItem = accountItem.child(0) # 遍历删除一级账户下的二级账户
                        self.delsubAcountMenu(self.accountM, childItem, accountItem, info=0) # 不显示成功删除二级账户的提示
                    self.delAcountMenu(self.accountM, accountItem, root) # 最后删除一级账户
        elif flag == 3: # 添加二级账户
            if accountItem.text() == "金融账户":
                bankD = DialogAccountBankSettingFunction(0, self)
                bankD.bankaccountSignal.connect(lambda bankAccount: self.setFinancialsubaccount(bankAccount, accountItem))
                bankD.exec()
            elif accountItem.text() == "现金账户":
                moneyD = DialogAccountMoneySettingFunction(0, self)
                moneyD.moneySignal.connect(lambda moneyAccount: self.setMoneysubaccount(moneyAccount, accountItem))
                moneyD.exec()
            elif accountItem.text() == "信用卡":
                choiceD = CreditSelectDialog(self)
                res = choiceD.exec()
                if res == 1:
                    creditD = DialogAccountCreditSettingFunction(0, self)
                    creditD.creditaccountSignal.connect(lambda creditAccount: self.setCreditsubaccount(creditAccount, accountItem))
                    creditD.exec()
                elif res == 2:
                    self.handle_subaccount_addition(accountItem)
            else: 
                self.handle_subaccount_addition(accountItem)
            expandIndex = self.model.indexFromItem(accountItem) # 返回添加二级节点的父节点索引
            self.AccountSettingTree.expand(expandIndex)
        elif flag == 4: # 重命名二级账户名称
            if accountItem.parent().text() == "金融账户":
                bank = accountItem.text().split("（")[0] # 银行
                bankid = accountItem.text().split("（")[1].replace("）", "") # 卡号后4位
                BankModify = DialogAccountBankSettingFunction(1, self)
                BankModify.bankaccountSignal.connect(lambda newsubaccountName: self.renameSubAcountMenu(newsubaccountName, self.accountM, accountItem))
                BankModify.setBankInfo(bank, bankid)
                BankModify.exec()
            elif accountItem.parent().text() == "信用卡" and "信用卡" in accountItem.text():
                credit = accountItem.text().split("（")[0] # 银行
                creditid = accountItem.text().split("（")[1].replace("）", "") # 卡后后4位
                CreditModify = DialogAccountCreditSettingFunction(1, self)
                CreditModify.creditaccountSignal.connect(lambda newsubaccountName: self.renameSubAcountMenu(newsubaccountName, self.accountM, accountItem))
                CreditModify.setCreditInfo(credit, creditid)
                CreditModify.exec()
            elif accountItem.parent().text() == "现金账户":
                money = accountItem.text().split("（")[0] # 币种
                moneyaccount = accountItem.text().split("（")[1].replace("）", "") # 现金账户别称
                MoneyModify = DialogAccountMoneySettingFunction(1, self)
                MoneyModify.moneySignal.connect(lambda newmoneyName: self.renameSubAcountMenu(newmoneyName, self.accountM, accountItem))
                MoneyModify.setMoneyInfo(money, moneyaccount)
                MoneyModify.exec()
            else:
                subaccoutNameDN = QInputDialog.getText(self, "重命名二级账户", "请填写新的二级账户的名称")
                if subaccoutNameDN[1]:
                    newsubaccountName = subaccoutNameDN[0] # 新的账户名称
                    if not newsubaccountName:
                        QMessageBox.information(self, "提示", "新的二级账户名称为空！")
                    else:
                        self.renameSubAcountMenu(newsubaccountName, self.accountM, accountItem)
        elif flag == 5: # 删除二级账户
            yesorno = QMessageBox.question(self, "删除二级账户", "确认删除吗？删除二级账户会影响整个记账程序的记录，请务必谨慎！", defaultButton=QMessageBox.StandardButton.No)
            if yesorno == QMessageBox.StandardButton.Yes:
                self.delsubAcountMenu(self.accountM, accountItem, root) # 删除二级账户

    def handle_subaccount_addition(self, accountItem): 
        """
        添加二级账户的预操作
        """
        issubaccount = QInputDialog.getText(self, "二级账户", "请输入二级账户信息！")
        if issubaccount[1]:
            subaccountName = issubaccount[0] # 子账户
            if not subaccountName:
                QMessageBox.information(self, "提示", "二级账户名称为空！")
            else:
                self.setNormalsubaccount(subaccountName, accountItem)

    def addAcountMenu(self, dM, account, root):
        """
        添加一级账户
        dM：账户操作类的对象
        account：一级账户名称
        root：根节点
        """
        isok = dM.addAccount(account)
        if isok == "existed":
            QMessageBox.information(self, "提示", "不能输入重复的账户名称！")
        elif isok == "execut_account_error":
            QMessageBox.warning(self, "提示", "一级账户添加失败！")
        elif isok == "success":
            QMessageBox.information(self, "提示", "一级账户添加成功！")
            newAccountItem = QStandardItem(account)
            root.appendRow(newAccountItem)
            
    def renameAcountMenu(self, dM, accountItem, newaccount):
        """
        修改一级账户
        dM：账户操作类的对象
        accountItem：一级账户节点对象
        newaccount：新的一级账户名称
        """
        isok = dM.queryAccountID(newaccount, 1)
        if isok:
            QMessageBox.information(self, "提示", "不能输入重复的账户名称！")
        else:
            old_accountName = accountItem.text() # 原有的账户名称
            isok2 = dM.renameAccount(old_accountName, newaccount)
            if isok2 == "execut_account_error":
                QMessageBox.warning(self, "提示", "一级账户重命名失败！")
            elif isok2 == "success":
                QMessageBox.information(self, "提示", "一级账户重命名成功！")
                accountItem.setText(newaccount)

    def delAcountMenu(self, dM, accountItem, root):
        """
        删除一级账户
        dM：账户操作类的对象
        account：一级账户名称
        """
        delaccountname = accountItem.text() # 一级账户名称
        isok = dM.delAccount(delaccountname)
        if isok == "execut_account_error":
            QMessageBox.warning(self, "提示", "一级账户删除失败！")
        elif isok == "execut_flowfunds_error":
            QMessageBox.warning(self, "提示", "账户流水删除失败！")
        elif isok == "execut_recentaccount_error":
            QMessageBox.warning(self, "提示", "最近使用账户删除失败！")
        elif isok == "success":
            QMessageBox.information(self, "提示", "一级账户删除成功！")
            root.removeRow(accountItem.row())

    def renameSubAcountMenu(self, subnewaccount, dM, subaccountItem):
        """
        修改二级账户
        subnewaccount：新的二级账户名称
        dM：账户操作类的对象
        subaccountItem：二级账户节点对象
        """
        old_accountName = subaccountItem.text() # 原有的账户名称
        isok2 = dM.renameSubAccount(old_accountName, subnewaccount)
        if isok2 == "execut_account_error":
            QMessageBox.warning(self, "提示", "二级账户重命名失败！")
        elif isok2 == "success":
            QMessageBox.information(self, "提示", "二级账户重命名成功！")
            subaccountItem.setText(subnewaccount)

    def delsubAcountMenu(self, dM, subaccountItem, accountItem, info=1):
        """
        删除二级账户
        dM：账户操作类的对象
        subaccountItem：二级账户节点对象
        accountItem：一级账户节点对象
        """
        delsubaccountname = subaccountItem.text() # 二级账户名称
        isok = dM.delSubAccount(delsubaccountname)
        if isok == "execut_subaccount_error":
            QMessageBox.warning(self, "提示", "二级账户删除失败！")
        elif isok == "execut_flowfunds_error":
            QMessageBox.warning(self, "提示", "账户流水删除失败！")
        elif isok == "execut_recentaccount_error":
            QMessageBox.warning(self, "提示", "最近使用账户删除失败！")
        elif isok == "success":
            if info: # 是否提示信息的标志
                QMessageBox.information(self, "提示", "二级账户删除成功！")
            accountItem.removeRow(subaccountItem.row())

    def setFinancialsubaccount(self, bankAccount, accountItem):
        """
        添加二级金融账户
        bankAccount：银行账户
        accountItem：金融账户节点对象
        """
        bankItem = QStandardItem(bankAccount)
        accountItem.appendRow(bankItem)

    def setCreditsubaccount(self, creditAccount, accountItem):
        """
        添加二级信用卡账户
        creditAccount：信用卡二级账户
        accountItem：信用卡账户节点对象
        """
        creditItem = QStandardItem(creditAccount)
        accountItem.appendRow(creditItem)
    
    def setMoneysubaccount(self, moneyAccount, accountItem):
        """
        添加二级现金账户
        moneyAccount：现金二级账户
        accountItem：现金账户节点对象
        """
        moneyItem = QStandardItem(moneyAccount)
        accountItem.appendRow(moneyItem)

    def setNormalsubaccount(self, subaccount, accountItem):
        """
        添加普通二级账户
        subaccount：二级账户
        accountItem：一级账户节点对象
        """
        isok = self.accountM.addSubAccount(subaccount, accountItem.text())
        if isok == "existed":
            QMessageBox.information(self, "提示", "新增的二级账户重复！")
        elif isok == "execut_subaccount_error":
            QMessageBox.warning(self, "警告", "二级账户新增失败")
        elif isok == "success":
            subaccountItem = QStandardItem(subaccount)
            accountItem.appendRow(subaccountItem)