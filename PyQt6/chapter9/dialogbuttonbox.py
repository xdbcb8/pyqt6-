#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dialogbuttonbox.py
@Time    :   2023/07/16 11:39:09
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第9章第8节QDialogButtonBox

import sys
from PyQt6.QtWidgets import QDialog, QApplication, QDialogButtonBox, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MyWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(300, 100)
        self.setWindowTitle("QDialogButtonBox举例")
        label = QLabel("你真的不吃苹果吗？", self)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        font = QFont()
        font.setPointSize(16)
        label.setFont(font)
        # ########自定义按钮##########
        buttonBox = QDialogButtonBox(self)
        YesButton_ = QPushButton("要吃", self)
        YesButton_.setDefault(True)
        NoButton_ = QPushButton("不吃", self)
        NoButton_.setAutoDefault(False)
        buttonBox.addButton(YesButton_, QDialogButtonBox.ButtonRole.YesRole)
        buttonBox.addButton(NoButton_, QDialogButtonBox.ButtonRole.NoRole)

        # ########标准按钮############
        # buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)

        # ########混合按钮############
        # helpButton = QPushButton("帮助", self)
        # helpButton.setDefault(True)
        # buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)
        # buttonBox.addButton(helpButton, QDialogButtonBox.ButtonRole.HelpRole)

        # buttonBox.accepted.connect(lambda: self.showMessage(0))
        # buttonBox.rejected.connect(lambda: self.showMessage(1))
        # buttonBox.helpRequested.connect(lambda: self.showMessage(2))

        # 布局
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        self.show()

    def showMessage(self, p):
        if p == 0:
            QMessageBox.information(self, "accepted", "你单击了Yes按钮！")
            self.accept()
        elif p == 1:
            QMessageBox.information(self, "rejected", "你单击了No按钮！")
            self.reject()
        elif p == 2:
            QMessageBox.information(self, "helpRequested", "这是帮助文档！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())