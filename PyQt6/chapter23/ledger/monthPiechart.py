#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   monthPiechart.py
@Time    :   2024/03/20 16:57:24
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt

# 饼图

class PieChart():  
    def __init__(self, seriesList):
        series = QPieSeries()
        for item in seriesList:
            iteminfo = item[0] # 饼图一个切片的说明
            itemdata = item[1] # 饼图一个切片的数据
            if float(itemdata) < 0: # 饼图数据显示的时候大于0
                itemdata = -1 * itemdata

            # 创建一个饼形系列并添加数据
            series.append(f"{iteminfo}：{itemdata}", itemdata)

        # 为每个饼图切片设置标签和颜色  
        for slice in series.slices():  
            slice.setLabelVisible(True)  # 使标签可见  
            slice.setPen(QColor(Qt.GlobalColor.black))  # 设置边框颜色  
            slice.setLabelFont(QFont("Arial", 9))  # 设置标签字体和大小  

        # 创建一个图表并将系列添加到图表中  
        chart = QChart()  
        chart.addSeries(series)  
        chart.setTitle("当月二级支出分类TOP10")  
        chart.legend().setVisible(True) 
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)  # 设置图例位置   
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)  

        # 创建一个图表视图并将图表添加到视图中  
        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing) # 抗锯齿

    def getPie(self):
        return self.chart_view