#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   TIM.py
@Time    :   2023/08/13 18:05:47
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第12章第2节QTreeWidget--主窗体

import sys
import os
import random
import codecs
from PyQt6.QtWidgets import (QWidget, QApplication, QTreeWidget, QTreeWidgetItem, QMenu, 
                            QInputDialog, QMessageBox, QAbstractItemView, QCompleter, 
                            QLineEdit, QToolButton, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import Qt, QSize, QVariant
from PyQt6.QtGui import QIcon, QFont, QBrush, QStandardItemModel, QAction
from newFriendDialog import NewFriend

current_dir = os.path.dirname(os.path.abspath(__file__))

class TIM(QWidget):
    """
    TIM模拟
    """
    def __init__(self):
        super().__init__()
        self.grouplist = [] # 分组信息列表储
        self.userslist = [] # 用户信息列表存储
        self.tmpuseritem = [] # 临时保存选中的好友对象，以便进行批量操作
        self.initUI()
    
    def initUI(self):
        """
        界面初始设置
        """
        self.setWindowTitle("QTreeWidget举例")
        self.resize(300, 700)
        # 只保留最小化、关闭按钮
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint|Qt.WindowType.WindowMinimizeButtonHint)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setClearButtonEnabled(True)
        bt_search = QToolButton(self)
        bt_search.setText("查找")
        bt_adduser = QToolButton(self)
        bt_adduser.setText("新增")
        self.treeWidget = QTreeWidget(self)
        # 每个项目的标题中添加一列，并为每列设置标签
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setColumnWidth(0, 50)
        self.treeWidget.setHeaderLabels(["好友"])
        # 设置图标大小的
        self.treeWidget.setIconSize(QSize(70, 70))
        # 同时设置多选的方式
        self.treeWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.treeWidget.itemSelectionChanged.connect(self.getListitems)# 项目选择发生变化时发出信号
        self.treeWidget.currentItemChanged.connect(self.restatistic)# 当前项目发生变化时发出信号
        self.treeWidget.itemClicked.connect(self.isclick)# 项目点击时发出信号
 
        root = self.creategroup("我的好友")# 默认用户组
        root.setExpanded(True)# 默认是好友展开

        self.menuflag = 1 # 是否出现批量操作菜单的标志
        
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
        vlayout.addWidget(self.treeWidget)
        self.setLayout(vlayout)

        # 信号与槽连接
        bt_search.clicked.connect(self.searchFriend)
        bt_adduser.clicked.connect(self.addNewFriendDialog)
        self.lineEdit.textEdited.connect(self.autocompleteName)

    def creategroup(self, groupname):
        """
        增加分组
        groupname：分组名称
        """
        hidernum = 0
        # 统计离线好友

        group = QTreeWidgetItem(self.treeWidget)
        # 新增一个分组（QTreeWidgetItem类型），这个分组是挂在self.treeWidget下的

        groupdic = {"group":group, "groupname":groupname, "childcount":0, "childishide":0}
        # 分组信息字典：包括分组名称、在线、离线人数
        
        for i in range(10):
            child = QTreeWidgetItem()
            # 一个好友
            randname, randicon, font, isvip, ishider = self.createusers()# 随机创建一个用户
            userdic = {"user":child, "username":randname, "ishide":0}
            self.userslist.append(userdic)
            child.setText(0, randname)
            child.setFont(0, font)
            child.setIcon(0, randicon)
            child.setTextAlignment(0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            if isvip == 1:
                # 会员红名
                child.setForeground(0, QBrush(Qt.GlobalColor.red))
                child.setToolTip(0, "会员红名尊享")
            if ishider == 1:
                # 是否离线
                hidernum += 1
                userdic["ishide"] = 1
            group.addChild(child)
            # 将每个好友增加先前创建的group分组当中

        childnum = group.childCount()
        # 统计每个分组下好友的数量

        lastchildnum = childnum - hidernum # 好友数量减去离线好友的数量就是在线好友的数量

        groupdic["childcount"] = childnum
        groupdic["childishide"] = hidernum
        # 更新groupdic中的数据

        groupname += " " + str(lastchildnum) + "/" + str(childnum)
        # 将当前groupname设置成类似：我的好友 8/10 的样式

        group.setText(0, groupname)
        # 将给定列中显示的文本设置为给定文本，如：我的好友 8/10

        self.grouplist.append(groupdic)
        #把分组加入到分组列表中

        return group
    
    def loadrandomName(self):
        """
        载入姓名和头像
        """
        with codecs.open(f"{current_dir}\\timres\\name.txt", "r", "utf-8") as f:
            nameList = f.read().split("\r\n")
            frineName = random.choice(nameList) # 随机姓名
            iconpath = f"{current_dir}\\timres\\{frineName[0]}" # 随机姓名对应的头像
            return frineName, iconpath

    def createusers(self):
        """
        创建一个好友，属性随机
        """
        randname, iconpath = self.loadrandomName()
        font = QFont()
        font.setPointSize(16)
        isvip = random.randint(0, 5) # 是否会员
        ishider = random.randint(0, 5) # 是否离线
        randicon = QIcon(f"{iconpath}.png")
        if ishider == 1:
            randicon = QIcon(f"{iconpath}H.png")
        return randname, randicon, font, isvip, ishider

    def contextMenuEvent(self, event):
        """
        右键菜单
        """
        hititem = self.treeWidget.currentItem()
        # 返回树型控件中的当前项目，这里可以是分组也可以是好友

        if hititem:
            root = hititem.parent()
            # 看看是否为根节点

            if root is None: # 如果该节点无父节点，说明是根节点
                pgroupmenu = QMenu(self)
                pAddgroupAct = QAction("添加分组", pgroupmenu)
                pRenameAct = QAction("重命名分组", pgroupmenu)
                pDeleteAct = QAction("删除该组", pgroupmenu)
                pgroupmenu.addAction(pAddgroupAct)
                pgroupmenu.addAction(pRenameAct)
                pgroupmenu.addAction(pDeleteAct)
                pAddgroupAct.triggered.connect(self.addgroup)
                pRenameAct.triggered.connect(self.renamegroup)

                if self.treeWidget.itemAbove(hititem) is None:
                    pDeleteAct.setEnabled(False)
                else:
                    pDeleteAct.triggered.connect(self.deletegroup)
                # 若最顶端的分组（它的上面是没有分组的），pDeleteAct被设置为禁用，否则是可以执行删除分组操作

                pgroupmenu.popup(self.mapToGlobal(event.pos()))
                # 弹出菜单
            elif root.childCount() > 0:
                # 下面有好友的话
                pItemmenu = QMenu(self)       
                pDeleteItemAct = QAction("删除好友", pItemmenu)
                pItemmenu.addAction(pDeleteItemAct)            
                pDeleteItemAct.triggered.connect(self.delete)
                if len(self.grouplist) > 1:
                    pSubMenu = QMenu("转移好友至", pItemmenu)
                    pItemmenu.addMenu(pSubMenu)
                    for item_dic in self.grouplist:
                        if item_dic["group"] is not root:
                            pMoveAct = QAction(item_dic["groupname"] ,pItemmenu)
                            pSubMenu.addAction(pMoveAct)
                            pMoveAct.triggered.connect(self.moveItem)
                if len(self.getListitems(self.menuflag)) == 1:
                    pRenameItemAct = QAction("设定备注", pItemmenu)
                    pItemmenu.addAction(pRenameItemAct)            
                    pRenameItemAct.triggered.connect(self.renameItem)
                    # 我们选择的好友数量只能为1的时候，才能设定备注
                if self.menuflag > 0 and root.childCount() > 1:
                    pBatchAct = QAction("分组内批量操作", pItemmenu)
                    pItemmenu.addAction(pBatchAct)
                    pBatchAct.triggered.connect(self.Batchoperation)
                    # 如果批量操作标志大于0，且该分组下的好友多于1人，则菜单“分组内批量操作”出现
                elif self.menuflag < 0:
                    pCancelBatchAct = QAction("取消批量操作", pItemmenu)
                    pItemmenu.addAction(pCancelBatchAct)
                    pCancelBatchAct.triggered.connect(self.CancelBatchoperation)
                    # 否则批量操作标志小于0，我们就显示取消批量操作按钮，这个联系到CancelBatchoperation()函数。
                    
                pItemmenu.popup(self.mapToGlobal(event.pos()))
                #弹出菜单

    def getListitems(self, flag=1):
        """
        获得选择的好友数量
        """
        if flag > 0:
            return self.treeWidget.selectedItems()
            # 当批量操作标志大于0的时候，即返回所有选定的非隐藏项目的列表
        return self.tmpuseritem
        # 要是批量操作标志小于0的时候，我们返回临时存储批量操作的好友项目。

    def addgroup(self):
        """
        增加一个分组
        """
        gname, isok = QInputDialog.getText(self, "提示信息", "请输入分组名称")
        if isok:
            if not gname:
                QMessageBox.information(self, "提示", "分组名称不能为空哦")
            else:
                self.creategroup(gname)

    def searchgroup(self, hitgroup):
        """
        根据分组名称或对象返回其索引
        """
        if isinstance(hitgroup, str):# 判断hitgroup是否为分组名称，用于批量转移时操作
            for i, g in enumerate(self.grouplist):
                if g["groupname"] == hitgroup:
                    return i
        else:
            for i, g in enumerate(self.grouplist):# 分组对象吗？
                if g["group"] == hitgroup:
                    return i

    def renamegroup(self):
        """
        重命名分组，之后相关数据更新一下
        """
        hitgroup = self.treeWidget.currentItem()
        #我们选中的分组

        gnewname, isok = QInputDialog.getText(self, "提示信息", "请输入分组的新名称")
        if isok:
            if len(gnewname) == 0:
                QMessageBox.information(self, "提示", "分组名称不能为空哦")
            else:
                hitgroup.setText(0, gnewname)
                gindex = self.searchgroup(hitgroup)
                self.grouplist[gindex]["groupname"] = gnewname
                self.treeWidget.setCurrentItem(hitgroup.child(0))
                # 设置当前的项目（这里表示分组中的第一个好友）
                
    def deletegroup(self):
        """
        删除分组
        """
        hitgroup = self.treeWidget.currentItem()
        gindex = self.searchgroup(hitgroup)
        reply = QMessageBox.question(self, "警告", "确定要删除这个分组及其好友吗？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.treeWidget.takeTopLevelItem(gindex)
            # 删除树中给定索引处的顶级项目并返回它

            del self.grouplist[gindex]
            # 也要把在self.grouplist的数据也要删除

    def moveItem(self):
        """
        移动好友
        """
        movelist = self.getListitems(self.menuflag)
        togroupname = self.sender().text()
        mindex = self.searchgroup(togroupname)
        # 得到新的分组对象
        togroup = self.grouplist[mindex]["group"]
        # 分组的好友先删除后增加实现好友移动
        self.deleteItems(movelist, flag=0)
        self.add(togroup, movelist)
        self.tmpuseritem.clear() # 暂存的好友数据清除

    def delete(self):
        """
        删除好友
        """
        delitems = self.getListitems(self.menuflag)
        self.deleteItems(delitems)
        self.tmpuseritem.clear() # 暂存的好友数据清除

    def deleteItems(self, items, flag=1):
        """
        删除好友的具体操作
        items：好友们
        """
        for delitem in items:
            delitem.setData(0, Qt.ItemDataRole.CheckStateRole, QVariant())
            # 取消删除item的多选框，这句不写，批量操作时好友转移过去后还是带多选框的。
            if delitem.parent(): # 不能分组也删除
                pindex = delitem.parent().indexOfChild(delitem)
                dindex = self.searchuser(delitem)
                ishide = self.userslist[dindex]["ishide"]
                # 取得我们好友在当前分组下的索引。找到这个好友在userslist列表中的索引以及是否离线信息

                if flag == 1:
                    del self.userslist[dindex]
                    # 若不是批量操作状态下，则直接删除这些存储在userslist的对象

                fathergroup = delitem.parent()# 父节点
                findex = self.searchgroup(fathergroup)
                if ishide == 1:
                    self.grouplist[findex]["childishide"] -= 1
                    self.grouplist[findex]["childcount"] -= 1
                    # 要是这个好友状态是离线的，我们把grouplist相应的group字典信息修改：总数 - 1，离线数量 - 1
                else:
                    self.grouplist[findex]["childcount"] -= 1
                    # 否则只有：总数 - 1

                delitem.parent().takeChild(pindex)
                # 最后删除分组下的好友
            else: # 把删除好友的分组好友信息再次更新一下
                self.restatistic_op(delitem)

    def add(self, group, items):
        """
        分组中增加好友
        group：分组
        item：好友们
        """
        gindex = self.searchgroup(group)
        for item in items:
            aindex = self.searchuser(item)
            ishide = self.userslist[aindex]["ishide"]
            if ishide == 1:
                self.grouplist[gindex]["childishide"] += 1
                self.grouplist[gindex]["childcount"] += 1
            else:
                self.grouplist[gindex]["childcount"] += 1
            group.addChild(item)
            # 更新grouplist中的相应信息和实际情况，确保这些信息一致

            self.treeWidget.setCurrentItem(item)
            # 触发itemSelectionChanged信号，让分组上的数量再次更新一下

    def Batchoperation(self):
        """
        遍历分组下的所有好友，给它们加上checkState
        """
        self.menuflag *= -1
        # 是否批量操作的标志

        group = self.getListitems()[0].parent()
        childnum = group.childCount()
        for c in range(childnum):
            child = group.child(c)
            child.setCheckState(0, Qt.CheckState.Unchecked)

    def CancelBatchoperation(self):
        """
        遍历然后把分组好友的多选框信息全部清除
        """
        self.menuflag *= -1
        group = self.getListitems()[0].parent()
        childnum = group.childCount()
        for c in range(childnum):
            child = group.child(c)
            child.setData(0, Qt.ItemDataRole.CheckStateRole, QVariant())

    def isclick(self, item):
        """
        看看好友是否被选中
        """
        if item.checkState(0) == Qt.CheckState.Checked:
            if self.tmpuseritem.count(item) == 0:
                self.tmpuseritem.append(item)
        # 若好友的状态是Qt.CheckState.Checked（被选中），我们一定要先在tmpuseritem列表查查我们点击的好友对象是不是已经存在了。
        else:
            if len(self.tmpuseritem) > 0:
                if self.tmpuseritem.count(item) != 0:
                    i = self.tmpuseritem.index(item)
                    del self.tmpuseritem[i]
        # 如果tmpuseritem列表有好友的话，取消选中的时候，获取它的索引，然后将它从列表中删除。

    def renameItem(self):
        """
        设定好友备注
        """
        hituser = self.treeWidget.currentItem()
        uindex = self.searchuser(hituser)# 得到当前选定好友的索引
        unewname, isok = QInputDialog.getText(self, "提示信息", "请输入备注名称")
        if isok:
            if not unewname:
                QMessageBox.information(self, "提示", "备注名称不能为空哦")
            else:
                hituser.setText(0, unewname)
                self.userslist[uindex]["username"] = unewname

    def searchuser(self, hituser):
        """
        返回好友的索引
        """
        if isinstance(hituser, str):# 是好友名称吗？
            for i, u in enumerate(self.userslist):
                if u["username"] == hituser:
                    return i
        else:
            for i, u in enumerate(self.userslist):
                if u["user"] == hituser:
                    return i

    def restatistic(self, item, preitem):
        """
        针对分组的统计方法
        """
        if item:
            # 首先判断当前项目究竟是分组还是好友
            fathergroup = item.parent() 
            if fathergroup: # 对分组进行统计
                self.restatistic_op(fathergroup)
        elif preitem: # 分组内没有好友了
            fathergroup2 = preitem.parent()
            if fathergroup2:
                self.restatistic_op(fathergroup2)
                self.menuflag = 1

    def restatistic_op(self, itemorgroup):
        """
        根据分组对象我们在self.grouplist取到相应的好友数量、离线好友的数量，然后再设置分组名称
        """
        gindex = self.searchgroup(itemorgroup)
        totalcount = self.grouplist[gindex]["childcount"]
        hidecount = self.grouplist[gindex]["childishide"]
        fathergroupname = self.grouplist[gindex]["groupname"]
        fathergroupname += " " + str(totalcount - hidecount) + "/" + str(totalcount)
        itemorgroup.setText(0, fathergroupname)

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
        for itm in self.userslist:
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
            useritemindex = self.searchuser(username)
            if useritemindex: # 有好友才能找到，否则无法查找
                useritem = self.userslist[useritemindex]["user"]
                self.treeWidget.setCurrentItem(useritem)

    def addNewFriendDialog(self):
        """
        启动增加好友对话框
        """
        self.adduser = NewFriend(self) # 自定义增加好友对话框
        for g in self.grouplist:
            self.adduser.comboBox.addItem(g["groupname"])
        self.adduser.friendItem.connect(self.setnewFriend)
        self.adduser.exec()
    
    def setnewFriend(self, newname, newicon):
        """
        设置新增的好友
        newname：好友姓名
        newicon：好友头像路径
        """
        newitem = QTreeWidgetItem()
        font = QFont()
        font.setPointSize(16)
        newitem.setFont(0, font)
        newitem.setText(0, newname) # 好友姓名
        newitem.setTextAlignment(0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)
        newitem.setIcon(0, QIcon(newicon)) # 好友头像
        comboxinfo = self.adduser.comboBox.currentText() # 好友分组
        # 新增的好友在哪个分组呢，看这里
        
        cindex = self.searchgroup(comboxinfo)
        group = self.grouplist[cindex]["group"]
        self.grouplist[cindex]["childcount"] += 1
        userdic = {"user":newitem, "username":newname, "ishide":0} # 新的好友信息
        self.userslist.append(userdic)
        group.addChild(newitem)
        self.treeWidget.setCurrentItem(newitem)
        # 增加好友之后相关数据要更新一下
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    tim = TIM()
    tim.show()
    sys.exit(app.exec())