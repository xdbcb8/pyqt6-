#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   numberGame.py
@Time    :   2023/09/27 07:13:29
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

# 第16章数字合并小游戏

import sys
import os
import random
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtCore import Qt, QMimeData, QPoint, QByteArray
from PyQt6.QtGui import QDrag, QFont, QPixmap

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class NumLabel(QLabel):
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.value = 0 # 每个自定义标签的初始值
        randomNum = self.getRandom() 
        self.setValue(randomNum)

    def getRandom(self): 
        """
        10~100随机数
        """
        randomNum = random.randint(10, 100)
        return randomNum

    def setValue(self, num):
        """
        设置标签显示数字
        num：待显示的数字
        """
        self.value = num
        font = QFont()
        font.setPointSize(30)
        self.setFont(font)
        self.setText(str(num))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter) # 居中显示
    
    def getValue(self):
        """
        以int型返回标签的数字
        """
        return self.value
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragStartPosition = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton: # 必须鼠标左键开始拖动
            return
        if (event.position().toPoint() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance(): # 拖动的距离必须足够
            return
        super().mouseMoveEvent(event)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("拖放举例")
        self. resize(800, 600)
        self.setAcceptDrops(True)
        self.numLabelList = [] # 暂存自定义标签对象
        self.initUI()
        self.show()

    def getRandomList(self, length):
        """
        生成随机坐标
        length：根据具体的窗体的尺寸生成随机坐标的上限
        你也可以换成任何自己喜欢的方式，只是让自定义标签随机分布而已
        """
        diyList = []
        interval = (length-80)//20
        first = 50
        for i in range(20):
            last = first + interval
            diyList.append(random.randint(first, last))
            first = last
        return random.sample(diyList, 10)

    def initUI(self):
        """
        自定义标签位置初始化
        """
        widthList = self.getRandomList(self.width()) # x坐标列表
        heightlist = self.getRandomList(self.height()) # y坐标列表
        points = zip(widthList, heightlist)
        for point in points:
            sx = point[0]
            sy = point[1]
            self.numLabelobj = NumLabel(self)
            self.numLabelobj.move(sx, sy)
            self.numLabelList.append(self.numLabelobj)

    def comparePoint(self, numLabelObj):
        """
        查看自定义标签是否和其他标签存在重合部分
        numLabelObj：待检查的标签
        """
        for item in self.numLabelList:
            if numLabelObj is not item:
                if numLabelObj.geometry().intersects(item.geometry()):
                    return item # 有重合的话就返回那个重合的自定义标签
        return False # 否则返回False

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-xdbcb8"):
            if event.source() == self: # 如果事件的源对象是当前对象，则将拖放操作的动作设置为移动操作，并接受该事件
                event.setDropAction(Qt.DropAction.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction() # 根据事件的类型和当前的状态来决定是否接受这个动作
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-xdbcb8"):
            self.itemNum.move(event.position().toPoint() - self.offset) # 将自定义标签移动到放下的位置
            if event.source() == self:
                event.setDropAction(Qt.DropAction.MoveAction)
                compareItem = self.comparePoint(self.itemNum)
                if compareItem:
                    number1 = self.itemNum.getValue()
                    number2 = compareItem.getValue()
                    newNumber = number1 + number2
                    self.itemNum.setValue(newNumber)
                    self.itemNum.adjustSize() # 自定义标签适应内容的大小
                    compareItem.move(-100, -100) # 让这个标签看不到
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-xdbcb8"):
            if event.source() == self: # 如果事件的源对象是当前对象，则将拖放操作的动作设置为移动操作，并接受该事件
                event.setDropAction(Qt.DropAction.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        self.itemNum = self.childAt(event.position().toPoint()) # 返回被拖动的自定义标签
        if self.itemNum:
            self.offset = QPoint(event.position().toPoint() - self.itemNum.pos()) # 返回光标坐标与自定义标签坐标的偏移量
            mimeData = QMimeData()
            mimeData.setData("application/x-xdbcb8", QByteArray())
            drag = QDrag(self)
            pixmap = QPixmap(f"{current_dir}\\heart.png")
            drag.setPixmap(pixmap)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width()//2, pixmap.height()//2))
            drag.exec(Qt.DropAction.MoveAction)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())