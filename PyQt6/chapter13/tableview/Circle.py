#coding = utf-8

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainter, QBrush,  QColor

class CircleRating():
    '''
    创建一个圆形类
    '''
    PaintingScaleFactor = 20  # 坐标缩放量

    def __init__(self, maxCount = 5):
        self.maxCount = maxCount # 默认是5个圆

    def paint(self, painter, rect):
        """
        圆圈的样式和数量
        """
        painter.save() # 保存当前绘制器状态
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)  # 抗锯齿
        painter.setPen(Qt.PenStyle.NoPen) # 画笔样式
        painter.setBrush(QBrush(QColor(Qt.GlobalColor.red))) # 红色
        yOffset = (rect.height() - self.PaintingScaleFactor) / 2  # 偏移量
        painter.translate(rect.x(), rect.y() + yOffset)  # 按给定偏移量平移坐标系
        painter.scale(self.PaintingScaleFactor, self.PaintingScaleFactor) # 按(sx,sy)缩放坐标系
        for i in range(self.maxCount): # 画圆
            painter.drawEllipse(QPointF(1.0, 0.5), 0.4, 0.4)
            painter.translate(1.0, 0.0)
        painter.restore() # 恢复当前绘制器状态