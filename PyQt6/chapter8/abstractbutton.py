#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   abstractbutton.py
@Time    :   2023/06/20 06:52:45
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QAbstractButton举例：自定义一个圆形按钮

import sys
from PyQt6.QtWidgets import QAbstractButton, QApplication, QWidget
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QColor

class CircleButton(QAbstractButton):

    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.checked = False

    def paintEvent(self, event):
        """绘制控件"""
        size = self.rect().size() # 返回控件的内部几何图形尺寸（不包括任何窗口框架）
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing) # 消除图元边缘的锯齿
        qp.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform) # 平滑的像素映射转换
        qp.setBrush(QColor(225, 225, 225))  # 类灰色的颜色

        # 绘制圆形背景
        if self.isChecked():
            qp.setPen(QColor(201, 37, 88)) # 宝石红
        else:
            qp.setPen(QColor(225, 225, 225))
        qp.drawEllipse(0, 0, size.width() - 1, size.height() - 1)

        # 绘制圆形内部的选中标记
        if self.isChecked():
            qp.setBrush(QColor(201, 37, 88))
            margin = 5
            qp.drawEllipse(QRect(margin, margin, size.width() - margin * 2, size.height() - margin * 2))

    def sizeHint(self):
        """推荐尺寸"""
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        """最小推荐尺寸"""
        return QSize(36, 36)

    def isChecked(self):
        """返回按钮是否被选中"""
        return self.checked

    def setChecked(self, checked):
        """
        设置被选中状态
        checked：bool，True为选中
        """
        self.checked = checked

    def mouseReleaseEvent(self, event):
        """单击按钮时状态"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.checked = not self.checked
            self.clicked.emit(self.checked)
            self.update() # 立即刷新按钮画面

class Mywidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 100)
        self.setWindowTitle("自定义圆形按钮")
        button = CircleButton(self) # 默认为非选中状态
        button.clicked.connect(self.showRes)
        button.move(100, 40)
        # button.setChecked(True)  # 这里测试设置为选中状态
        self.show()

    def showRes(self, checked):
        if checked:
            print("选中了圆形按钮")
        else:
            print("未选中圆形按钮")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Mywidget()
    widget.show()
    sys.exit(app.exec())
