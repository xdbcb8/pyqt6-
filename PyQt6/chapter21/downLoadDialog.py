#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   downLoadDialog.py
@Time    :   2023/12/04 18:21:33
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

# 第21章简单浏览器--下载对话框

import os
from PyQt6.QtWidgets import (QDialog, QGridLayout, QDialogButtonBox, QLabel, QLineEdit, QComboBox, QPushButton, 
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import QStandardPaths, pyqtSignal
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest

class DownLoadDialog(QDialog):
    downloadStart = pyqtSignal(QWebEngineDownloadRequest, str, str) # 下载开始的信号

    def __init__(self, item, Parent=None):
        super().__init__(Parent)
        self.downLoadItem = item # QWebEngineDownloadRequest对象
        self.resize(400, 200)
        self.setWindowTitle("新建下载任务")

        layout = QGridLayout(self)
        layout.addWidget(QLabel("文件名"), 0, 0)
        self.downLoadLine = QLineEdit()
        self.downLoadName = self.downLoadItem.downloadFileName() # 下载的文件名
        self.downLoadLine.setText(self.downLoadName) # 下载的文件名
        self.downLoadLine.setClearButtonEnabled(True)
        layout.addWidget(self.downLoadLine, 0, 1)
        self.sizeLabel = QLabel() 
        size = self.downLoadItem.totalBytes() # 下载文件的大小
        self.sizeLabel.setText(f"{self.UnitConversion(size)}")
        layout.addWidget(self.sizeLabel, 0, 2)
        layout.addWidget(QLabel("保存到"), 1, 0)
        self.downLoadBox = QComboBox() 
        layout.addWidget(self.downLoadBox, 1, 1)
        button = QPushButton("自定义下载目录")
        layout.addWidget(button, 1, 2)
        buttonBox = QDialogButtonBox()
        buttonOK = buttonBox.addButton("开始下载", QDialogButtonBox.ButtonRole.AcceptRole)
        buttonCancel = buttonBox.addButton("取消下载", QDialogButtonBox.ButtonRole.RejectRole)
        layout.addWidget(buttonBox, 2, 1)
        self.setLayout(layout)
        self.path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation) # 默认下载路径（桌面）
        self.downLoadName = self.downLoadLine.text() # 默认文件名
        self.downLoadBox.addItems(["桌面", "我的文档", "下载", "清除其他目录..."])

        self.downLoadBox.textActivated.connect(self.pathChoice) # 选择下载目录
        button.clicked.connect(self.getDownLoadPath) # 自定义下载目录
        buttonOK.clicked.connect(self.actionDialog) # 开始下载
        buttonCancel.clicked.connect(self.dialogReject) # 取消下载

    def UnitConversion(self, size):
        """
        单位转换
        size：文件大小
        """
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024*1024:
            return f"{size/1024:.2f} KB"
        elif size < 1024*1024*1024:
            return f"{size/pow(1024, 2):.2f} MB"
        else:
            return f"{size/pow(1024, 3):.2f} GB"

    def actionDialog(self):
        """
        准备下载
        """
        if not self.downLoadLine.text():
            QMessageBox.information(self, "提示", "下载的文件名没有设置")
        else:
            self.downLoadName = self.downLoadLine.text().strip()
            self.downloadStart.emit(self.downLoadItem, self.path, self.downLoadName)
            # 开始下载信号发射
            self.accept()

    def dialogReject(self):
        """
        取消对话框
        """
        self.downLoadItem.cancel() # 取消下载
        self.reject()

    def closeEvent(self, event):
        """
        重写关闭对话框
        """
        self.downLoadItem.cancel() # 取消下载
        return super().closeEvent(event)

    def pathChoice(self, text):
        """
        选择下载路径
        text：项目文本
        """
        if text == "桌面":
            self.path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation) # 桌面
        elif text == "我的文档":
            self.path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation) # 我的文档
        elif text == "下载":
            self.path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation) # 下载
        elif text == "清除其他目录...":
            self.downLoadBox.clear()
            self.downLoadBox.addItems(["桌面", "我的文档", "下载", "清除其他目录..."])
            self.path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation) # 桌面
        else:
            self.path = self.downLoadBox.currentText()
    
    def getDownLoadPath(self):
        """
        自定义下载路径
        """
        pathTuple = QFileDialog.getSaveFileName(self, "另存为...", f"./{self.downLoadName}")
        if not pathTuple[0]:
            return
        self.path, self.downLoadName = os.path.split(pathTuple[0]) # 获得路径和下载的文件名
        self.downLoadLine.setText(self.downLoadName) # 设置下载的文件名
        self.downLoadBox.insertItem(3, self.path) # 在下拉框中插入下载目录
        self.downLoadBox.setCurrentText(self.path)