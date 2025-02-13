#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   qq.py
@Time    :   2023/08/20 20:59:44
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
"""
# 第13章第1节QListView--主程序

import sys
from PyQt6.QtWidgets import QApplication, QToolBox, QListView, QMenu, QInputDialog, QMessageBox
from PyQt6.QtCore import Qt
from ListView import ListView
from PyQt6.QtGui import QAction

class QQ(QToolBox):
    """
    自定义类的整合
    """
    def __init__(self):
        """
        一些初始设置
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        界面
        """
        self.setWindowTitle("QListView举例")
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint|Qt.WindowType.WindowCloseButtonHint)
        self.setMinimumSize(200, 600)
        self.setWhatsThis("这个一个模拟QQ软件")
        FriendListView = ListView() 
        FriendListView.setViewMode(QListView.ViewMode.ListMode) # 设置视图模型
        FriendListView.setStyleSheet("QListView{icon-size:70px}") # 设置QListView图标的大小70像素
        dic_list = {"listview":FriendListView, "groupname":"我的好友"}
        # 当前listview对象和分组名称放入到一个字典

        FriendListView.setListview_group(dic_list)
        # 这个字典放入到listview_group这个列表
        self.addItem(FriendListView, "我的好友") 
        self.show()
    
    def contextMenuEvent(self, event):
        """
        右键菜单
        """
        pmenu = QMenu(self)
        pAddGroupAct = QAction("添加分组", pmenu)
        pmenu.addAction(pAddGroupAct)
        pAddGroupAct.triggered.connect(self.addGroup)
        pmenu.popup(self.mapToGlobal(event.pos()))

    def addGroup(self):
        """
        增加分组
        """
        groupname, isok = QInputDialog.getText(self, "输入分组名", "")
        # 返回的是一个元组，其中第0个元素是分组名，第1个元素返回是否按了确定键
        if isok:
            if groupname:
                FriendListView1 = ListView()
                FriendListView1.setViewMode(QListView.ViewMode.ListMode)
                FriendListView1.setStyleSheet("QListView{icon-size:70px}")
                self.addItem(FriendListView1, groupname)
                dic_list = {"listview":FriendListView1, "groupname":groupname}
                FriendListView1.setListview_group(dic_list)
                # 新建一个ListView对象并将其与分组名称添加到字典当中，然后通过setListview_group()将这个字典放入到listview_group这个列表中
            else:
                QMessageBox.warning(self, "警告", "分组名称没有填写！")  # 没有填写分组名又按了确定键的话，就报错。

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qq = QQ()
    sys.exit(app.exec())