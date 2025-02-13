#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   accountbarchart.py
@Time    :   2024/02/09 10:02:44
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCharts import QChart, QChartView, QBarSet, QBarCategoryAxis, QValueAxis, QHorizontalBarSeries
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor

# 水平柱状图-账户

class AccountBarChart():  
    def __init__(self, accountList, maxormin, title):
        self.accountList = accountList # 账户数据
        cnt = len(self.accountList)
        setstr0List, setstr1List = [], [] # 分别代表收入和支出
        for i in range(cnt):
            setstr0List.append("<<0")
            setstr1List.append("<<0")
        for i in range(cnt):
            if self.accountList[i][1] > 0:
                setstr0List[i] = f"<<{self.accountList[i][1]}"
            else:
                setstr1List[i] = f"<<{self.accountList[i][1]}"

        setstr0 = " ".join(setstr0List)
        setstr1 = " ".join(setstr1List)
            
        # 创建柱状图数据系列
        set0 = QBarSet("金融类账户金额")
        set1 = QBarSet("负债类账户金额")

        eval("set0" + setstr0) # 数据动态填充
        eval("set1" + setstr1) 

        set0.setColor(QColor("red")) # 红色表示实实在在的金额
        set1.setColor(QColor("green")) # 绿色表示负债（即预支金额）

        series = QHorizontalBarSeries() # 水平柱状图系列
        series.append(set0) # 添加系列0
        series.append(set1) # 添加系列1
  
        # 创建图表并添加水平柱状图系列  
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations) # 出现的动画
        
        # X轴    
        axisX = QValueAxis()  
        axisX.setLabelFormat('%.2f') # 设置标签为浮点数格式，保留两位小数
        max = maxormin[0][0] # 最大值
        min = maxormin[0][1] # 最小值
        axisX.setRange(min, max)  # 设置X轴的范围  
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)  # 将X轴添加到图表的底部
        
        # Y轴
        categories = []
        for account in self.accountList:
            categories.append(account[0]+"："+str(account[1])) # Y轴的每个柱状图说明
        axisY = QBarCategoryAxis()
        axisY.append(categories)
        axisY.setLabelsAngle(0) # 说明的角度，这里是0度
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)  # 将Y轴添加到图表的左侧

        # 创建图表视图  
        self.chart_view = QChartView(chart)  
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)  # 抗锯齿
  
    def getBar(self):
        # 返回图表
        return self.chart_view