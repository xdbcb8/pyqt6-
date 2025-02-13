#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   messagebox.py
@Time    :   2023/07/14 13:18:20
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第9章第6节QMessageBox

import sys
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox, QGridLayout, QPushButton, QCheckBox, QLabel
from PyQt6.QtCore import pyqtSlot, QMetaObject, Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(350, 200)
        self.setWindowTitle("QMessageBox举例")
        button1 = QPushButton("提示信息对话框", self)
        button2 = QPushButton("询问对话框", self)
        button3 = QPushButton("警告对话框", self)
        button4 = QPushButton("严重问题对话框", self)
        button5 = QPushButton("关于对话框", self)
        button6 = QPushButton("关于Qt对话框", self)
        button7 = QPushButton("自定义消息对话框", self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter) # 靠右对齐

        button1.setObjectName("buttonInfo")
        button2.setObjectName("buttonQue")
        button3.setObjectName("buttonWaring")
        button4.setObjectName("buttonCritical")
        button5.setObjectName("buttonAbout")
        button6.setObjectName("buttonAboutqt")
        button7.setObjectName("buttonDiy")

        layout = QGridLayout(self)
        layout.addWidget(button1, 0, 0)
        layout.addWidget(button2, 0, 1)
        layout.addWidget(button3, 0, 2)
        layout.addWidget(button4, 1, 0)
        layout.addWidget(button5, 1, 1)
        layout.addWidget(button6, 1, 2)
        layout.addWidget(button7, 2, 0)
        layout.addWidget(self.label, 2, 1, 1, 2)
        self.setLayout(layout)
        self.show()
        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def on_buttonInfo_clicked(self):
        QMessageBox.information(self, "information()", "这是一条消息")

    @pyqtSlot()
    def on_buttonQue_clicked(self):
        result = QMessageBox.question(self, "question()", "这个问题你知道吗？", defaultButton=QMessageBox.StandardButton.No)
        print(result) # StandardButton.No

    @pyqtSlot()
    def on_buttonWaring_clicked(self):
        QMessageBox.warning(self, "warning()", "这是一条告警信息！")

    @pyqtSlot()
    def on_buttonCritical_clicked(self):
        QMessageBox.critical(self, "critical()", "你这个行为很危险！")

    @pyqtSlot()
    def on_buttonAbout_clicked(self):
        QMessageBox.about(self, "about()", "这是关于XXX的事情。")

    @pyqtSlot()
    def on_buttonAboutqt_clicked(self):
        QMessageBox.aboutQt(self, "aboutQt()")

    @pyqtSlot()
    def on_buttonDiy_clicked(self):
        msgBox = QMessageBox(self)
        cb = QCheckBox("都按此操作")
        msgBox.setWindowTitle("小提示")
        msgBox.setIcon(QMessageBox.Icon.Information)
        infomation = "这是一条非常<b><font color='#FF0000'>好玩</font></b>的消息<br>大家一起来玩啊~！"
        msgBox.setText("这是一条简单的提示信息！")
        msgBox.setInformativeText(infomation)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Abort | QMessageBox.StandardButton.Ignore)
        msgBox.setDetailedText("这里是详细的说明：……………………")
        Save = msgBox.addButton("保存", QMessageBox.ButtonRole.AcceptRole)
        NoSave = msgBox.addButton("不保存", QMessageBox.ButtonRole.DestructiveRole)
        Cancel = msgBox.addButton("取消", QMessageBox.ButtonRole.RejectRole)
        msgBox.setDefaultButton(Save)
        msgBox.setCheckBox(cb)
        reply = msgBox.exec()
        if reply == 0:
            self.label.setText("自定义消息对话框：你单击了“保存”按钮！")
        elif reply == 1:
            self.label.setText("自定义消息对话框：你选择了不保存！")
        elif reply == 2:
            self.label.setText("自定义消息对话框：你选择了取消！")
        elif reply == QMessageBox.StandardButton.Retry:
            self.label.setText("自定义消息对话框：你选择了重试！")
        elif reply == QMessageBox.StandardButton.Abort:
            self.label.setText("自定义消息对话框：你选择了终止！")
        elif reply == QMessageBox.StandardButton.Ignore:
            self.label.setText("自定义消息对话框：你选择了忽略！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())