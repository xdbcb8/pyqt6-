#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   classificationbarchart.py
@Time    :   2024/02/09 10:02:33
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCharts import QChart, QChartView, QBarSet, QBarCategoryAxis, QValueAxis, QHorizontalBarSeries  
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor

# 水平柱状图-分类

class ClassificationBarChart():  
    def __init__(self, classificationList, maxormin, title, color):
        self.classificationList = classificationList # 分类数据
        cnt = len(self.classificationList)
        setstr0List = []
        for i in range(cnt):
            setstr0List.append("<<0")

        for i in range(cnt): # 等于0就不做变更
            if self.classificationList[i][1] != 0:
                setstr0List[i] = f"<<{self.classificationList[i][1]}"

        setstr0 = " ".join(setstr0List)
            
        # 创建柱状图数据系列
        set0 = QBarSet("金额")

        eval("set0" + setstr0) # 数据动态填充

        set0.setColor(QColor(color)) # 颜色          

        series = QHorizontalBarSeries() # 水平柱状图
        series.append(set0)  
  
        # 创建图表并添加系列  
        chart = QChart()  
        chart.addSeries(series)  
        chart.setTitle(title) 
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # X轴  
        axisX = QValueAxis()  
        axisX.setLabelFormat('%.2f') # 设置标签为浮点数格式，保留两位小数
        max = maxormin[0][0] # 最大值
        min = maxormin[0][1] # 最小值
        axisX.setRange(min, max)  # 设置X轴的范围
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)  # 将X轴添加到图表的底部

        # Y轴
        categories = []
        for classification in self.classificationList:
            categories.append(classification[0]+"："+str(classification[1])) # Y轴的每个柱状图说明
        axisY = QBarCategoryAxis()  
        axisY.append(categories)
        axisY.setLabelsAngle(0)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)  # 将Y轴添加到图表的左侧

        # 创建图表视图  
        self.chart_view = QChartView(chart)  
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)  
  
    def getBar(self):
        # 返回图表
        return self.chart_view