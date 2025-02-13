#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   LineChart.py
@Time    :   2024/02/07 20:21:40
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PyQt6.QtCore import Qt, QDate, QDateTime  
from PyQt6.QtGui import QPainter

# 折线图

class LineChart():  
    def __init__(self, moneyList, title, ytitle): 
        self.moneyList = moneyList
        self.cnt = len(self.moneyList)
        self.mindate = QDateTime.fromString(self.moneyList[0][0], "yyyy-MM-dd") # X轴的最小值
        self.maxdate = QDateTime.fromString(self.moneyList[self.cnt-1][0], "yyyy-MM-dd") # X轴的最大值
        self.max = float(self.moneyList[0][2]) # 某日的最大消费
        self.min = float(self.moneyList[0][3]) # 某日的最低消费

        # 创建折线系列  
        self.series = QLineSeries()  

        # 填充数据  
        self.fill_series()  

        # 创建图表并添加系列  
        chart = QChart()  
        chart.addSeries(self.series)  
        chart.setTitle(title)  
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # 设置x轴
        axisX = QDateTimeAxis()  
        axisX.setFormat("yyyy-MM-dd")  # 设置日期格式  
        axisX.setTitleText("日期")
        axisX.setRange(self.mindate, self.maxdate) # 设置轴的最小值和最大值（使用QDate对象）
        axisX.setTickCount(self.cnt)  # 设置轴以便按日期进行刻度划分，每天一个刻度
        axisX.setLabelsAngle(45)  # 轴标签的角度，合适的角度利于查看
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)

        # 设置Y轴
        axisY = QValueAxis()  
        axisY.setRange(self.min, self.max)
        axisY.setLabelFormat("%.2f")
        axisY.setTitleText(ytitle)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft) # Y轴在图表左侧

        # 创建图表视图  
        self.chart_view = QChartView(chart)  
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)  

    def fill_series(self):
        """
        填充数据
        """
        for item in self.moneyList:
            # 将QDate转换为整数以用于x轴（例如，使用toJulianDay()，这是从公元前4714年1月1日开始的连续天数）  
            date = QDate.fromString(item[0], "yyyy-MM-dd")
            x = date.toJulianDay()  
            money = item[1]
            # 将支出金额与日期添加到折线系列
            self.series.append(x, money)

    def getchart(self):
        # 返回图表
        return self.chart_view
