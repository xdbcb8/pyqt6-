#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File     :   message_menu.py
@Time     :   2025/06/27 22:04:25
@Author   :   yangff
@Version  :   1.0
@微信公众号 : 学点编程吧
'''

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from config import current_dir, favorabilityDict

class Button(QPushButton):
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred) # 设定控件尺寸的策略

class MessageMenu(QWidget):

    choiceInfoSignal = pyqtSignal(str) # 玩家选择的选项
    updateFavorabilitySignal = pyqtSignal(str, int) # 更新好感度的信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.message = ''
        self.choices = []
        self.initUI()
        
    def setinfomation(self, optionsList):
        '''
        设置消息框的界面内容
        optionsList: 一个列表，包含消息内容和选项
        '''
        self.message = optionsList[0]
        self.choices = optionsList[1:]
        self.label.setText(self.message)
        self.button1.setText(self.choices[0])
        self.button2.setText(self.choices[1])
        count = len(self.choices)
        if count == 2:
            self.button3.hide() 
            self.button4.hide() # 默认第3、4个按钮是隐藏
        elif count == 4:
            self.button3.setText(self.choices[2])
            self.button4.setText(self.choices[3])
            self.button3.show()
            self.button4.show()

    def initUI(self):
        '''
        初始化消息框的界面
        '''
        self.hide() # 默认隐藏
        vlayout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setText(self.message)
        self.label.setStyleSheet("""
            QLabel {
                border-radius: 10px;
                background-color: #2c3e50;
                color: white;
                padding: 8px 16px;
                font-size: 16px;
                text-align: center;
            }
        """)
        vlayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        hlayout = QHBoxLayout()
        button_style = """
            QPushButton {
                border-radius: 10px;
                background-color: #2c3e50;
                color: white;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
                color: #ecf0f1;
            }
        """
        self.button1 = Button(self)
        self.button2 = Button(self)
        self.button3 = Button(self)
        self.button4 = Button(self)
        self.button1.setStyleSheet(button_style)
        self.button2.setStyleSheet(button_style)
        self.button3.setStyleSheet(button_style)
        self.button4.setStyleSheet(button_style)
        self.button1.clicked.connect(self.on_button_clicked)
        self.button2.clicked.connect(self.on_button_clicked)
        self.button3.clicked.connect(self.on_button_clicked)
        self.button4.clicked.connect(self.on_button_clicked)
        hlayout.addWidget(self.button1)
        hlayout.addWidget(self.button2)
        hlayout.addWidget(self.button3)
        hlayout.addWidget(self.button4)
        vlayout.addLayout(hlayout)
        self.setLayout(vlayout)

    def on_button_clicked(self):
        '''
        处理按钮点击事件
        '''
        # 播放点击音效
        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile(current_dir + "/res/sfx/click.wav"))
        sound.play()
        
        buttonInfo = self.sender()
        if buttonInfo:
            choiceInfo = buttonInfo.text()
            self.choiceInfoSignal.emit(choiceInfo)
            self.hide()
            favorability = favorabilityDict.get(choiceInfo)
            if favorability:
                self.updateFavorabilitySignal.emit(favorability[0], favorability[1])