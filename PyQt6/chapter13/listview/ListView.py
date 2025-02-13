#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   ListView.py
@Time    :   2023/08/20 21:10:14
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
"""
# 第13章第1节QListView--好友列表视图

from PyQt6.QtWidgets import QListView, QMenu
from PyQt6.QtGui import QAction
from ListModel import ListModel
from newFriendDialog import NewFriend

class ListView(QListView):
    """
    自定义视图
    """
    listview_group = [] # listview_group保存QListView对象和分组名称的对应关系

    def __init__(self):
        """
        一些初始设置
        """
        super().__init__()
        self.listmodel = ListModel(self)
        self.setModel(self.listmodel)
        
    def contextMenuEvent(self, event):
        """
        右键菜单
        """
        hitIndex = self.indexAt(event.pos()).column()
        # 返回鼠标指针相对于接收事件的小部件的位置
        pmenu = QMenu(self)
        pAddItem = QAction("新增好友", pmenu)
        pmenu.addAction(pAddItem)     
        pAddItem.triggered.connect(self.addNewfriend)
        if hitIndex > -1: # 找到索引
            pDeleteAct = QAction("删除", pmenu)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemFriend)
            if len(self.listview_group) > 1:
                pSubMenu = QMenu("转移好友至", pmenu)
                pmenu.addMenu(pSubMenu)
                for item_dic in self.listview_group:
                    # 这里我们将每个分组名称取出，新建一个QAction对象，加入到pSubMenu当中。
                    if self != item_dic["listview"]:
                        pMoveAct = QAction(item_dic["groupname"], pmenu)
                        pSubMenu.addAction(pMoveAct)
                        pMoveAct.triggered.connect(self.move)
                        # 点击这个每个分组的时候就会执行好友转移分组操作，这里就是move()的调用。
            pmenu.popup(self.mapToGlobal(event.pos()))
            # 显示菜单，以便动作QAction对象在指定的全局位置坐标处。这里的全局位置坐标是根据小控件的本地坐标转换为全局坐标的
    
    def deleteItemFriend(self):
        """
        删除好友
        """
        index = self.currentIndex().row()
        if index > -1:
            self.listmodel.deleteItem(index)

    def setListview_group(self, listview):
        """
        将分组名称和QListView对象这个字典增加到listview_group数据列表中
        """
        self.listview_group.append(listview)

    def addNewfriend(self):
        """
        新增好友
        """
        newFfiendExec = NewFriend(self)
        newFfiendExec.friendItem.connect(self.getNewFriend)
        newFfiendExec.exec()

    def getNewFriend(self, name, iconPath):
        """
        获得新的朋友
        name：好友名称
        iconPath：图标路径
        """
        newFriendItemData = {"name":"", "iconPath":""}
        newFriendItemData["name"] = name
        newFriendItemData["iconPath"] = iconPath
        self.addItemFriend(newFriendItemData)

    def addItemFriend(self, friendItem):
        """
        新增一个好友
        friendItem：好友项目
        """
        self.listmodel.addItem(friendItem)

    def move(self):
        """
        实现好友转移
        """
        tolistview = self.find(self.sender().text())
        # 点击的分组名称找到对应的QListView对象
        index = self.currentIndex().row()
        friendItem = self.listmodel.getItem(index)
        tolistview.addItemFriend(friendItem)
        self.listmodel.deleteItem(index)
        # 我们首先要获得这个好友，然后在将转移的分组中将这个好友加上，原分组好友删除

    def find(self, pmenuname):
        """
        找到分组对象
        pmenuname：分组名称
        """
        for item_dic in self.listview_group:
            if item_dic["groupname"] == pmenuname:
                return item_dic["listview"]