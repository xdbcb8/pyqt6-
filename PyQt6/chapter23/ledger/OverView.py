#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   OverView.py
@Time    :   2024/02/26 20:23:17
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, QDate
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from Ui_OverView import Ui_overViewWidget
from datamanagement import AccountManagement, FlowFunds
from monthPiechart import PieChart
from LineChart import LineChart

# 财务概况

class overViewWidget(QWidget, Ui_overViewWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.layout2 = QHBoxLayout(self.tab_2)
        self.tab_2.setLayout(self.layout2)
        self.layout3 = QHBoxLayout(self.tab_3)
        self.tab_3.setLayout(self.layout3)
        self.setOverview()

    def setOverview(self):
        """
        显示资产概况
        """
        accountM = AccountManagement()
        isok = accountM.loadALLassets()
        if isok:
            self.label_assets.setText(str(isok[0][0])) # 净资产
        self.flowFundM = FlowFunds()
        todayin, todayout = self.flowFundM.todayFlow() # 今天的收支
        monthin, monthout = self.flowFundM.monthFlow() # 这个月的收支
        yearin, yearout = self.flowFundM.yearFlow() # 今年的收支
        self.lineEdit_today_in.setText(str(todayin))
        self.lineEdit_today_out.setText(str(todayout))
        self.lineEdit_currentMonth_in.setText(str(monthin))
        self.lineEdit_currentMonth_out.setText(str(monthout))
        self.lineEdit_currentYear_in.setText(str(yearin))
        self.lineEdit_currentYear_out.setText(str(yearout))

    def setDateInterval(self):
        """
        设置默认的日期区间是当前月份的第一天和最后一天
        """
        firstDayOfMonth = QDate(QDate.currentDate().year(), QDate.currentDate().month(), 1) # 当前月份的第一天
        lastDayOfMonth = firstDayOfMonth.addMonths(1).addDays(-1) # 当前月份的最后一天
        return firstDayOfMonth.toString("yyyy-MM-dd"), lastDayOfMonth.toString("yyyy-MM-dd")

    def setOutPie(self):
        """
        设置支出分类饼图
        """
        start, end = self.setDateInterval()
        outList = self.flowFundM.outinFlow(start, end, "out")
        if outList:
            if len(outList) > 10:
                outList = outList[0:9]
            pie = PieChart(outList)
            pieview = pie.getPie()
            item = self.layout2.takeAt(0)
            if item: # 要是布局中有图形就先删除再添加
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.layout2.addWidget(pieview)

    def setOutLine(self):
        """
        设置支出折线图
        """
        start, end = self.setDateInterval()
        moneyList = self.flowFundM.dayFlow(start, end)
        if moneyList:
            line = LineChart(moneyList, "当月支出趋势图", "花费")
            lineview = line.getchart()
            item = self.layout3.takeAt(0)
            if item: # 要是布局中有图形就先删除再添加
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.layout3.addWidget(lineview)

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        查看当月财务数据
        index：索引
        """
        if index == 0:
            self.setOverview()
        elif index == 1:
            self.setOutPie()
        elif index == 2:
            self.setOutLine()