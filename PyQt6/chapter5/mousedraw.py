#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mousedraw.py
@Time    :   2023/04/29 07:04:46
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 涂鸦板 - 基于PyQt6实现的简易绘图应用
# 功能说明：通过鼠标左键绘制红色线条，右键清除所有内容
# 完整程序位于本书配套资料的PyQt6\chapter5\mousedraw.py中

import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen  # 导入绘图相关类
from PyQt6.QtCore import Qt

class drawingTablet(QWidget):
    """
    涂鸦板类 - 继承自QWidget，实现鼠标绘图功能
    
    功能特点：
    - 左键拖动绘制红色线条
    - 右键点击清除所有绘图
    - 自动记录和显示所有绘制的线条
    """
    def __init__(self):
        """
        初始化涂鸦板窗口
        设置窗口大小和标题，并初始化存储线条的数据结构
        """
        super().__init__()
        self.setFixedSize(800, 600)  # 设置固定窗口大小为800x600像素
        
        # 数据结构说明：
        # paths是一个二维列表，用于存储所有绘制的线条
        # 每个子列表表示一条连续绘制的线段的所有坐标点
        # 初始化为包含一个空列表，表示可以开始绘制第一条线
        self.paths = [[]]  
        
        self.setWindowTitle("涂鸦板")

    def paintEvent(self, event):
        """
        重写绘画事件处理方法
        当窗口需要重新绘制时自动调用，或通过update()方法触发
        
        参数:
            event: QPaintEvent对象，包含绘画区域信息
        """
        # 每次执行update()方法时，都会调用绘图事件
        # 创建QPainter对象，用于在窗口上绘图
        painter = QPainter(self)
        
        # 设置画笔属性：红色，线宽2像素
        painter.setPen(QPen(Qt.GlobalColor.red, 2))  
        
        # 遍历所有线条路径
        for path in self.paths:
            # 对每条路径，绘制线段连接相邻的坐标点
            for i in range(len(path)-1):
                painter.drawLine(path[i], path[i + 1])

    def mousePressEvent(self, event):
        """
        重写鼠标按下事件处理方法
        
        参数:
            event: QMouseEvent对象，包含鼠标事件信息
        """
        # 判断是否按下左键
        if event.buttons() == Qt.MouseButton.LeftButton:
            # 记录当前鼠标位置作为线条的起点或延续点
            self.paths[-1].append(event.pos())
        # 判断是否按下右键
        elif event.buttons() == Qt.MouseButton.RightButton:
            # 清空所有路径数据，清除绘画内容
            self.paths.clear()
            # 重新添加一个空列表，以便可以继续绘制新线条
            self.paths = [[]]
        # 触发窗口重绘，显示更新后的内容
        self.update()

    def mouseMoveEvent(self, event):
        """
        重写鼠标移动事件处理方法
        
        参数:
            event: QMouseEvent对象，包含鼠标事件信息
        """
        # 当鼠标移动且左键被按下时（拖拽操作）
        if event.buttons() == Qt.MouseButton.LeftButton:
            # 记录当前鼠标位置，形成连续的线条
            self.paths[-1].append(event.pos())
            # 触发窗口重绘，实时显示绘制的线条
            self.update()

    def mouseReleaseEvent(self, event):
        """
        重写鼠标释放事件处理方法
        
        参数:
            event: QMouseEvent对象，包含鼠标事件信息
        """
        # 释放鼠标按键意味着当前线条绘制结束
        # 添加一个新的空列表，准备记录下一条线的坐标
        self.paths.append([])

if __name__ == "__main__":   
    app = QApplication(sys.argv)
    drawing = drawingTablet()
    drawing.show()
    sys.exit(app.exec())