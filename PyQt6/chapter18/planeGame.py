#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   planeGame.py
@Time    :   2023/10/21 09:48:47
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

# 第18章第5节飞机碰撞大挑战

import sys
import os
import random
from PyQt6.QtCore import QPointF, QTimer, QRectF, QRect, Qt
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QWidget, QMessageBox, QGraphicsView, QGraphicsItem, QGraphicsSceneMouseEvent

map_timer = QTimer() # 地图滚动间隔时间
timerEnemyPlane = QTimer() # 敌机出现的间隔时间
timerEnemyPlaneSpeed = QTimer() # 敌机的前进间隔时间

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

enemyPlaneList = [] # 敌机对象的列表

class Map(QGraphicsView):
    '''
    地图
    '''
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.resize(512, 768) # 地图的尺寸是512*768
        self.setWindowTitle("飞机碰撞大挑战")
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)
        # 保留最小化和关闭按钮
        backgroundPath = f"{current_dir}\\img\\background.jpg" # 地图背景路径
        self.mapUp = QPixmap(backgroundPath)
        self.mapDown = QPixmap(backgroundPath)
        self.mapUp_y = -768
        self.mapDown_y = 0
        self.mapSpeed = 2 # 地图每次滚动的速度
        map_timer.timeout.connect(self.mapScroll)
        map_timer.start(10) # 地图每次滚动的时间间隔

    def mapScroll(self):
        """
        每个时间间隔自动滚动地图，让地图看起来一直在滚动一样
        """
        self.viewport().update() # 强制刷新窗体绘图
        self.mapUp_y += self.mapSpeed
        if self.mapUp_y >= 0:
            self.mapUp_y = -768
        self.mapDown_y += self.mapSpeed
        if self.mapDown_y >= 768:
            self.mapDown_y = 0

    def drawBackground(self, painter, rect):
        """
        绘制背景图片
        """
        painter.drawPixmap(self.mapToScene(0, self.mapUp_y), self.mapUp)
        painter.drawPixmap(self.mapToScene(0, self.mapDown_y), self.mapDown)

class Bomb(QGraphicsItem):
    '''
    碰撞后爆炸
    '''
    def __init__(self):
        super().__init__()
        self.i = 1
        self.bombPath = f"{current_dir}\\img\\bomb1.png"
        self.bomb_timer = QTimer()
        self.bomb_timer.timeout.connect(self.picSwitch)
        self.bomb_timer.start(30) # 爆炸图片切换的时间间隔

    def picSwitch(self):
        '''
        爆炸过程图片切换
        '''
        self.i += 1
        self.bombPath = f"{current_dir}\\img\\bomb{self.i}.png"
        self.update() # 强制刷新
        if self.i > 6:
            self.bomb_timer.stop()
    
    def boundingRect(self):
        '''
        将图元的外边界定义为矩形，所有绘画必须限制在图元的边界矩形内。
        QGraphicsView使用它来确定图元是否需要重绘。
        '''
        return QRectF(-43, -48, 86, 95)

    def paint(self, painter, option, widget):
        '''
        画出爆炸的效果
        '''
        bombPix = QPixmap(self.bombPath)
        painter.drawPixmap(QRect(-43, -48, 86, 95), bombPix)

class Plane(QGraphicsItem):
    '''
    我方飞机
    '''
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        # 飞机可以移动

    def boundingRect(self):
        return QRectF(-50, -33, 100, 65)

    def paint(self, painter, option, widget):
        '''
        画出我方飞机
        '''
        planePath = f"{current_dir}\\img\\plane.png"
        planePix = QPixmap(planePath)
        painter.drawPixmap(QRect(-50, -33, 100, 65), planePix)

    def mousePressEvent(self, event:QGraphicsSceneMouseEvent):
        '''
        获取场景坐标和本地坐标
        '''
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        scenePos = event.scenePos()
        
        # 保存当前的一些信息
        self.m_pressedPos = scenePos # 鼠标按键按下的坐标
        self.m_startPos = self.pos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event:QGraphicsSceneMouseEvent):
        '''
        获取场景坐标和本地坐标
        '''
        scenePos = event.scenePos()

        # 计算坐标偏移
        dx = scenePos.x() - self.m_pressedPos.x()
        dy = scenePos.y() - self.m_pressedPos.y()

        # 设置我方飞机在场景中位置
        self.setPos(self.m_startPos + QPointF(dx, dy))
        self.update()

class Enemy(QGraphicsItem):
    '''
    敌机
    '''
    def __init__(self):
        super().__init__()
    
    def boundingRect(self):
        return QRectF(-50, -40, 100, 81)

    def paint(self, painter, option, widget):
        '''
        画出敌机
        '''
        enemyPath = f"{current_dir}\\img\\enemy.png"
        enemyPix = QPixmap(enemyPath)
        painter.drawPixmap(QRect(-50, -40, 100, 81), enemyPix)

# ----------下面是一些函数调用----------------#        

def enemyPlaneAttack(scene):
    '''
    敌机出现
    '''
    x = random.randint(-150, 150) # 随机坐标
    y = random.randint(-1000, -500)
    enemyPlane = Enemy()
    enemyPlaneList.append(enemyPlane) # 敌机放入到敌机列表中
    enemyPlane.setPos(QPointF(x, y)) # 设置敌机的场景坐标
    scene.addItem(enemyPlane)

def bombing(enemyPlane):
    '''
    爆炸出现
    '''
    scene = enemyPlane.scene() # 敌机所在场景
    bomb = Bomb()
    bomb.setPos(plane.pos())
    scene.addItem(bomb)

def enemyPlaneFlying(plane):
    '''
    敌机攻击
    '''
    for enemyPlane in enemyPlaneList:
        x = enemyPlane.x()
        y = enemyPlane.y() + 5
        enemyPlane.setPos(QPointF(x, y))
        if enemyPlane.collidesWithItem(plane): # 检测是否发生碰撞
            map_timer.stop()
            timerEnemyPlane.stop()
            timerEnemyPlaneSpeed.stop()
            plane.setVisible(False) # 我方飞机不可见
            enemyPlane.setVisible(False) # 敌机不可见
            bombing(enemyPlane) # 发生爆炸
            answer = QMessageBox.question(QWidget(), "询问", "你挂了！再来一次？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if answer == QMessageBox.StandardButton.No:
                QApplication.quit() # 不同意再来一次直接关闭
            else:
                enemyPlaneList.clear()
                map_timer.start()
                timerEnemyPlane.start()
                timerEnemyPlaneSpeed.start()
                plane.setVisible(True)
                plane.setPos(QPointF(0, 150))
                enemyPlane.setPos(0, 1000) # 把敌机移到这个坐标
                plane.scene().removeItem(enemyPlane) # 把敌机从场景中移除

def planeAttack(scene):
    '''
    我方飞机出现
    '''
    plane = Plane()
    plane.setPos(QPointF(0, 150)) # 飞机起始位置
    scene.addItem(plane)
    return plane

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = QGraphicsScene(-200, -200, 400, 400)
    plane = planeAttack(scene)

    timerEnemyPlane.timeout.connect(lambda:enemyPlaneAttack((scene)))
    timerEnemyPlane.start(1500)

    timerEnemyPlaneSpeed.timeout.connect(lambda:enemyPlaneFlying(plane))
    timerEnemyPlaneSpeed.start(5)

    gameMapView = Map(scene)
    gameMapView.setRenderHint(QPainter.RenderHint.Antialiasing) # 抗锯齿
    gameMapView.show()
    sys.exit(app.exec())