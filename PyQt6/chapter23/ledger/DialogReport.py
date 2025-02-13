#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogReport.py
@Time    :   2024/02/27 09:11:25
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, QDate
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from Ui_DialogReport import Ui_Form_report
from LineChart import LineChart
from datamanagement import AccountManagement, ClassificationManagement
from accountbarchart import AccountBarChart
from classificationbarchart import ClassificationBarChart

# 报表

class Form_report(QWidget, Ui_Form_report):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.initData()
        self.assertsLine()

    def initData(self):
        """
        数据初始化
        """
        self.accountM = AccountManagement()
        self.classificationM = ClassificationManagement()
        currentYear = QDate.currentDate().year() # 当前的年份
        date1 = QDate(currentYear, 1, 1) # 本年度第一天
        date2 = QDate(currentYear, 12, 31) # 本年度的最后一天
        self.dateEditS.setDate(date1)
        self.dateEditE.setDate(date2)
        self.dateS = date1.toString("yyyy-MM-dd") # 开始日期
        self.dateE = date2.toString("yyyy-MM-dd") # 结束日期
        self.layout1 = QHBoxLayout(self.tab)
        self.tab.setLayout(self.layout1)
        self.layout2 = QHBoxLayout(self.tab_2)
        self.tab_2.setLayout(self.layout2)
        self.layout3 = QHBoxLayout(self.tab_3)
        self.tab_3.setLayout(self.layout3)
        self.layout4 = QHBoxLayout(self.tab_4)
        self.tab_4.setLayout(self.layout4)
        self.layout5 = QHBoxLayout(self.tab_5)
        self.tab_5.setLayout(self.layout5)
        self.layout6 = QHBoxLayout(self.tab_6)
        self.tab_6.setLayout(self.layout6)
        self.layout7 = QHBoxLayout(self.tab_7)
        self.tab_7.setLayout(self.layout7)

    def assertsLine(self):
        """
        显示净资产趋势图
        """
        moneyList, maxinList = self.accountM.loadassets(self.dateS, self.dateE) # 按月的净资产和其中的最大最小值
        if moneyList and maxinList:
            moneyList[0].append(maxinList[0][0])
            moneyList[0].append(maxinList[0][1])
            line = LineChart(moneyList, "年度净资产趋势图", "金额")
            view = line.getchart()
            item = self.layout1.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.layout1.addWidget(view)

    def balanceBar(self):
        """
        显示一级账户余额
        """
        moneyList, maxinList = self.accountM.loadAccountBalance() # 一级账户的金额和其中的最大最小值
        if moneyList and maxinList:
            bar = AccountBarChart(moneyList, maxinList, "一级账户分析")
            view = bar.getBar()
            item = self.layout5.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.layout5.addWidget(view)

    def subbalanceBar(self):
        """
        显示二级账户余额
        """
        submoneyList, submaxinList = self.accountM.loadSubAccountBalance() # 二级账户的金额和其中的最大最小值
        if submoneyList and submaxinList:
            bar = AccountBarChart(submoneyList, submaxinList, "二级账户分析")
            view = bar.getBar()
            item = self.layout2.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.layout2.addWidget(view)

    def classificationoutBar(self, flag):
        """
        一级支出分类
        """
        color = "Green" # 支出的颜色是绿色
        title = "一级支出分类分析" # 标题
        moneyList, maxinList = self.classificationM.loadClassificationflow(self.dateS, self.dateE, flag)
        if moneyList and maxinList:
            bar = ClassificationBarChart(moneyList, maxinList, title, color)
            view = bar.getBar()
            item = self.layout6.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    self.layout6.removeWidget(widget)
                    widget.deleteLater()
            self.layout6.addWidget(view)

    def subclassificationoutBar(self, flag):
        """
        二级支出分类
        """
        color = "Green" # 支出的颜色是绿色
        title = "二级支出分类TOP10分析" # 标题
        submoneyList, submaxinList = self.classificationM.loadsubClassificationflow(self.dateS, self.dateE, flag)
        if submoneyList and submaxinList:
            bar = ClassificationBarChart(submoneyList, submaxinList, title, color)
            view = bar.getBar()
            item = self.layout3.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    self.layout3.removeWidget(widget)
                    widget.deleteLater()
            self.layout3.addWidget(view)

    def classificationinBar(self, flag):
        """
        一级收入分类
        """
        color = "Red" # 收入的颜色是红色
        title = "一级收入分类分析" # 标题
        moneyList, maxinList = self.classificationM.loadClassificationflow(self.dateS, self.dateE, flag)
        if moneyList and maxinList:
            bar = ClassificationBarChart(moneyList, maxinList, title, color)
            view = bar.getBar()
            item = self.layout7.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    self.layout7.removeWidget(widget)
                    widget.deleteLater()
            self.layout7.addWidget(view)

    def subclassificationinBar(self, flag):
        """
        二级收入分类
        """
        color = "Red" # 收入的颜色是红色
        title = "二级收入分类分析" # 标题
        submoneyList, submaxinList = self.classificationM.loadsubClassificationflow(self.dateS, self.dateE, flag)
        if submoneyList and submaxinList:
            bar = ClassificationBarChart(submoneyList, submaxinList, title, color)
            view = bar.getBar()
            item = self.layout4.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    self.layout4.removeWidget(widget)
                    widget.deleteLater()
            self.layout4.addWidget(view)

    def setWidgetEnable(self, isenable):
        """
        设置相关控件是否禁用，涉及日期选择和筛选按钮
        isenable：是否禁用的标志
        """
        if isenable:
            self.dateEditE.setEnabled(True)
            self.dateEditS.setEnabled(True)
            self.pushButton.setEnabled(True)
        else:
            self.dateEditE.setEnabled(False)
            self.dateEditS.setEnabled(False)
            self.pushButton.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        筛选
        """
        self.dateS = self.dateEditS.date().toString("yyyy-MM-dd")
        self.dateE = self.dateEditE.date().toString("yyyy-MM-dd")
        scurrentIndex= self.tabWidget.currentIndex()
        self.on_tabWidget_currentChanged(scurrentIndex)
       

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        标签页的切换
        """
        if index == 0: # 净资产趋势图
            self.assertsLine()
            self.setWidgetEnable(True)
        elif index == 1: # 一账户余额分析，余额不需要通过日期来筛选，只要知道多少就行了
            self.balanceBar()
            self.setWidgetEnable(False)
        elif index == 2: # 二账户余额分析
            self.subbalanceBar()
            self.setWidgetEnable(False)
        elif index == 3: # 一级支出分析
            self.classificationoutBar("out")
            self.setWidgetEnable(True)
        elif index == 4: # 二级支出分析
            self.subclassificationoutBar("out")
            self.setWidgetEnable(True)
        elif index == 5: # 一级收入分析
            self.classificationinBar("in")
            self.setWidgetEnable(True)
        elif index == 6: # 二级收入分析
            self.subclassificationinBar("in")
            self.setWidgetEnable(True)