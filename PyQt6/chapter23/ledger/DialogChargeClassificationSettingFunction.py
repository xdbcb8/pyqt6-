#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogChargeClassificationSettingFunction.py
@Time    :   2024/02/03 17:51:10
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QDialog, QMenu, QInputDialog, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QAction
from Ui_DialogChargeClassificationSetting import Ui_DialogChargeClassificationSetting
from datamanagement import ClassificationManagement

# 分类设置

class DialogChargeClassificationSettingFunction(QDialog, Ui_DialogChargeClassificationSetting):

    def __init__(self, flag, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.flag = flag # 支出还是收入分类的标志
        self.initData()

    def createmodel(self):
        # 创建一个标准模型  
        model = QStandardItemModel()
        # 设置模型的列名
        if self.flag == "in":
            model.setHorizontalHeaderLabels(["收入分类"])
        else:
            model.setHorizontalHeaderLabels(["支出分类"])
    
        # 创建树形结构
        self.root_item = model.invisibleRootItem()

        # 创建分类节点
        # 一级分类
        classificationList = self.loadClassification(1)
        for classificationItem in classificationList:
            itemstr = classificationItem[0]
            item = QStandardItem(itemstr)
            # 二级分类
            subclassificationList = self.loadClassification(2, itemstr)
            if subclassificationList:
                for child in subclassificationList:
                    childItem = QStandardItem(child[0])
                    item.appendRow(childItem)
            self.root_item.appendRow(item)
        expandIndex = model.indexFromItem(self.root_item.child(0)) # 返回第一个一级分类节点的索引
        return model, expandIndex

    def initData(self):
        """
        数据初始化
        """
        self.classificationM = ClassificationManagement()
        self.model, expandIndex = self.createmodel()
        self.ChargeClassificationTree.setModel(self.model)
        self.ChargeClassificationTree.expand(expandIndex) # 将第一个一级分类节点展开
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
        self.ChargeClassificationTree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ChargeClassificationTree.customContextMenuRequested.connect(self.treecontextMenuEvent) # 节点上的右键菜单

    def loadClassification(self, level, classificationName=""):
        """
        载入一二级分类信息
        """
        if level == 1:
            classifications = self.classificationM.loadAllClassification(self.flag)
        elif level == 2:
            classifications = self.classificationM.loadAllSubClassification(classificationName, self.flag)
        return classifications
    
    def treecontextMenuEvent(self, pos):
        """
        右键菜单
        """
        hitIndex = self.ChargeClassificationTree.indexAt(pos) # 返回鼠标指针相对于接收事件的小部件的位置
        if hitIndex.isValid():
            hitItem = self.model.itemFromIndex(hitIndex)
            if self.flag == "in":
                inOrout = "收入"
            else:
                inOrout = "支出"
            if not hitItem.parent():
                classificationMenu = QMenu(self) # 一级分类上的右键菜单
                addclassificationAct = QAction(f"添加一级{inOrout}分类", classificationMenu)
                renameclassificationAct = QAction(f"重命名一级{inOrout}分类", classificationMenu)
                delclassificationAct = QAction(f"删除该一级{inOrout}分类", classificationMenu)
                addSubclassificationAct = QAction(f"添加二级{inOrout}分类", classificationMenu)
                if hitItem.rowCount() != 0: # 有子节点的根节点
                    classificationMenu.addActions([addclassificationAct, renameclassificationAct, delclassificationAct])
                else: # 无子节点的根节点
                    classificationMenu.addActions([addclassificationAct, renameclassificationAct, delclassificationAct, addSubclassificationAct])
                    addSubclassificationAct.triggered.connect(lambda:self.classificationFunciton(3, self.root_item, hitItem))
                clasLis = ['食品酒水', '消费购物', '居家生活', '行车交通', '交流通讯', '休闲娱乐', '人情费用', '宝宝费用', '出差旅游', '金融保险', '医疗教育', '装修费用', '其他杂项', '职业收入', '人情收入', '其他收入']
                if hitItem.text() in clasLis: # 这些一级分类不能删除和重命名
                    renameclassificationAct.setEnabled(False)
                    delclassificationAct.setEnabled(False)
                else:
                    renameclassificationAct.setEnabled(True)
                    delclassificationAct.setEnabled(True)
                classificationMenu.popup(self.ChargeClassificationTree.viewport().mapToGlobal(pos)) # 弹出菜单
                addclassificationAct.triggered.connect(lambda:self.classificationFunciton(0, self.root_item))
                renameclassificationAct.triggered.connect(lambda:self.classificationFunciton(1, self.root_item, hitItem))
                delclassificationAct.triggered.connect(lambda:self.classificationFunciton(2, self.root_item, hitItem))
            else:
                subclassificationMenu = QMenu(self) # 二级分类上的右键菜单
                addSubclassification = QAction(f"添加二级{inOrout}分类", subclassificationMenu)
                renameSubclassification = QAction(f"重命名二级{inOrout}分类", subclassificationMenu)
                delSubclassification = QAction(f"删除该二级{inOrout}分类", subclassificationMenu)
                if hitItem.parent().rowCount() == 1: # 每个一级分类至少保留一个二级分类
                    delSubclassification.setEnabled(False)
                else:
                    delSubclassification.setEnabled(True)
                subclassificationMenu.addActions([addSubclassification, renameSubclassification, delSubclassification])
                subclassificationMenu.popup(self.ChargeClassificationTree.viewport().mapToGlobal(pos)) # 弹出菜单
                addSubclassification.triggered.connect(lambda:self.classificationFunciton(3, self.root_item, hitItem.parent()))
                renameSubclassification.triggered.connect(lambda:self.classificationFunciton(4, self.root_item, hitItem))
                delSubclassification.triggered.connect(lambda:self.classificationFunciton(5, hitItem.parent(), hitItem))

    def classificationFunciton(self, type, root, classificationItem=None):
        """
        分类操作
        type：不同一级分类对应不同的添加方式
        root：根节点或一级节点
        classificationItem：一级节点或二级节点
        """
        if type == 0: # 添加一级分类
            classificationNameDN = QInputDialog.getText(self, "添加一级分类", "添加一级分类的名称")
            if classificationNameDN[1]:
                newclassificationName = classificationNameDN[0] # 添加的分类名称
                if not newclassificationName:
                    QMessageBox.information(self, "提示", "新的一级分类名称不能为空！")
                else:
                    self.addClassificationMenu(self.classificationM, newclassificationName, root)
        elif type == 1: # 重命名一级分类
            classificationNameDN = QInputDialog.getText(self, "重命名一级分类", "请填写新的一级分类的名称")
            if classificationNameDN[1]:
                newclassificationName = classificationNameDN[0] # 新的分类名称
                if not newclassificationName:
                    QMessageBox.information(self, "提示", "新的一级分类名称不能为空！")
                else:
                    self.renameClassificationMenu(self.classificationM, classificationItem, newclassificationName)
        elif type == 2: # 删除一级分类
            yesorno = QMessageBox.question(self, "删除一级分类", "确认删除吗？删除分类会影响整个记账程序的记录，请务必谨慎！", defaultButton=QMessageBox.StandardButton.No)
            if yesorno == QMessageBox.StandardButton.Yes:
                if classificationItem.rowCount() == 0:
                    self.delClassificationMenu(self.classificationM, classificationItem, root)
                else:
                    for i in range(classificationItem.rowCount()):
                        childItem = classificationItem.child(0) # 遍历删除一级分类下的二级分类
                        self.delsubClassificationMenu(self.classificationM, childItem, classificationItem, info=0) # 不显示成功删除二级分类的提示
                    self.delClassificationMenu(self.classificationM, classificationItem, root) # 最后删除一级分类
        elif type == 3: # 添加二级分类
            issubclassification = QInputDialog.getText(self, "二级分类", "请输入二级分类信息！")
            if issubclassification[1]:
                subclassificationName = issubclassification[0] # 子分类
                if not subclassificationName:
                    QMessageBox.information(self, "提示", "二级分类名称为空！")
                else:
                    self.setNormalsubclassification(subclassificationName, classificationItem)
            expandIndex = self.model.indexFromItem(classificationItem) # 返回添加二级节点的父节点索引
            self.ChargeClassificationTree.expand(expandIndex)
        elif type == 4: # 重命名二级分类名称
            subaccoutNameDN = QInputDialog.getText(self, "重命名二级分类", "请填写新的二级分类的名称")
            if subaccoutNameDN[1]:
                newsubclassificationName = subaccoutNameDN[0] # 新的分类名称
                if not newsubclassificationName:
                    QMessageBox.information(self, "提示", "新的二级分类名称为空！")
                else:
                    self.renameSubClassificationMenu(self.classificationM, classificationItem, newsubclassificationName)
        elif type == 5: # 删除二级分类
            yesorno = QMessageBox.question(self, "删除二级分类", "确认删除吗？删除二级分类会影响整个记账程序的记录，请务必谨慎！", defaultButton=QMessageBox.StandardButton.No)
            if yesorno == QMessageBox.StandardButton.Yes:
                subclassificationName = classificationItem.text() # 待删除的子分类名称
                self.delsubClassificationMenu(self.classificationM, classificationItem, root) # 删除二级分类

    def addClassificationMenu(self, dM, classification, root):
        """
        添加一级分类
        dM：分类操作类的对象
        classification：一级分类名称
        root：根节点
        """
        isok = dM.addClassification(classification, self.flag)
        if isok == "existed":
            QMessageBox.information(self, "提示", "不能输入重复的分类名称！")
        elif isok == "execut_classification_error":
            QMessageBox.warning(self, "提示", "一级分类添加失败！")
        elif isok == "success":
            QMessageBox.information(self, "提示", "一级分类添加成功！")
            newclassificationItem = QStandardItem(classification)
            root.appendRow(newclassificationItem)
            
    def renameClassificationMenu(self, dM, classificationItem, newclassification):
        """
        修改一级分类
        dM：分类操作类的对象
        classificationItem：一级分类节点对象
        newclassification：新的一级分类名称
        """
        isok = dM.queryClassificationID(newclassification, 1, self.flag)
        if isok:
            QMessageBox.information(self, "提示", "不能输入重复的分类名称！")
        else:
            old_classificationName = classificationItem.text() # 原有的分类名称
            isok2 = dM.renameclassification(old_classificationName, newclassification, self.flag)
            if isok2 == "execut_classification_error":
                QMessageBox.warning(self, "提示", "一级分类重命名失败！")
            elif isok2 == "success":
                QMessageBox.information(self, "提示", "一级分类重命名成功！")
                classificationItem.setText(newclassification)

    def delClassificationMenu(self, dM, classificationItem, root):
        """
        删除一级分类
        dM：分类操作类的对象
        classification：一级分类名称
        """
        delclassificationname = classificationItem.text() # 一级分类名称
        isok = dM.delClassification(delclassificationname, self.flag)
        if isok == "execut_classification_error":
            QMessageBox.warning(self, "提示", "一级分类删除失败！")
        elif isok == "execut_flowfunds_error":
            QMessageBox.warning(self, "提示", "分类流水删除失败！")
        elif isok == "execut_recentclassification_error":
            QMessageBox.warning(self, "提示", "最近使用分类删除失败！")
        elif isok == "success":
            QMessageBox.information(self, "提示", "一级分类删除成功！")
            root.removeRow(classificationItem.row())

    def renameSubClassificationMenu(self, dM, subclassificationItem, subnewclassification):
        """
        修改二级分类
        dM：分类操作类的对象
        subclassificationItem：二级分类节点对象
        subnewclassification：新的二级分类名称
        """
        isok = dM.queryClassificationID(subnewclassification, 2, self.flag)
        if isok:
            QMessageBox.information(self, "提示", "不能输入重复的分类名称！")
        else:
            old_classificationName = subclassificationItem.text() # 原有的分类名称
            isok2 = dM.renameSubclassification(old_classificationName, subnewclassification, self.flag)
            if isok2 == "execut_classification_error":
                QMessageBox.warning(self, "提示", "二级分类重命名失败！")
            elif isok2 == "success":
                QMessageBox.information(self, "提示", "二级分类重命名成功！")
                subclassificationItem.setText(subnewclassification)

    def delsubClassificationMenu(self, dM, subclassificationItem, classificationItem, info=1):
        """
        删除二级分类
        dM：分类操作类的对象
        subclassificationItem：二级分类节点对象
        classificationItem：一级分类节点对象
        """
        delsubclassificationname = subclassificationItem.text() # 二级分类名称
        isok = dM.delSubClassification(delsubclassificationname, self.flag)
        if isok == "execut_subclassification_error":
            QMessageBox.warning(self, "提示", "二级分类删除失败！")
        elif isok == "execut_flowfunds_error":
            QMessageBox.warning(self, "提示", "分类流水删除失败！")
        elif isok == "execut_recentclassification_error":
            QMessageBox.warning(self, "提示", "最近使用分类删除失败！")
        elif isok == "success":
            if info: # 是否提示信息的标志
                QMessageBox.information(self, "提示", "二级分类删除成功！")
            classificationItem.removeRow(subclassificationItem.row())

    def setNormalsubclassification(self, subclassification, classificationItem):
        """
        添加普通二级分类
        subclassification：二级分类
        classificationItem：一级分类节点对象
        """
        isok = self.classificationM.addSubClassification(subclassification, classificationItem.text(), self.flag)
        if isok == "existed":
            QMessageBox.information(self, "提示", "新增的二级分类重复！")
        elif isok == "execut_subclassification_error":
            QMessageBox.warning(self, "警告", "二级分类新增失败")
        elif isok == "success":
            subclassificationItem = QStandardItem(subclassification)
            classificationItem.appendRow(subclassificationItem)