#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   six.py
@Time    :   2023/04/17 19:07:47
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 完整程序位于本书配套资料的PyQt6\chapter4\diyWidget.py中

# 六角星窗体 - 使用PyQt6实现的异形窗口示例
# 通过图片蒙版技术创建非矩形的窗口界面

import sys
import os
# 导入PyQt6所需模块
from PyQt6.QtWidgets import QWidget, QApplication  # 基础窗口部件和应用程序类
from PyQt6.QtGui import QPixmap, QPainter          # 用于图像处理和绘制
from PyQt6.QtCore import Qt                        # 包含Qt框架的核心功能和枚举

# 获取当前脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

class DIYWidget(QWidget):
    """
    自定义窗口部件类，用于创建六角星形的异形窗口
    
    继承自QWidget，通过图片蒙版技术实现非矩形窗口，
    并支持鼠标拖动和右键关闭功能
    """
    def __init__(self):
        """初始化自定义窗口部件"""
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        初始化用户界面，设置窗口大小、形状和外观
        """
        # 加载六角星图片作为窗口蒙版和显示内容
        pixmap = QPixmap(f"{current_dir}\\six.png")
        # 设置窗口大小与图片大小一致
        self.resize(pixmap.size())
        # 设置窗口蒙版，使窗口形状与图片中非透明区域一致
        self.setMask(pixmap.mask())
        # 设置窗口背景透明，消除异形窗口边缘可能出现的毛边
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        """
        处理鼠标按下事件，实现拖动窗口和右键关闭功能
        
        参数:
            event: QMouseEvent对象，包含鼠标事件的相关信息
        """
        # 鼠标左键按下时，计算鼠标位置与窗口左上角的偏移量，用于拖动窗口
        if event.button() == Qt.MouseButton.LeftButton:
            # 将PyQt6的QPointF转换为QPoint，计算鼠标全局位置与窗口框架左上角的差值
            self.dragPosition = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        # 鼠标右键按下时，关闭窗口
        elif event.button() == Qt.MouseButton.RightButton:
            self.close()

    def mouseMoveEvent(self, event):
        """
        处理鼠标移动事件，实现窗口拖动功能
        
        参数:
            event: QMouseEvent对象，包含鼠标事件的相关信息
        """
        # 当鼠标左键按住并移动时，根据鼠标当前位置和之前记录的偏移量移动窗口
        if event.buttons() == Qt.MouseButton.LeftButton:
            # 计算新的窗口左上角坐标并移动窗口
            self.move(event.globalPosition().toPoint() - self.dragPosition)
 
    def paintEvent(self, event):
        """
        处理窗口绘制事件，绘制六角星图片
        
        参数:
            event: QPaintEvent对象，包含绘制事件的相关信息
        """
        # 创建绘图对象
        p = QPainter(self)
        # 在窗口的左上角(0, 0)位置绘制六角星图片
        p.drawPixmap(0, 0, QPixmap(f"{current_dir}\\six.png"))

if __name__ == "__main__":
    # 创建Qt应用程序实例
    app = QApplication(sys.argv)
    # 创建自定义窗口实例
    diy = DIYWidget()
    # 显示窗口
    diy.show()
    # 运行应用程序的事件循环，并在结束时退出程序
    sys.exit(app.exec())