#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogAccountFunction.py
@Time    :   2024/01/27 15:48:07
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, QModelIndex, pyqtSignal
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from Ui_DialogAccount import Ui_Dialog_Account
from datamanagement import AccountManagement

# 账户选择

class Dialog_Account_Function(QDialog, Ui_Dialog_Account):

    subaccountSignal = pyqtSignal(str) # 选中账户的信号

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
        root_item = model.invisibleRootItem()

        # 创建账户节点
        # 最近使用账户
        recentItem = QStandardItem("最近使用")
        root_item.appendRow(recentItem)
        accountRecentList = self.loadAccount(3)
        if accountRecentList:
            for accountRecentItem in accountRecentList:
                if accountRecentItem:
                    accountRecent = accountRecentItem[0] # 一级账户
                    subaccountRecent = accountRecentItem[1] # 二级账户
                    mergeaccount = f"{accountRecent}>{subaccountRecent}"
                    recentSubItem = QStandardItem(mergeaccount)
                    recentItem.appendRow(recentSubItem)
        # 一级账户
        accountList = self.loadAccount(1)
        for accountItem in accountList:
            itemstr = accountItem[0]
            item = QStandardItem(itemstr)
            # 二级账户
            subaccountList = self.loadAccount(2, itemstr)
            if subaccountList:
                for child in subaccountList:
                    childItem = QStandardItem(child[0])
                    item.appendRow(childItem)
            root_item.appendRow(item)
        expandIndex = model.indexFromItem(recentItem) # 返回“最近使用”节点的索引
        return model, expandIndex
    
    def initData(self):
        """
        数据初始化
        """
        self.model, expandIndex = self.createmodel()
        self.AccountTree.setModel(self.model)
        self.AccountTree.expand(expandIndex) # 将“最近使用”节点展开
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
        self.AccountTree.setStyleSheet(qss) # 设置QSS样式

    def loadAccount(self, level, accountName=""):
        """
        载入一二级账户信息
        """
        accountM = AccountManagement()
        if level == 1:
            accounts = accountM.loadAllAccount()
        elif level == 2:
            accounts = accountM.loadAllSubAccount(accountName)
        else:
            accounts = accountM.loadAllRecentSubAccount()
        return accounts

    @pyqtSlot(QModelIndex)
    def on_AccountTree_activated(self, index):
        """
        双击二级账户将账户信息传递出去
        """
        activatedItem = self.model.itemFromIndex(index)
        parent = activatedItem.parent()
        if not parent: # 如果是一级账户被激活，则忽略
            return
        accountText = activatedItem.text() # 二级账户名称
        accountText_parent = parent.text() # 一级账户名称
        if accountText_parent == "最近使用": # 非最近使用，要作一次一二级分类的合并
            mergeAccount = accountText
        else:
            mergeAccount = f"{accountText_parent}>{accountText}"
        self.subaccountSignal.emit(mergeAccount) # 将选中的二级账户传递出去
        self.accept()