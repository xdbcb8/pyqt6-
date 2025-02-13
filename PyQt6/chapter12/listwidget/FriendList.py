#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   FriendList.py
@Time    :   2023/08/13 15:03:45
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
"""
# 第12章第1节QListWidget--好友列表

import os
import random
import codecs
from PyQt6.QtWidgets import QListWidget, QMenu, QListWidgetItem, QAbstractItemView
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QFont, QBrush, QAction
from newFriendDialog import NewFriend

current_dir = os.path.dirname(os.path.abspath(__file__))

class ListWidget(QListWidget):

    """
    QQ模拟
    """

    map_listwidget = [] # map_listwidget保存QListWidget对象和分组名称的对应关系

    def __init__(self):
        """
        一些初始设置
        """
        super().__init__()
        self.Data_init()
        self.Ui_init()

    def Data_init(self):
        """
        数据初始化，随机生成10个会员，有随机会员红名等功能
        """
        for i in range(10):
            item = QListWidgetItem()
            # 随机生成好友名称和头像
            randname, randicon = self.loadrandomName()
            font = QFont()
            font.setPointSize(16)
            item.setFont(font)
            item.setText(randname)
            flag = random.randint(0, 5)
            if flag == 1:
                item.setForeground(QBrush(Qt.GlobalColor.red))
                item.setToolTip("会员红名尊享")
            # 实现随机会员

            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            # 设置联系人名称的对其方式：水平、垂直居中

            item.setIcon(QIcon(randicon))
            self.addItem(item)
            # 给每个联系人设置图标，然后新增到QListWidget当中

    def loadrandomName(self):
        """
        载入姓名和头像
        """
        with codecs.open(f"{current_dir}\\qqres\\name.txt", "r", "utf-8") as f:
            nameList = f.read().split("\r\n")
            frineName = random.choice(nameList) # 随机姓名
            iconpath = f"{current_dir}\\qqres\\{frineName[0]}.png" # 随机姓名对应的头像
            return frineName, iconpath
    
    def Ui_init(self):
        self.setIconSize(QSize(70, 70))
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection) # 项目选择方式，支持ctrl多选
        self.itemSelectionChanged.connect(self.getListitems) # 当选择的项目（联系人）改变时，发出此信号，这里我们返回被选中项目对象的列表
    
    def getListitems(self):
        """
        返回被选中的项目对象的列表
        """
        return self.selectedItems()

    def contextMenuEvent(self, event):
        """
        右键菜单
        """
        hitIndex = self.indexAt(event.pos()).column()
        pmenu = QMenu(self)
        pAddItem = QAction("新增好友", pmenu)
        pmenu.addAction(pAddItem)     
        pAddItem.triggered.connect(self.addItemSlot)
        if hitIndex > -1: # 只有在有好友的情况下才会出现删除或转移好友到其他分组的情况
            pDeleteAct = QAction("删除", pmenu)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            if len(self.map_listwidget) > 1:
                pSubMenu = QMenu("转移好友至", pmenu)
                pmenu.addMenu(pSubMenu)
                for item_dic in self.map_listwidget:
                    if item_dic["listwidget"] is not self:
                        # 在遍历分组名称和QListWidget对象字典的时候，会判断下当前要转移的分组是否就是单击右键时分组。
                        pMoveAct = QAction(item_dic["groupname"], pmenu)
                        pSubMenu.addAction(pMoveAct)
                        pMoveAct.triggered.connect(self.move)
        pmenu.popup(self.mapToGlobal(event.pos()))
    
    def deleteItemSlot(self):
        """
        根据选择的项目（好友）进行删除
        """
        dellist = self.getListitems()
        for delitem in dellist:
            del_item = self.takeItem(self.row(delitem))
            del del_item

    def addItemSlot(self):
        """
        执行新增好友对话框
        """
        friendDialog = NewFriend(self)
        friendDialog.friendItem.connect(self.addNewFriend)
        friendDialog.exec()
        # 这里是执行我们自定义的新增联系人对话框

    def addNewFriend(self, name, iconpath):
        """
        新增好友的设置
        name：好友名称
        iconpath：好友头像路径
        """
        newitem = QListWidgetItem()
        font = QFont()
        font.setPointSize(16)
        newitem.setFont(font)
        newitem.setText(name)
        newitem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        newitem.setIcon(QIcon(iconpath))
        self.addItem(newitem)
        

    def setListMap(self, listwidget):
        """
        把一个分组对象加入到map_listwidget，会在主程序中调用
        """
        self.map_listwidget.append(listwidget)

    def move(self):
        """
        转移好友，获取已选的项目，删除后再增加。
        """
        tolistwidget = self.find(self.sender().text())
        movelist = self.getListitems()
        for moveitem in movelist:
            pItem = self.takeItem(self.row(moveitem))
            tolistwidget.addItem(pItem)

    def find(self, pmenuname):
        """
        找到分组对象
        """
        for item_dic in self.map_listwidget:
            if item_dic["groupname"] == pmenuname:
                return item_dic["listwidget"]