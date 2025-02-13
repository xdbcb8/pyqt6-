#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   imageView.py
@Time    :   2023/09/21 14:46:03
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

import sys
from PyQt6.QtWidgets import (QWidget, QApplication, QTreeView, QLabel, QSplitter, QScrollArea,
                             QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QMenu, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFileSystemModel, QAction, QImage, QPixmap, QTransform, QPainter
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter

class Button(QPushButton):
    def __init__(self, text, Parent=None):
        super().__init__(Parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed) # 设定控件尺寸的策略
        self.setText(text)

class ImageViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initData()
        self.printerObj = QPrinter() # 打印类的对象
        self.zoomFactor = 1.0 # 缩放因子

    def initUI(self):
        """
        界面构造
        """
        self.setWindowTitle("图片查看器")
        self.resize(800, 600)
        splitter = QSplitter(self)
        self.fileTree = QTreeView()
        splitter.addWidget(self.fileTree)
        rightWidget = QWidget()
        self.showPicLabel = QLabel()
        self.showPicLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored) # 会根据内容和窗口大小进行自动调整
        self.showPicLabel.setScaledContents(True)
        self.scroll = QScrollArea(rightWidget) # 图片QLabel的载体
        self.scroll.setWidget(self.showPicLabel)
        self.RotateClockButton = Button("顺转")
        self.RotateClockButton.setEnabled(False)
        self.RotateCounterButton = Button("逆转")
        self.RotateClockButton.setEnabled(False)
        self.RotateCounterButton.setEnabled(False)
        self.zoomInButton = Button("放大")
        self.zoomoutButton = Button("缩小")
        self.zoomInButton.setEnabled(False)
        self.zoomoutButton.setEnabled(False)
        self.moreButton = Button("更多")
        self.moreButton.setEnabled(False)
        self.printButton = Button("打印")
        self.printButton.setEnabled(False)

        menu = QMenu() # 更多菜单
        self.originalAction = QAction("原始尺寸", self, triggered=self.showOriginal)
        self.windowAction = QAction("适应窗口", self, checkable=True, triggered=self.showAdjust)
        menu.addAction(self.originalAction)
        menu.addSeparator()
        menu.addAction(self.windowAction)
        self.moreButton.setMenu(menu)
        # 按钮的布局
        layout1 = QGridLayout()
        layout1.addWidget(self.RotateClockButton, 0, 1)
        layout1.addWidget(self.zoomInButton, 0, 2)
        layout1.addWidget(self.RotateCounterButton, 1, 1)
        layout1.addWidget(self.zoomoutButton, 1, 2)
        layout1.addWidget(self.printButton, 0, 3)
        layout1.addWidget(self.moreButton, 1, 3)
        # 右侧窗体布局
        layout2 = QVBoxLayout()
        layout2.addWidget(self.scroll)
        layout2.addLayout(layout1)
        rightWidget.setLayout(layout2)
        splitter.addWidget(rightWidget)
        # 主窗体布局
        layoutMain = QHBoxLayout()
        layoutMain.addWidget(splitter)
        self.setLayout(layoutMain)
        self.show()
    
    def initData(self):
        """
        载入树形目录及数据初始化
        """
        self.model = QFileSystemModel()
        self.model.setRootPath('.')
        self.model.setNameFilters(["*.png", "*.jpg", "*.jpeg", "*.bmp"]) # 只显示这些类型的图片
        self.model.setNameFilterDisables(False) # 启用过滤器，默认值是False
        self.fileTree.setModel(self.model)
        self.fileTree.clicked.connect(self.on_item_clicked) # 单击目录或者图片
        self.RotateClockButton.clicked.connect(self.rotation_clock)
        self.RotateCounterButton.clicked.connect(self.rotation_counter_clock)
        self.zoomoutButton.clicked.connect(self.zoomOut)
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.printButton.clicked.connect(self.printPic)

    def on_item_clicked(self, index):
        """
        获取所选项的文件路径
        index：索引
        """
        if not self.model.isDir(index): # 非目录，即是图片
            file_info = self.model.fileInfo(index)
            pic_path = file_info.filePath() # 图片路径
            self.loadPicture(pic_path)

    def loadPicture(self, path):
        """
        载入图片
        path：图片路径
        """
        image = QImage(path)
        pixmap = QPixmap.fromImage(image)
        if not image.isNull():
            self.showPicLabel.setPixmap(pixmap)
            # 启用按钮
            self.RotateClockButton.setEnabled(True)
            self.RotateClockButton.setEnabled(True)
            self.RotateCounterButton.setEnabled(True)
            self.zoomInButton.setEnabled(True)
            self.zoomoutButton.setEnabled(True)
            self.printButton.setEnabled(True)
            self.moreButton.setEnabled(True)
            self.zoomFactor = 1.0
            if not self.windowAction.isChecked():
                self.showPicLabel.adjustSize() # 调整QLabel的大小以适合其内容

    def rotation_clock(self):
        """
        顺时针旋转
        """
        transform = QTransform() 
        # QTransform类指定坐标系的2D变换。
        # 转换指定如何平移，缩放，剪切，旋转或投影坐标系，通常在渲染图形时使用。
        transform.rotate(90)  # 顺时针旋转90°
        pixmap = self.showPicLabel.pixmap() # QLabel中的图像
        pixmapTransformed = pixmap.transformed(transform)  # 顺时针旋转
        self.showPicLabel.setPixmap(pixmapTransformed)
        self.showPicLabel.resize(self.zoomFactor * pixmapTransformed.size()) # 根据图像调整QLabel尺寸

    def rotation_counter_clock(self):
        """
        逆时针旋转
        """
        transform = QTransform()
        transform.rotate(-90)  # 逆时针旋转90°
        pixmap = self.showPicLabel.pixmap() # QLabel中的图像
        pixmapTransformed = pixmap.transformed(transform)  # 逆时针旋转
        self.showPicLabel.setPixmap(pixmapTransformed)
        self.showPicLabel.resize(self.zoomFactor * pixmapTransformed.size())

    def showOriginal(self):
        """
        显示原始尺寸
        """
        self.windowAction.setChecked(False)
        self.scroll.setWidgetResizable(False) 
        # 设置滚动区域是否应调整QLabel的大小，若参数False（默认值），则滚动区域将遵循其大小
        self.showPicLabel.adjustSize()
        self.zoomFactor = 1.0

    def showAdjust(self):
        """
        图片适应窗口
        """
        isAdjustSetting = self.windowAction.isChecked() # 判断是否适应窗体
        self.scroll.setWidgetResizable(isAdjustSetting) # 若参数为True，则滚动区域将自动调整小部件的大小，以避免滚动条
        if not isAdjustSetting:
            self.showOriginal()
        # 启用适应窗体后，以下按钮禁用
        self.RotateClockButton.setEnabled(not isAdjustSetting)
        self.RotateCounterButton.setEnabled(not isAdjustSetting)
        self.zoomInButton.setEnabled(not isAdjustSetting)
        self.zoomoutButton.setEnabled(not isAdjustSetting)
        self.originalAction.setEnabled(not isAdjustSetting)
        self.printButton.setEnabled(not isAdjustSetting)

    def printPic(self):
        """
        打印图片
        """
        printDialog = QPrintDialog(self.printerObj, self)
        pixmap = self.showPicLabel.pixmap() # QLabel中的图像
        if printDialog.exec():
            painterVar = QPainter(self.printerObj)
            rect = painterVar.viewport()
            size = pixmap.size()
            size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio) # 在给定矩形内，图像大小将缩放到尽可能大的矩形，从而保留长宽比
            painterVar.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painterVar.setWindow(pixmap.rect())
            painterVar.drawPixmap(0, 0, pixmap)

    def zoomIn(self):
        """
        图片放大
        """
        self.zoomFactor *= 1.05 # 每次放大5%
        pixmap = self.showPicLabel.pixmap() # QLabel中的图像
        self.showPicLabel.resize(self.zoomFactor * pixmap.size())

    def zoomOut(self):
        """
        图片缩小
        """
        self.zoomFactor *= 0.95 # 每次缩小5%
        pixmap = self.showPicLabel.pixmap() # QLabel中的图像
        self.showPicLabel.resize(self.zoomFactor * pixmap.size())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ImageViewWidget()
    sys.exit(app.exec())