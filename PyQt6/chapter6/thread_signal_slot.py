#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   thread_signal_slot.py
@Time    :   2023/05/18 15:49:36
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 跨线程的信号与槽方法使用
# 完整程序位于本书配套资料的PyQt6\chapter6\thread_signal_slot.py中

import sys
import time
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox

class Worker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        for i in range(1000):
            time.sleep(0.1)
            self.progress.emit(i)
        self.finished.emit()

class myWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(200, 100)
        self.setWindowTitle("跨线程信号与槽")
        self.label = QLabel(f"当前进度：0", self)
        self.button = QPushButton("启动")
        self.button.clicked.connect(self.begin)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def begin(self):
        '''
        单击按钮开始新线程
        '''
        self.button.setEnabled(False)
        self.worker = Worker(self)
        self.worker.start()
        self.worker.progress.connect(self.updateLabel)  # 接收线程的进度信号并连接到相应的槽方法
        self.worker.finished.connect(self.finishWork)  # 接收线程的完成信号并连接到相应的槽方法

    def updateLabel(self, value):
        '''
        显示线程当前工作进度
        '''
        self.label.setText(f"当前进度：{value}")
            
    def finishWork(self):
        '''
        完成线程工作后再次启用按钮
        '''
        self.worker.deleteLater
        self.button.setEnabled(True)

    def closeEvent(self, event):
        """
        子进程进行中则忽略关闭事件
        """
        if hasattr(self, 'worker'): 
            if self.worker.isRunning():
                QMessageBox.information(self, "提示", "进程仍在进行中！")
                event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myWindow()
    window.show()
    sys.exit(app.exec())