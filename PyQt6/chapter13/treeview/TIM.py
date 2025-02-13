#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   TIM.py
@Time    :   2023/08/13 18:05:47
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第13章第2节QTreeView--主窗体

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QAbstractItemView, QCompleter, QLineEdit, QToolButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QStandardItemModel, QStandardItem
from newFriendDialog import NewFriend
from friendTree import FriendTree

class TIM(QWidget):
    """
    TIM模拟
    """
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        """
        界面初始设置
        """
        self.setWindowTitle("QTreeView举例")
        self.resize(300, 700)
        # 只保留最小化、关闭按钮
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint|Qt.WindowType.WindowMinimizeButtonHint)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setClearButtonEnabled(True)
        bt_search = QToolButton(self)
        bt_search.setText("查找")
        bt_adduser = QToolButton(self)
        bt_adduser.setText("新增")
        self.treeView = FriendTree(self)
        self.treeView.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection) # 允许多选

        # 搜索时自动填充好友姓名
        self.m_model = QStandardItemModel(0, 1, self)
        m_completer = QCompleter(self.m_model, self)
        self.lineEdit.setCompleter(m_completer)
        m_completer.activated[str].connect(self.onUsernameChoosed)

        # 布局
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.lineEdit)
        hlayout.addWidget(bt_search)
        hlayout.addWidget(bt_adduser)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.treeView)
        self.setLayout(vlayout)

        # 信号与槽连接
        bt_search.clicked.connect(self.searchFriend)
        bt_adduser.clicked.connect(self.addNewFriendDialog)
        self.lineEdit.textEdited.connect(self.autocompleteName)

        self.show()

    def onUsernameChoosed(self, name):
        """
        自动补全后设置搜索的好友
        name：好友姓名
        """
        self.lineEdit.setText(name)

    def autocompleteName(self, text):
        """
        好友名称自动补全
        text：好友名称
        """
        namelist = []
        for itm in self.treeView.userslist:
            username = itm["username"]
            if username.find(text) >= 0:
                namelist.append(itm["username"])
        self.m_model.removeRows(0, self.m_model.rowCount())
        for i in range(0, len(namelist)):
            self.m_model.insertRow(0)
            self.m_model.setData(self.m_model.index(0, 0), namelist[i])

    def searchFriend(self):
        """
        查找好友
        """
        username = self.lineEdit.text()
        if username:
            useritemindex = self.treeView.searchuser(username)
            if useritemindex: # 若有好友存在才会提示找到
                useritem = self.treeView.userslist[useritemindex]["user"]
                index = self.treeView.model().indexFromItem(useritem)
                self.treeView.setCurrentIndex(index) # 按照索引找到好友

    def addNewFriendDialog(self):
        """
        启动增加好友对话框
        """
        self.adduser = NewFriend(self) # 自定义增加好友对话框
        for g in self.treeView.grouplist:
            self.adduser.comboBox.addItem(g["groupname"])
        self.adduser.friendItem.connect(self.setnewFriend)
        self.adduser.exec()
    
    def setnewFriend(self, newname, newicon):
        """
        设置新增的好友
        newname：好友姓名
        newicon：好友头像路径
        """
        newitem = QStandardItem()
        font = QFont()
        font.setPointSize(16)
        newitem.setFont(font)
        newitem.setText(newname) # 好友姓名
        newitem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)
        newitem.setIcon(QIcon(newicon)) # 好友头像
        comboxinfo = self.adduser.comboBox.currentText() # 新增好友分组
        cindex = self.treeView.searchgroup(comboxinfo)
        group = self.treeView.grouplist[cindex]["group"] # 分组对象
        self.treeView.grouplist[cindex]["childcount"] += 1
        userdic = {"user":newitem, "username":newname, "iconPath":QIcon(newicon), "isvip":0, "ishide":0} # 新的好友信息
        self.treeView.userslist.append(userdic)
        group.appendRow(newitem) # 分组增加好友
        self.treeView.restatistic_op(group) # 增加好友之后相关数据要更新一下
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    tim = TIM()
    sys.exit(app.exec())