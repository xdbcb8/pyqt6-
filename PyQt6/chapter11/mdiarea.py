#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2023/08/06 15:13:31
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第11章第5节QMdiArea

import sys
import os
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QMenu, QLabel
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtCore import Qt, QDir, QPoint

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class DiyMdiSubWindow(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        self.moving = False # 是否移动标志
        self.offset = QPoint()

    # 重写与mouse相关的方法，以实现牌的拖动。由于牌没有标题栏，因此不重写这些方法将无法实现拖动

    def mousePressEvent(self, event):
        """
        按下鼠标左键
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """
        鼠标指针移动
        """
        if self.moving:
            global_pos = self.mapToParent(event.pos())  # 获取全局坐标
            self.move(global_pos - self.offset)

    def mouseReleaseEvent(self, event):
        """
        释放鼠标左键
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.moving = False
            
    def contextMenuEvent(self, event):
        """
        右键菜单
        """
        contextMenu = QMenu(self)
        exitAction = QAction("关闭", self)
        exitAction.triggered.connect(self.close)
        contextMenu.addAction(exitAction)
        contextMenu.exec(self.mapToGlobal(event.pos()))

class Card(QLabel):
    def __init__(self, num):
        super().__init__()
        self.num = num
        QDir.addSearchPath("res",f"{current_dir}\images")
        # 把每张牌的基本路径设置好
        pixmap = QPixmap(f"res:{self.num}.png")
        self.setPixmap(pixmap)
        self.setScaledContents(True)

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        '''
        界面初始设置
        '''
        self.setWindowTitle("QMdiArea举例")

        self.mid = QMdiArea()
        self.setCentralWidget(self.mid)
        # 新建一个QMdiArea类的对象，并将其设置为主窗口的中央小部件

        sendOnecardAct = QAction("发1张牌", self)
        sendOnecardAct.triggered.connect(self.sendOnecard)
        # 发1张牌命令

        sendFivecardsAct = QAction("随机5张牌", self)
        sendFivecardsAct.triggered.connect(self.sendFivecards)
        # 随机5张牌命令

        clearcardAct = QAction("清除牌", self)
        clearcardAct.triggered.connect(self.clearCards)
        # 清除牌命令

        foldcardAct = QAction("收牌", self)
        foldcardAct.triggered.connect(self.foldCards)
        # 收牌

        toolbar = self.addToolBar('工具栏')
        toolbar.addAction(sendOnecardAct)
        toolbar.addAction(sendFivecardsAct)
        toolbar.addAction(clearcardAct)
        toolbar.addAction(foldcardAct)
        #把上面的几个命令放到工具栏上

        self.show()
    
    def sendOnecard(self):
        '''
        随机一张牌，发出去。
        '''
        randomflag = self.randomsend(1)
        card = Card(randomflag)
        subcard = DiyMdiSubWindow()
        subcard.setWidget(card)
        self.mid.addSubWindow(subcard)
        subcard.setWindowFlags(Qt.WindowType.FramelessWindowHint) # 去除窗口标题栏
        subcard.resize(100, 150)
        subcard.show()
    
    def sendFivecards(self):
        '''
        随机5张牌
        '''
        randomflag = self.randomsend(5)
        for num in randomflag:
            # 遍历5张牌，发出去。
            subcard = DiyMdiSubWindow()
            card = Card(num)
            subcard.setWidget(card)
            self.mid.addSubWindow(subcard)
            subcard.setWindowFlags(Qt.WindowType.FramelessWindowHint) # 去除窗口标题栏
            subcard.resize(100, 150)
            subcard.show()
        
    def clearCards(self):
        '''
        清除牌
        '''
        self.mid.closeAllSubWindows()
        # 所有窗口关闭

    def foldCards(self):
        '''
        收牌
        '''
        self.mid.cascadeSubWindows()
        # 所有窗口级联模式排列
    
    def randomsend(self, num):
        '''
        发送方式：
        1、要是发1张牌，从cardlist中随机取一个元素返回就行了。
        2、要是随机发5张牌，从cardlist中随机取出一段包含有5个元素的列表。
        '''
        cardlist = ["2", "3", "4", "5", "6", "7", "8", "9", "10"]
        if num == 1:
            return random.choice(cardlist)
        elif num == 5:
            return random.sample(cardlist, 5)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec())