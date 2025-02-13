#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   progressdialog.py
@Time    :   2023/07/15 11:53:21
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第9章第7节QProgressDialog

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QProgressDialog, QSpinBox, QPushButton, QVBoxLayout, QSizePolicy, QMessageBox
from PyQt6.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QProgressDialog举例")
        self.resize(300, 100)
        button = QPushButton("开始复制", self)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        files = QSpinBox(self)
        files.setPrefix("文件数量：") # 前缀
        files.setSuffix("个") # 后缀
        files.setRange(100000, 10000000)
        files.setStepType(QSpinBox.StepType.AdaptiveDecimalStepType)
        layout = QVBoxLayout(self)
        layout.addWidget(files)
        layout.addWidget(button)
        self.setLayout(layout)
        self.show()
        button.clicked.connect(lambda :self.showDialog(files.value()))
    
    def showDialog(self, num):
        """
        调用进度对话框
        num：表示需要复制的文件数量
        """
        progress = QProgressDialog(self)
        progress.setWindowTitle("请稍等")  
        progress.setLabelText("文件正在复制中...")
        progress.setCancelButtonText("取消")
        progress.setMinimumDuration(1000) # 预估最少时间大于1秒才显示对话框
        progress.setWindowModality(Qt.WindowModality.WindowModal) # 使用模态对话框
        progress.setRange(0, num)
        for i in range(num+1):
            progress.setValue(i) 
            if progress.wasCanceled(): # 若单击“取消”按钮
                QMessageBox.warning(self, "提示", "复制失败，可能没有复制完全！") 
                break
        else:
            QMessageBox.information(self,"提示","操作成功")
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())