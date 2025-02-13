#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   table.py
@Time    :   2023/08/21 07:01:09
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第13章第3节QTableView--表格视图

import random
import sys
import codecs
import os
import time
from PyQt6.QtWidgets import QWidget, QApplication, QTableView, QPushButton, QHeaderView, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QItemSelectionModel, Qt
from TableDelegate import CircleshowD, SexD, BirthdateD, CountryD, IncomeD, ProgressD

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录的绝对路径

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dataInit()

    def initUI(self):
        """
        界面
        """
        self.setWindowTitle("QTableView举例")
        self.resize(1024, 800)
        addButton = QPushButton("增加")
        self.delButton = QPushButton("删除")
        self.delButton.setEnabled(False)
        hlayout = QHBoxLayout()
        hlayout.addStretch()
        hlayout.addWidget(addButton)
        hlayout.addWidget(self.delButton)
        self.tableView = QTableView()
        vlaytout = QVBoxLayout(self)
        vlaytout.addLayout(hlayout)
        vlaytout.addWidget(self.tableView)
        self.setLayout(vlaytout)
        self.show()
        addButton.clicked.connect(self.addRow)
        self.delButton.clicked.connect(self.delRow)
        self.tableView.clicked.connect(self.enableButton)

    def getBirthDate(self):
        '''
        随机出生日期
        '''

        a1 = (1990, 1, 1, 0, 0, 0, 0, 0, 0)  # 设置开始日期时间元组（1990-01-01 00：00：00）
        a2 = (2022, 12, 31, 23, 59, 59, 0, 0, 0)  # 设置结束日期时间元组（2022-12-31 23：59：59）

        start = time.mktime(a1)  # 生成开始时间戳
        end = time.mktime(a2)  # 生成结束时间戳

        t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
        randomtime = time.localtime(t)  # 将时间戳生成时间元组
        randomdate = time.strftime("%Y/%m/%d", randomtime)  # 将时间元组转成格式化字符串
        return randomdate
    
    def getname(self):
        """
        随机姓名
        """
        with codecs.open(f"{current_dir}\\res\\name.txt", "r", "utf-8") as f:
            nameList = f.read().split("\r\n")
            frineName = random.choice(nameList) # 随机姓名
            return frineName

    def getClient(self):
        '''
        随机客户信息
        '''
        level = random.randint(1, 5)  # 随机客户等级1-5级
        name = self.getname()  # 随机姓名
        sex = random.choice(['男', '女'])  # 随机性别
        birthdate = self.getBirthDate()  # 随机日期
        nationality = random.choice(['中国', '美国', '英国', '日本', '俄罗斯'])  # 随机国籍
        income = random.randint(8, 100)  # 随机年收入
        progress = random.randint(10, 100)  # 随机进度
        vip = random.randint(0, 1)  # 随机vip
        return [level, name, sex, birthdate, nationality, income, progress, vip]

    def dataInit(self):
        """
        表格初始化
        """
        self.table_Row = 5  # 原始表格数据为5行
        self.table_Column = 8 # 原始表格数据为8列

        self.tableView.verticalHeader().setDefaultSectionSize(22)  # 默认行高22像素
        self.tableView.setAlternatingRowColors(True)  # 交替行颜色

        self.model = QStandardItemModel(self.table_Row, self.table_Column, self)
        self.tableView.setModel(self.model)  # 设置数据模型

        headerTitle = ['客户等级', '客户姓名', '客户性别', '出生年月', '客户国籍', '客户年均收入（万元）', '洽谈进度', '是否VIP']
        self.model.setHorizontalHeaderLabels(headerTitle)  # 设置表头

        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # 列宽自动分配

        self.selectionModel = QItemSelectionModel(self.model)  # Item选择模型
        self.tableView.setSelectionModel(self.selectionModel)

        for i in range(self.table_Row):
            for j in range(self.table_Column-1):
                clientList = self.getClient()  # 随机客户数据
                client = QStandardItem(str(clientList[j]))
                self.model.setItem(i, j, client)
                self.model.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)  # 表格内容居中

            vipItem = QStandardItem("VIP")  # VIP多选框为选择状态
            if clientList[self.table_Column-1] == 0:
                vipItem.setCheckState(Qt.CheckState.Unchecked)
            else:
                vipItem.setCheckState(Qt.CheckState.Checked)
            vipItem.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)  # 可选、可多选、可启用
            self.model.setItem(i, self.table_Column-1, vipItem)
            self.model.item(i, self.table_Column-1).setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)  # VIP表格内容居中

###########################以下为代理设置##############################

        levelList=["一级", "二级", "三级", "四级", "五级"]
        self.circleD = CircleshowD()
        self.circleD.setItems(levelList)
        self.tableView.setItemDelegateForColumn(0, self.circleD)  # 客户等级显示为圆圈

        sexList=["男", "女"]
        self.sexD = SexD()
        self.sexD.setItems(sexList)
        self.tableView.setItemDelegateForColumn(2, self.sexD)  # 客户性别代理

        self.birthdateD= BirthdateD()
        self.tableView.setItemDelegateForColumn(3, self.birthdateD)  # 客户生日代理
    
        countryList=['中国', '美国', '英国', '日本', '俄罗斯', '未知']
        self.countryD = CountryD()
        self.countryD.setItems(countryList)
        self.tableView.setItemDelegateForColumn(4, self.countryD)  # 客户国籍代理

        self.incomeD = IncomeD()
        self.tableView.setItemDelegateForColumn(5, self.incomeD)  # 客户收入代理

        self.progressD = ProgressD()
        self.tableView.setItemDelegateForColumn(6, self.progressD)  # 客户收入代理

###########################以下为按钮功能##############################
    
    def delRow(self):
        """
        删除当前选中的行
        """
        currentIndex = self.selectionModel.currentIndex()  # 获取当前选中行的模型索引
        self.model.removeRow(currentIndex.row())  # 删除当前行
        self.delButton.setEnabled(False) # 删除一行后删除按钮禁用
        if self.model.rowCount() == 0:
            self.delButton.setEnabled(False)
    
    def enableButton(self):
        """
        选中某一行时可进行的操作
        """
        self.delButton.setEnabled(True)  # 删除按钮被启用

    def addRow(self):
        """
        新增用户
        """
        newClientList = self.getClient()  # 新增客户数据
        itemList = []  # 对象列表
        for j in range(self.table_Column-1):
            client = QStandardItem(str(newClientList[j]))
            itemList.append(client)

        vipItem = QStandardItem("VIP")  # VIP多选框为选择状态
        if newClientList[self.table_Column-1] == 0:
            vipItem.setCheckState(Qt.CheckState.Unchecked)
        else:
            vipItem.setCheckState(Qt.CheckState.Checked)
        vipItem.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)  # 可选、可多选、可启用
        itemList.append(vipItem)

        self.model.appendRow(itemList)  # 新增一行数据

        for j in range(self.table_Column):
            self.model.item(self.model.rowCount()-1, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)  # 新增表格内容居中

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())