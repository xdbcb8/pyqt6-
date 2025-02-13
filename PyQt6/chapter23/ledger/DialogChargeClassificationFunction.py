#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogChargeClassificationFunction.py
@Time    :   2024/01/30 08:58:04
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, QModelIndex, pyqtSignal
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from Ui_DialogChargeClassification import Ui_DialogCharge
from datamanagement import ClassificationManagement

# 分类选择

class DialogChargeClassificationFunction(QDialog, Ui_DialogCharge):

    subclassificationSignal = pyqtSignal(str)

    def __init__(self, flag, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.flag = flag # 控制显示支出或者收入分类
        self.initData()

    def createmodel(self):
        # 创建一个标准模型  
        model = QStandardItemModel()
        # 设置模型的列名
        if self.flag == "in":
            headerlabel = "收入分类"
        else:
            headerlabel = "支出分类"
        model.setHorizontalHeaderLabels([headerlabel])
    
        # 创建树形结构
        root_item = model.invisibleRootItem()

        # 创建支出/收入分类节点
        # 最近使用支出/收入分类
        recentItem = QStandardItem("最近使用")
        root_item.appendRow(recentItem)
        classificationRecentList = self.loadClassification(3, self.flag)
        if classificationRecentList:
            for classificationRecentItem in classificationRecentList:
                if classificationRecentItem:
                    recentclaItem = classificationRecentItem[0] # 一级支出/收入分类
                    recentsubclaItem = classificationRecentItem[1] # 二级支出/收入分类
                    mergecla = f"{recentclaItem}>{recentsubclaItem}"
                    recentSubItem = QStandardItem(mergecla)
                    recentItem.appendRow(recentSubItem)
        # 一级支出/收入分类
        classificationList = self.loadClassification(1, self.flag)
        for classificationItem in classificationList:
            itemstr = classificationItem[0] # 一级分类
            item = QStandardItem(itemstr)
            # 二级支出/收入分类
            subclassificationList = self.loadClassification(2, itemstr)
            if subclassificationList:
                for child in subclassificationList:
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
        self.ChargeClassificationTree.setModel(self.model)
        self.ChargeClassificationTree.expand(expandIndex) # 将“最近使用”节点展开
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
        self.ChargeClassificationTree.setStyleSheet(qss) # 设置QSS样式

    def loadClassification(self, level, classification=""):
        """
        载入一二级支出/收入分类信息
        """
        classificationM = ClassificationManagement()
        if level == 1:
            classifications = classificationM.loadAllClassification(self.flag)
        elif level == 2:
            classifications = classificationM.loadAllSubClassification(classification, self.flag)
        else:
            classifications = classificationM.loadAllRecentClassification(self.flag)
        return classifications

    @pyqtSlot(QModelIndex)
    def on_ChargeClassificationTree_activated(self, index):
        """
        双击二级支出/收入分类信息传递出去
        """
        activatedItem = self.model.itemFromIndex(index)
        parent = activatedItem.parent()
        if not parent: # 如果是一级支出/收入分类被激活，则忽略
            return
        classificationText = activatedItem.text() # 二级支出/收入分类
        classificationText_parent = parent.text() # 一级支出/收入分类
        if classificationText_parent == "最近使用": # 非最近使用，要作一次一二级分类的合并
            mergeClassification = classificationText
        else:
            mergeClassification = f"{classificationText_parent}>{classificationText}"
        self.subclassificationSignal.emit(mergeClassification) # 将选中的二级账户传递出去
        self.accept()