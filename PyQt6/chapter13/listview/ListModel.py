#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ListModel.py
@Time    :   2023/08/20 21:15:46
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第13章第1节QListView--视图模型

import os
import codecs
import random
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QVariant, QSize
from PyQt6.QtGui import QIcon, QFont

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录的绝对路径

class ListModel(QAbstractListModel):
    """
    自定义模型
    """
    def __init__(self, Parent=None):
        """
        一些初始设置
        """
        super().__init__(Parent)     
        self.ListItemData = [] # 存储每个QQ好友的列表
        self.Data_init()

    def data(self, index, role):
        """
        子类化QAbstractListModel必须要实现的方法，主要作用就是返回index所引用项目的给定role下存储的数据
        role：角色
        """
        if index.isValid() or (0 <= index.row() < len(self.ListItemData)):
            if role == Qt.ItemDataRole.DisplayRole:
                return QVariant(self.ListItemData[index.row()]["name"])
                # 文本形式呈现数据
            elif role == Qt.ItemDataRole.DecorationRole:
                return QVariant(QIcon(self.ListItemData[index.row()]["iconPath"]))
                # 以图标形式呈现装饰数据
            elif role == Qt.ItemDataRole.SizeHintRole:
                return QVariant(QSize(70, 70))
                # 视图项目大小
            elif role == Qt.ItemDataRole.TextAlignmentRole:
                return QVariant(int(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter))
                # 文本对齐方式
            elif role == Qt.ItemDataRole.FontRole:
                font = QFont()
                font.setPixelSize(20)
                return QVariant(font)
                # 字体设置
        return QVariant()
        # 非上述情况，返回为空，记住这里是QVariant()

    def rowCount(self, parent):
        """
        返回行数，在这里就是数据列表的大小。
        """
        return len(self.ListItemData)

    def Data_init(self):
        """
        数据初始化，随机生成10个好友
        """
        for i in range(10):
            frineName, iconpath = self.loadrandomName()
            ItemData = {"name":"", "iconPath":""}
            ItemData["name"] = frineName
            ItemData["iconPath"] = iconpath
            # 其中联系人的姓名是随机生成的，随机的生成图标的路径；把姓名和图标路径添加到字典当中。
            self.ListItemData.append(ItemData) # append到数据列表里面

    def loadrandomName(self):
        """
        载入姓名和头像
        """
        with codecs.open(f"{current_dir}\\qqres\\name.txt", "r", "utf-8") as f:
            nameList = f.read().split("\r\n")
            frineName = random.choice(nameList) # 随机姓名
            iconpath = f"{current_dir}\\qqres\\{frineName[0]}.png" # 随机姓名对应的头像
            return frineName, iconpath

    def addItem(self, itemData):
        """
        新增的操作实现
        itemData：项目
        """
        if itemData:
            self.beginInsertRows(QModelIndex(), len(self.ListItemData), len(self.ListItemData) + 1)
            self.ListItemData.append(itemData)
            self.endInsertRows()
            # 结束行插入操作

    def deleteItem(self, index):
        """
        指定索引的数据从数据列表中删除
        index：索引
        """
        self.beginRemoveRows(QModelIndex(), index, index + 1)
        del self.ListItemData[index]
        self.endRemoveRows()

    def getItem(self, index):
        """
        获得相应的项目数据
        index：索引
        """
        if index > -1 and index < len(self.ListItemData):
            return self.ListItemData[index]
