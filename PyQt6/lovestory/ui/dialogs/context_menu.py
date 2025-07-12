#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File     :   context_menu.py
@Time     :   2025/07/03 07:42:08
@Author   :   yangff
@Version  :   1.0
@微信公众号 : 学点编程吧
'''

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from config import db, current_dir

class ContextMenu(QWidget):
    
    menuSignal = pyqtSignal(str) # 菜单信号

    def __init__(self, flag, parent=None):
        super().__init__(parent)
        self.flag = flag
        self.initUI()

    def initUI(self):
        actions = ["新的游戏", "继续游戏", "我的历程", "查看好感", "退    出"]
        layout = QHBoxLayout()
        self.setLayout(layout)
        for action in actions:
            button = QPushButton(action)
            if action == '继续游戏':
                if db.query_non_empty_datetime(): # 必须得有游戏记录才能继续游戏
                    button.setEnabled(True)
                else:
                    button.setEnabled(False)
            button.setStyleSheet('''
                QPushButton {
                    border-radius: 10px;
                    background-color: #2c3e50;
                    color: white;
                    padding: 8px 16px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #3498db;
                    color: white;
                    font-size: 15px;
                }
            ''')
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

    def button_clicked(self):
        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile(current_dir + "/res/sfx/click.wav"))
        sound.play()
        actionName = self.sender().text()
        if actionName == "新的游戏":
            self.menuSignal.emit("newgame")
        elif actionName == "继续游戏":
            self.menuSignal.emit("continuegame")
        elif actionName == "我的历程":
            self.menuSignal.emit("myhistory")
        elif actionName == "查看好感":
            self.menuSignal.emit("viewfavor")
        elif actionName == "退    出":
            self.menuSignal.emit("exitgame")