#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   filedialog.py
@Time    :   2023/07/11 12:48:47
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第9章第3节QFileDialog

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QFileDialog, QPushButton

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.setWindowTitle("QFileDialog举例")
        button = QPushButton("选择文件", self)
        button.clicked.connect(self.selectFile)
        self.show()

    def selectFile(self):
        """
        选择文件
        """
        # 选择单个文件对话框
        fileNameList = QFileDialog.getOpenFileName(self, "选择图像", "./", "Images (*.png *.jpg);;Text files (*.txt);;XML files (*.xml)")
        print(fileNameList)

        # 选择多个文件对话框
        # fileNameList = QFileDialog.getOpenFileNames(self, "选择图像", "./", "Python Files (*.py *.pyw)")
        # print(fileNameList)

        # 保存单个文件对话框
        # saveFileName = QFileDialog.getSaveFileName(self, "保存TXT文件", "./", "Text files (*.txt)")
        # print(saveFileName)

        # 创建QFileDialog对象打开对话框
        # dialog = QFileDialog(self)
        # dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        # # dialog.setFileMode(QFileDialog.FileMode.ExistingFiles) # 选择多个文件
        # dialog.setNameFilter("Python Files (*.py);;Images (*.png *.xpm *.jpg)") # 筛选器
        # dialog.setViewMode(QFileDialog.ViewMode.Detail)
        # dialog.setDirectory("D:\\") # 打开D盘目录
        # dialog.setWindowTitle("选择Python文件") # 设置对话框标题
        # if dialog.exec():
        #     fileNameList = dialog.selectedFiles() # 返回选取的文件路径
        #     print(fileNameList)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())