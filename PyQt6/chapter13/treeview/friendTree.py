#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   friendTree.py
@Time    :   2023/08/25 16:17:10
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第13章第2节QTreeView--自定义视图

import os
import random
import codecs
from PyQt6.QtWidgets import QTreeView, QMenu, QInputDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QBrush, QStandardItemModel, QAction, QStandardItem

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录的绝对路径

class FriendTree(QTreeView):
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.grouplist = [] # 分组信息列表存储
        self.userslist = [] # 用户信息列表存储
        self.initData()

    def initData(self):
        """
        数据初始化
        """
        self.treeModel = QStandardItemModel(self)
        self.setModel(self.treeModel)
        self.setColumnWidth(0, 50) # 列宽
        self.setStyleSheet("QTreeView{icon-size:70px}") # 头像图标
        self.treeModel.setHorizontalHeaderLabels(["好友"])  # 设置标题标签
        self.root = self.treeModel.invisibleRootItem() # 总的根节点
        self.creategroup("我的好友")
        self.expandAll() # 默认是好友展开

    def creategroup(self, groupname):
        """
        增加分组
        groupname：分组名称
        """
        hidernum = 0 # 统计离线好友
        group = QStandardItem()
        self.root.appendRow(group)
        # 新增一个分组（QStandardItem类型），这个分组是挂在self.treeView下的
        groupdic = {"group":group, "groupname":groupname, "childcount":0, "childishide":0}
        # 分组信息字典：包括分组名称、在线、离线人数
        for i in range(10):
            randname, randicon, isvip, ishider = self.createusers() # 创建一个好友，并返回姓名、头像、是否会员、是否离线
            child = self.newFriendItem([randname, randicon, isvip, ishider])
            if ishider == 1:
                # 是否离线
                hidernum += 1
            group.appendRow(child) # 将每个好友增加先前创建的group分组当中
        childnum = group.rowCount() # 统计每个分组下好友的数量
        lastchildnum = childnum - hidernum # 减去离线的数量就是在线好友的数量了
        groupdic["childcount"] = childnum
        groupdic["childishide"] = hidernum # 更新groupdic中的数据
        groupname += " " + str(lastchildnum) + "/" + str(childnum) # 将当前groupname设置成类似：我的好友 8/10 的样式
        group.setText(groupname) # 将给定列中显示的文本设置为给定文本，如：我的好友 8/10
        self.grouplist.append(groupdic) # 把分组加入到分组列表中
    
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
        isvip = random.randint(0, 5) # 是否会员
        ishider = random.randint(0, 5) # 是否离线
        randicon = QIcon(f"{iconpath}.png") # 好友在线头像
        if ishider == 1:
            randicon = QIcon(f"{iconpath}H.png") # 好友离线头像
        return randname, randicon, isvip, ishider

    def newFriendItem(self, info):
        """
        新好友项目节点
        info：好友属性，List类型
        """
        newFriend = QStandardItem() # 新朋友节点
        name = info[0] # 姓名
        icon = info[1] # 头像
        isvip = info[2] # 是否会员
        ishider = info[3] # 是否离线
        userdic = {"user":newFriend, "username":name, "iconPath":icon, "isvip":0, "ishide":0} # 单个好友字典数据
        self.userslist.append(userdic)
        newFriend.setText(name)
        font = QFont()
        font.setPointSize(16)
        newFriend.setFont(font)
        newFriend.setIcon(icon)
        newFriend.setTextAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)
        if isvip == 1:
            # 会员红名
            newFriend.setForeground(QBrush(Qt.GlobalColor.red))
            newFriend.setToolTip("会员红名尊享")
            userdic["isvip"] = 1
        if ishider == 1:
            # 是否离线
            userdic["ishide"] = 1
        return newFriend

    def contextMenuEvent(self, event):
        """
        右键菜单
        """
        hitIndex = self.indexAt(event.pos()) # 返回鼠标指针相对于接收事件的小部件的位置
        if hitIndex.isValid():
            hitItem = self.treeModel.itemFromIndex(hitIndex)
            if not hitItem.parent(): # 是否为根节点
                pgroupmenu = QMenu(self)
                pAddgroupAct = QAction("添加分组", pgroupmenu)
                pRenameAct = QAction("重命名分组", pgroupmenu)
                pDeleteAct = QAction("删除该组", pgroupmenu)
                pgroupmenu.addAction(pAddgroupAct)
                pgroupmenu.addAction(pRenameAct)
                pgroupmenu.addAction(pDeleteAct)
                pAddgroupAct.triggered.connect(self.addgroup)
                pRenameAct.triggered.connect(lambda:self.renamegroup(hitItem))
                if self.indexAbove(hitIndex) == self.root.index(): # 位置在最上面的分组不能删除
                    pDeleteAct.setEnabled(False)
                else:
                    pDeleteAct.triggered.connect(lambda:self.deletegroup(hitItem))
                pgroupmenu.popup(self.mapToGlobal(event.pos())) # 弹出菜单
            else:
                pItemmenu = QMenu(self)       
                pDeleteItemAct = QAction("删除好友", pItemmenu)
                pItemmenu.addAction(pDeleteItemAct)            
                pDeleteItemAct.triggered.connect(self.delete)
                if len(self.grouplist) > 1: # 分组数量大于1
                    pSubMenu = QMenu("转移好友至", pItemmenu)
                    pItemmenu.addMenu(pSubMenu)
                    for item_dic in self.grouplist:
                        if item_dic["group"] is not hitItem.parent():
                            pMoveAct = QAction(item_dic["groupname"] ,pItemmenu)
                            pSubMenu.addAction(pMoveAct)
                            pMoveAct.triggered.connect(self.moveItem)
                if len(self.getListitems()) == 1: # 我们选择的好友数量只能为1的时候，才能设定备注
                    pRenameItemAct = QAction("设定备注", pItemmenu)
                    pItemmenu.addAction(pRenameItemAct)            
                    pRenameItemAct.triggered.connect(lambda:self.renameItem(hitItem))
                pItemmenu.popup(self.mapToGlobal(event.pos()))
                #弹出菜单

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

    def renamegroup(self, hitgroup):
        """
        重命名分组，之后相关数据更新一下
        hitgroup：我们选中的分组
        """
        gnewname, isok = QInputDialog.getText(self, "提示信息", "请输入分组的新名称")
        if isok:
            if not gnewname:
                QMessageBox.information(self, "提示", "分组名称不能为空哦")
            else:
                hitgroup.setText(gnewname)
                gindex = self.searchgroup(hitgroup)
                self.grouplist[gindex]["groupname"] = gnewname
                self.restatistic_op(hitgroup) # 重新刷新好友在线情况

    def restatistic_op(self, itemorgroup):
        """
        根据分组对象我们在self.grouplist取到相应的好友数量、离线好友的数量，然后再设置分组名称
        """
        gindex = self.searchgroup(itemorgroup)
        totalcount = self.grouplist[gindex]["childcount"]
        hidecount = self.grouplist[gindex]["childishide"]
        fathergroupname = self.grouplist[gindex]["groupname"]
        fathergroupname += " " + str(totalcount - hidecount) + "/" + str(totalcount)
        itemorgroup.setText(fathergroupname)
                
    def deletegroup(self, hitItem):
        """
        删除分组
        hitItem：分组
        """
        gindex = self.searchgroup(hitItem)
        reply = QMessageBox.question(self, "警告", "确定要删除这个分组及其好友吗？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            row = hitItem.row()
            self.root.removeRow(row)  # 删除分组
            del self.grouplist[gindex] # 也要把在self.grouplist的数据也要删除
            
    def searchgroup(self, hitgroup):
        """
        hitgroup：分组名称或者对象
        根据分组返回分组对象在分组列表中的索引
        """
        if isinstance(hitgroup, str): # 根据分组名称返回分组对象在分组列表中的索引，好友转移分组使用
            for index, g in enumerate(self.grouplist):
                if g["groupname"] == hitgroup:
                    return index
        else:
            for index, group in enumerate(self.grouplist): # 根据分组对象返回分组对象在分组列表中的索引
                if group["group"] == hitgroup:
                    return index

    def delete(self):
        """
        删除好友
        """
        delitemsIndex = self.getListitems()
        self.deleteItems(delitemsIndex)

    def deleteItems(self, itemsIndex):
        """
        删除好友的具体操作
        itemsIndex：好友们在模型中的索引
        """
        for delitemIndex in itemsIndex[::-1]: # 把要删除的好友项目列表倒序，否则会出现删除错误
            delitem = self.treeModel.itemFromIndex(delitemIndex) # 根据模型索引返回具体的好友节点项目对象
            dindex = self.searchuser(delitem)
            ishide = self.userslist[dindex]["ishide"]
            # 找到待删除的好友在userslist列表中的索引以及是否离线信息
            del self.userslist[dindex] # 直接删除这些存储在userslist的对象
            fathergroup = delitem.parent()# 分组节点
            findex = self.searchgroup(fathergroup)
            if ishide == 1:
                self.grouplist[findex]["childishide"] -= 1
                self.grouplist[findex]["childcount"] -= 1
                # 要是这个好友状态是离线的，我们把grouplist相应的group字典信息修改：总数 - 1，离线数量 - 1
            else:
                self.grouplist[findex]["childcount"] -= 1
                # 否则只有：总数 - 1
            row = delitem.row() # 获得行号
            fathergroup.removeRow(row) # 删除分组下的好友
            self.restatistic_op(fathergroup) # 把删除好友的分组好友信息再次更新一下

    def moveItem(self):
        """
        移动好友
        """
        movelist = self.getListitems()
        togroupname = self.sender().text()
        mindex = self.searchgroup(togroupname) # 得到新的分组对象
        togroup = self.grouplist[mindex]["group"]
        # 分组的好友增加、删除
        self.add(togroup, movelist)
        self.deleteItems(movelist)
        
    def add(self, togroup, itemsIndex):
        """
        分组中增加好友
        togroup：目标分组
        itemsIndex：好友们在模型中的索引
        """
        gindex = self.searchgroup(togroup)
        for index in itemsIndex:
            item = self.treeModel.itemFromIndex(index)
            aindex = self.searchuser(item) # 从好友列表中取得好友的基本信息
            name = self.userslist[aindex]["username"] # 姓名
            icon = self.userslist[aindex]["iconPath"] # 头像
            isvip = self.userslist[aindex]["isvip"] # 是否会员
            ishide = self.userslist[aindex]["ishide"] # 是否离线
            # 更新grouplist中的相应信息和实际情况一致
            if ishide == 1:
                self.grouplist[gindex]["childishide"] += 1
                self.grouplist[gindex]["childcount"] += 1
            else:
                self.grouplist[gindex]["childcount"] += 1
            newItem = self.newFriendItem([name, icon, isvip, ishide]) # 构建新的好友对象转移
            togroup.appendRow(newItem)
            self.restatistic_op(togroup) # 让分组上的数量再次更新一下

    def getListitems(self):
        """
        获得选择的好友项目在模型中的索引
        """
        selectedIndex = self.selectionModel().selectedIndexes()
        return selectedIndex # 即返回所有选定的非隐藏项目列表的索引

    def renameItem(self, hituser):
        """
        设定好友备注
        hituser：好友
        """
        uindex = self.searchuser(hituser)# 得到当前选定好友的索引
        unewname, isok = QInputDialog.getText(self, "提示信息", "请输入备注名称")
        if isok:
            if not unewname:
                QMessageBox.information(self, "提示", "备注名称不能为空哦")
            else:
                hituser.setText(unewname)
                self.userslist[uindex]["username"] = unewname

    def searchuser(self, hituser):
        """
        返回好友在列表中的索引
        hituser：好友
        """
        for index, u in enumerate(self.userslist):
            if u["username"] == hituser:
                return index