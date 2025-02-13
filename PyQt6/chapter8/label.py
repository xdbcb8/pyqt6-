#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   label.py
@Time    :   2023/07/09 09:21:01
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第8章第6节QLabel

import sys
import os
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QFrame, QLineEdit, QHBoxLayout, QGridLayout, QToolButton
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import Qt

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLabel举例")
        self.resize(300, 200)
        # 凹陷面板
        # label = QLabel(self)
        # label.resize(200,100)
        # label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        # label.setText("这是第一行\n    这是第二行")
        # label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        # 快捷方式
        # hlayout = QHBoxLayout(self)
        # phoneEdit = QLineEdit()
        # phoneLabel = QLabel("&Phone:")
        # phoneLabel.setBuddy(phoneEdit)
        # hlayout.addWidget(phoneLabel)
        # hlayout.addWidget(phoneEdit)

        # 各种演示
        label1 = QLabel("这是文本演示")
        label2 = QLabel("这是很多文本的演示：12345678901234567890ewrewrewrrwerwerwedf是的方法答复的")
        label2.setWordWrap(True) # 自动换行

        label31 = QLabel("这是富文本演示")
        label32 = QLabel()
        html = '''
        <style type="text/css">
            table.imagetable {
                font-family: verdana,arial,sans-serif;
                font-size:11px;
                color:#333333;
                border-width: 1px;
                border-color: #999999;
                border-collapse: collapse;
            }
            table.imagetable th {
                background:#b5cfd2 url('cell-blue.jpg');
                border-width: 1px;
                padding: 8px;
                border-style: solid;
                border-color: #999999;
            }
            table.imagetable td {
                background:#dcddc0 url('cell-grey.jpg');
                border-width: 1px;
                padding: 8px;
                border-style: solid;
                border-color: #999999;
            }
        </style>
        <table class="imagetable">
            <tr>
                <th>标题一</th><th>标题二</th><th>标题三</th>
            </tr>
            <tr>
                <td>文本一</td><td>文本二</td><td>文本三</td>
            </tr>
        </table>
        '''
        label32.setText(html)

        label41 = QLabel("这是图片演示")
        label42 = QLabel()
        label42.setPixmap(QPixmap(f"{current_dir}\\labelPic.png"))

        label51 = QLabel("这是图片演示（缩放填充）")
        label52 = QLabel()
        label52.setPixmap(QPixmap(f"{current_dir}\\labelPic.png"))
        label52.setScaledContents(True)

        label61 = QLabel("这是动画演示")
        label62 = QLabel()
        self.movie = QMovie(f"{current_dir}\\num.gif")
        label62.setMovie(self.movie)
        self.movie.start() # 动画开始
        # 控制GIF动画暂停或者继续
        button1 = QToolButton()
        button1.setText("继续")
        button2 = QToolButton()
        button2.setText("暂停")
        button1.clicked.connect(self.Notpaused)
        button2.clicked.connect(self.paused)

        # 布局
        layout = QGridLayout(self)
        layout.addWidget(label1, 0, 0, 1, 2)
        layout.addWidget(label2, 1, 0, 1, 2)
        layout.addWidget(label31, 2, 0)
        layout.addWidget(label32, 2, 1)
        layout.addWidget(label41, 3, 0)
        layout.addWidget(label42, 3, 1)
        layout.addWidget(label51, 4, 0)
        layout.addWidget(label52, 4, 1)
        layout.addWidget(label61, 5, 0)
        layout.addWidget(label62, 5, 1)
        layout.addWidget(button1, 6, 0)
        layout.addWidget(button2, 6, 1)
        self.setLayout(layout)

        self.show()

    def Notpaused(self):
        """
        继续
        """
        self.movie.setPaused(False)

    def paused(self):
        """
        暂停
        """
        self.movie.setPaused(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())