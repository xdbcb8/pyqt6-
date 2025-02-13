#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dialog.py
@Time    :   2023/09/07 06:24:51
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第14章第3节QThread--对话框

import codecs
import os
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QPlainTextEdit, QMessageBox, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class errorDialog(QDialog):
    """
    查看错误日志
    """
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.setWindowTitle("错误日志")
        self.resize(600, 400)
        self.setWindowFlags(Qt.WindowType.Window) # 窗体样式
        errorLog = QPlainTextEdit(self)
        layout = QVBoxLayout()
        layout.addWidget(errorLog)
        self.setLayout(layout)
        font = QFont()
        font.setPointSize(11)
        with codecs.open(f"{current_dir}\\error.log", "r", "utf-8", errors="ignore") as file:
            content = file.read() # 读取文件
            errorLog.setPlainText(content)
            errorLog.setFont(font)

class KeyDialog(QDialog):
    """
    websocket参数配置
    """
    keySignal =  pyqtSignal(list) # 参数配置的信号
    def __init__(self, SparkDesk, Parent=None):
        super().__init__(Parent)
        self.sparkdesk = SparkDesk # QSettings("SparkDesk", "APIKey")对象
        self.initUI()
        self.loadDate()
    
    def initUI(self):
        self.resize(400, 150)
        self.setWindowTitle("设置鉴权密钥")
        self.appid = QLineEdit(self)
        self.api_secret = QLineEdit(self)
        self.api_key = QLineEdit(self)
        self.gpt_url = QLineEdit(self)
        self.appid.setClearButtonEnabled(True)
        self.api_secret.setClearButtonEnabled(True)
        self.api_key.setClearButtonEnabled(True)
        self.gpt_url.setClearButtonEnabled(True)
        self.gpt_url.setText("ws://spark-api.xf-yun.com/v1.1/chat")
        buttonBox = QDialogButtonBox(self)
        buttonBox.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        buttonBox.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        # 布局
        layout = QFormLayout(self)
        layout.addRow("APPID", self.appid)
        layout.addRow("API_Secret", self.api_secret)
        layout.addRow("API_Key", self.api_key)
        layout.addRow("GPT_Url", self.gpt_url)
        layout.addRow(buttonBox)

        buttonBox.accepted.connect(self.settingKey)
        buttonBox.rejected.connect(self.reject)

    def loadDate(self):
        """
        载入配置数据
        """
        # 检查注册表中是否已有配置，有的话就载入
        if all([self.sparkdesk.contains("APPID"), self.sparkdesk.contains("API_Secret"),
           self.sparkdesk.contains("API_Key") ,self.sparkdesk.contains("GPT_Url")]):
            self.appid.setText(self.sparkdesk.value("APPID"))
            self.api_secret.setText(self.sparkdesk.value("API_Secret"))
            self.api_key.setText(self.sparkdesk.value("API_Key"))
            self.gpt_url.setText(self.sparkdesk.value("GPT_Url"))

    def settingKey(self):
        """
        设置鉴权密钥
        这四项均可以从“星火认知大模型”中获得
        """
        APP_iD = self.appid.text()
        API_Secret = self.api_secret.text()
        API_Key = self.api_key.text()
        GPT_Url = self.gpt_url.text()
        if not all([APP_iD, API_Secret, API_Key, GPT_Url]):
            # 四个参数不能为空
            QMessageBox.warning(self, "警告", "请确保所有字段都填写完整。")
            return
        # 将四项关键设置存入注册表
        self.sparkdesk.setValue("APPID", APP_iD)
        self.sparkdesk.setValue("API_Secret", API_Secret)
        self.sparkdesk.setValue("API_Key", API_Key)
        self.sparkdesk.setValue("GPT_Url", GPT_Url)
        # 将配置发送到主窗体
        self.keySignal.emit([APP_iD, API_Secret, API_Key, GPT_Url])
        self.accept()
