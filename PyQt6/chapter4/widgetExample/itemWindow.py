#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   itemWindow.py
@Time    :   2023/04/16 07:54:38
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtWidgets import QPushButton, QTextEdit, QVBoxLayout, QWidget, QApplication
from PyQt6.QtCore import Qt

class ItemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        closeButton = QPushButton("关闭", self)
        closeButton.clicked.connect(self.close)

        layout = QVBoxLayout(self)
        layout.addWidget(self.textEdit)
        layout.addWidget(closeButton)
        self.setLayout(layout)

        self.setWindowTitle("演示子窗体")

    def setFlags(self, flags):
    
        text = ""
        self.setWindowFlags(flags)

        
        if flags == Qt.WindowType.Window:
            text = "Qt.WindowType.Window"
        elif flags == Qt.WindowType.Dialog:
            text = "Qt.WindowType.Dialog"
        elif flags == Qt.WindowType.Sheet:
            text = "Qt.WindowType.Sheet"
        elif flags == Qt.WindowType.Popup:
            text = "Qt.WindowType.Popup"
        elif flags == Qt.WindowType.Tool:
            text = "Qt.WindowType.Tool"
        elif flags == Qt.WindowType.ToolTip:
            text = "Qt.WindowType.ToolTip"
        elif flags == Qt.WindowType.SplashScreen:
            text = "Qt.WindowType.SplashScreen"
        elif flags == Qt.WindowType.MSWindowsFixedSizeDialogHint:
            text = "Qt.WindowType.MSWindowsFixedSizeDialogHint"
        elif flags == Qt.WindowType.X11BypassWindowManagerHint:
            text = "Qt.WindowType.X11BypassWindowManagerHint"
        elif flags == Qt.WindowType.FramelessWindowHint:
            text = "Qt.WindowType.FramelessWindowHint"
        elif flags == Qt.WindowType.NoDropShadowWindowHint:
            text = "Qt.WindowType.NoDropShadowWindowHint"
        elif flags == Qt.WindowType.WindowTitleHint:
            text = "Qt.WindowType.WindowTitleHint"
        elif flags == Qt.WindowType.WindowSystemMenuHint:
            text = "Qt.WindowType.WindowSystemMenuHint"
        elif flags == Qt.WindowType.WindowMinimizeButtonHint:
            text = "Qt.WindowType.WindowMinimizeButtonHint"
        elif flags == Qt.WindowType.WindowMaximizeButtonHint:
            text = "Qt.WindowType.WindowMaximizeButtonHint"
        elif flags == Qt.WindowType.WindowCloseButtonHint:
            text = "Qt.WindowType.WindowCloseButtonHint"
        elif flags == Qt.WindowType.WindowContextHelpButtonHint:
            text = "Qt.WindowType.WindowContextHelpButtonHint"
        elif flags == Qt.WindowType.WindowShadeButtonHint:
            text = "Qt.WindowType.WindowShadeButtonHint"
        elif flags == Qt.WindowType.WindowStaysOnTopHint:
            text = "Qt.WindowType.WindowStaysOnTopHint"
        elif flags == Qt.WindowType.CustomizeWindowHint:
            text = "Qt.WindowType.CustomizeWindowHint"
        elif flags == Qt.WindowType.WindowSystemMenuHint:
            text = "Qt.WindowType.WindowSystemMenuHint"

        self.textEdit.setPlainText(text)