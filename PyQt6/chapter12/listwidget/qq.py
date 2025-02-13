#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   qq.py
@Time    :   2023/08/13 11:39:08
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
"""
# 第12章第1节QListWidget-主窗体

import sys
from PyQt6.QtWidgets import QApplication, QToolBox, QMenu, QInputDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from FriendList import ListWidget

class QQ(QToolBox):
    def __init__(self):
        super().__init__()
        self.initUI()    

    def initUI(self):
        self.setWindowTitle("QQ好友模拟")
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setMinimumSize(200,600)
        self.setWhatsThis("模拟QQ好友列表")
        pListWidget = ListWidget()
        dic_list = {"listwidget":pListWidget, "groupname":"我的好友"}
        pListWidget.setListMap(dic_list)
        self.addItem(pListWidget, "我的好友") 
        self.show()

    def contextMenuEvent(self, event):
        """
        右键菜单--添加分组
        """
        pmenu = QMenu(self)
        pAddGroupAct = QAction("添加分组", pmenu)
        pmenu.addAction(pAddGroupAct) 
        pAddGroupAct.triggered.connect(self.addGroupSlot)  
        pmenu.popup(self.mapToGlobal(event.pos()))

    def addGroupSlot(self):
        """
        增加好友分组
        """
        groupname, isok = QInputDialog.getText(self, "新建分组", "输入好友分组名称")
        if isok:
            if groupname: 
                pListWidget = ListWidget()
                self.addItem(pListWidget, groupname)
                # 分组和好友列表控件相对应
                dic_list = {"listwidget":pListWidget, "groupname":groupname}
                pListWidget.setListMap(dic_list)
            else:
                QMessageBox.information(self, "提示", "好友分组名称未填写！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qq = QQ()
    sys.exit(app.exec())