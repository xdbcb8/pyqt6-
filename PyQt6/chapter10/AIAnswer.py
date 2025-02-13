#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   AIAnswer.py
@Time    :   2023/07/28 17:42:14
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第10章第3节QTextEdit
# 本程序运行前，请务必保证运行环境中已经安装websocket、websocket-client模块

import sys
import os
import codecs
import ssl
import websocket
import json
import SparkApi
from PyQt6.QtWidgets import (QWidget, QApplication, QMainWindow, QTextEdit, QDialog, QPushButton, 
                             QFormLayout, QLineEdit, QDialogButtonBox, QPlainTextEdit, QMessageBox, 
                             QVBoxLayout, QHBoxLayout, QSplitter, QMenu, QFileDialog)
from PyQt6.QtCore import QSettings, Qt, pyqtSignal, QDateTime, QCoreApplication
from PyQt6.QtGui import QAction, QTextCursor, QFont, QTextCharFormat, QKeySequence

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
        with codecs.open(f"{current_dir}\error.log", "r", "utf-8", errors="ignore") as file:
            content = file.read() # 读取文件
            errorLog.setPlainText(content)
            errorLog.setFont(font)

class KeyDialog(QDialog):
    """
    WebSocket参数配置
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

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.SparkDesksettings = QSettings("SparkDesk", "APIKey")
        # APP_iD、API_Secret、API_Key、GPT_Url 默认值
        self.APP_iD = ""
        self.API_Secret = ""
        self.API_Key = ""
        self.GPT_Url = ""
        self.answer = "" # 答案默认为空
        self.initUI()
        self.loadDate()

    def loadDate(self):
        """
        载入数据
        """
        #  如果注册表中没有相关配置，就提示无法使用
        if not all([self.SparkDesksettings.contains("APPID"), self.SparkDesksettings.contains("API_Secret"),
                   self.SparkDesksettings.contains("API_Key") ,self.SparkDesksettings.contains("GPT_Url")]):
            self.chatAnswer.append("<b><font color='#FF0000'>模型鉴权参数未配置，无法使用！</font></b><br>")
            self.sendButton.setEnabled(False)
        else: # 有配置就生成Ws_Param对象
            self.APP_iD = self.SparkDesksettings.value("APPID")
            self.API_Secret = self.SparkDesksettings.value("API_Secret")
            self.API_Key = self.SparkDesksettings.value("API_Key")
            self.GPT_Url = self.SparkDesksettings.value("GPT_Url")
            self.wsParam = self.createWs_Param(self.APP_iD, self.API_Key, self.API_Secret, self.GPT_Url)

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle("AI问答小工具")
        self.statusBar().showMessage("准备就绪") # 状态栏

        # ###########创建菜单#############

        # 设置菜单
        settingMenu = self.menuBar().addMenu("设置(&S)")
        keyAct = QAction("密钥(&K)", self)
        keyAct.setShortcut("ALt+K")
        keyAct.setStatusTip("密钥设置")
        settingMenu.addAction(keyAct)
        # 查看菜单
        viewMenu = self.menuBar().addMenu("查看(&V)")
        errorAct = QAction("错误日志(&E)", self)
        errorAct.setShortcut("ALt+E")
        errorAct.setStatusTip("查看错误日志")
        viewMenu.addAction(errorAct)
        zoomInAct = QAction("放大(&I)", self)
        zoomInAct.setShortcuts(QKeySequence.StandardKey.ZoomIn)
        zoomInAct.setStatusTip("放大")
        zoomOutAct = QAction("缩小(&O)", self)
        zoomOutAct.setShortcuts(QKeySequence.StandardKey.ZoomOut)
        zoomOutAct.setStatusTip("缩小")
        viewMenu.addAction(zoomInAct)
        viewMenu.addAction(zoomOutAct)

        # ###########创建聊天窗体#############
        
        spliter = QSplitter(self)
        spliter.setOrientation(Qt.Orientation.Vertical)
        widget= QWidget(spliter)
        # 使用QPlainTextEdit控件可以提出问题
        self.chatQue = QPlainTextEdit(widget)
        fontQue = QFont()
        fontQue.setPointSize(11)
        self.chatQue.setFont(fontQue)
        # 占位文本
        self.chatQue.setPlaceholderText("可以在这里输入你的问题，按下Ctrl+Enter键可以发送问题")
        # 使用QtextEdit可以显示回答的问题
        self.chatAnswer = QTextEdit()
        # 只读
        self.chatAnswer.setReadOnly(True)
        self.chatAnswer.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.chatAnswer.customContextMenuRequested.connect(self.showContextMenu)
        self.cursor = self.chatAnswer.textCursor()
        self.sendButton = QPushButton("发送", widget)
        # 简单布局
        hlayout = QHBoxLayout(widget)
        hlayout.addWidget(self.chatQue)
        hlayout.addWidget(self.sendButton)
        widget.setLayout(hlayout)
        spliter.addWidget(self.chatAnswer)
        spliter.addWidget(widget)
        spliter.setStretchFactor(0, 3)
        spliter.setStretchFactor(1, 1)
        self.setCentralWidget(spliter)
        
        keyAct.triggered.connect(self.execKeyDialog)
        errorAct.triggered.connect(self.showLog)
        self.sendButton.clicked.connect(self.sendQuestion)
        zoomInAct.triggered.connect(self.chatAnswer.zoomIn)
        zoomOutAct.triggered.connect(self.chatAnswer.zoomOut)

        self.show()

    def showContextMenu(self, position):
        # 创建self.chatAnswer自定义菜单对象
        context_menu = QMenu(self)

        # 创建动作并添加到自定义菜单中
        copy_action = QAction("复制", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        context_menu.addAction(copy_action)
        
        selectAll_action = QAction("全选", self)
        selectAll_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        context_menu.addAction(selectAll_action)
        
        clearAll_action = QAction("清屏", self)
        context_menu.addAction(clearAll_action)

        self.saveAs_action = QAction("保存记录", self)
        self.saveAs_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        context_menu.addAction(self.saveAs_action)

        # 连接动作的信号和槽函数
        copy_action.triggered.connect(self.chatAnswer.copy)
        selectAll_action.triggered.connect(self.chatAnswer.selectAll)
        clearAll_action.triggered.connect(self.chatAnswer.clear)
        self.saveAs_action.triggered.connect(self.saveAsChat)

        # 在指定位置显示自定义菜单
        context_menu.exec(self.chatAnswer.mapToGlobal(position))

    def saveAsChat(self):
        """
        保存聊天记录
        """
        if not self.chatAnswer.toPlainText():
            return
        saveFileName = QFileDialog.getSaveFileName(self, "保存文件", "./", "HTML files (*.html);;Text files (*.txt)")
        absFileName = saveFileName[0]
        if absFileName:
            with codecs.open(absFileName, "w", "utf-8", errors="ignore") as f:
                if absFileName.split('.')[1] == "html":
                    f.write(self.chatAnswer.toHtml())
                else:
                    f.write(self.chatAnswer.toPlainText())

    def createWs_Param(self, appid, api_key, api_secret, gpt_url):
        # 生成Ws_Param对象，为下步鉴权URL准备，具体请见“星火认知大模型”文档
        wsParam = SparkApi.Ws_Param(appid, api_key, api_secret, gpt_url)
        return wsParam

    def keyPressEvent(self, event):
        """
        实现按下Ctrl + Enter组合键发送问题
        """
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Return:
            self.sendButton.click()
        else:
            super().keyPressEvent(event)

    def execKeyDialog(self):
        """
        鉴权参数设置对话框
        """
        keydialog = KeyDialog(self.SparkDesksettings, self)
        keydialog.keySignal.connect(self.readSparkDesksettings)
        keydialog.exec()

    def readSparkDesksettings(self, apikEY):
        """
        获得从鉴权参数设置对话框发来的配置
        apikEY：列表，配置信息
        """
        self.APP_iD = apikEY[0]
        self.API_Secret = apikEY[1]
        self.API_Key = apikEY[2]
        self.GPT_Url = apikEY[3]
        self.sendButton.setEnabled(True)
        self.chatAnswer.clear()
        self.wsParam = self.createWs_Param(self.APP_iD, self.API_Key, self.API_Secret, self.GPT_Url)

    def showLog(self):
        """
        查看错误日志
        """
        errordialog = errorDialog(self)
        errordialog.exec()

    def on_error(self, ws, error):
        """
        错误处理
        """
        SparkApi.on_error(ws, error)
        self.chatAnswer.append("<br><b><font color='#FF0000'>连接错误，详细原因请查找日志！</font></b><br>")

    def on_message(self, ws, message):
        """
        收到websocket消息的处理
        有关数据中如“header”这些属性的含义请查看星火模型的文档
        """
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            SparkApi.error(code, data)
            self.chatAnswer.append("<br><b><font color='#FF0000'>请求错误，详细原因请查找日志！</font></b><br>")
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            self.answer += content
            if status == 2: # 表示已经回答完毕
                self.cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
                self.cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
                self.cursor.deleteChar()
                # 以上三段代码的含义就是删除“AI思考中……”这句话
                self.cursor.insertMarkdown(self.answer) # 插入markdown
                self.chatAnswer.append('\n\n回答完毕！\n----------------------------------------\n\n')
                self.answer = "" # 暂存的答案仍要清除
                ws.close() # 关闭websocket连接

    def getAnswer(self, ques):
        """
        从星火模型中得到答案
        ques：问题
        """
        wsUrl = self.wsParam.create_url()
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(wsUrl, on_message=self.on_message, on_error=self.on_error, on_close=SparkApi.on_close, on_open=SparkApi.on_open)
        ws.appid = self.APP_iD
        ws.question = ques
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def setRespondQue(self, ques):
        """
        将问题发送到聊天窗体
        ques：问题
        """
        self.setFormatText("Q")
        self.cursor.insertText(ques + '\n')
        self.setRespondAnswer(ques)

    def setRespondAnswer(self, ques):
        """
        得到问题的反馈
        ques：问题
        """
        self.setFormatText('A')
        self.cursor.insertText("AI思考中……")
         # 因为需要等待问题反馈，这里主要是为了避免卡死，但是个人感觉推荐使用多线程好点，后续再优化
        QCoreApplication.processEvents()
        self.getAnswer(ques)

    def getCurrentDateTime(self):
        """
        获得当前时间
        """
        currentDateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        return currentDateTime

    def sendQuestion(self):
        """
        发送问题
        """
        text = self.chatQue.toPlainText()
        if not text:
            return
        self.chatQue.clear() #发送问题后，提问处需要清屏
        self.setRespondQue(text)
    
    def setFormatText(self, Q_A):
        """
        格式化问答
        Q_A：识别是问题还是答案
        """
        currentDateTime = ' ' + self.getCurrentDateTime() + '\n'
        textFormat = QTextCharFormat()
        font = QFont()
        font.setItalic(True) # 斜体
        font.setBold(True) # 加粗
        textFormat.setFont(font)
        if Q_A == "Q":
            # 给问题中的时间增加格式
            self.cursor.insertImage(f"{current_dir}\images\heart.png") # 爱心
            textFormat.setForeground(Qt.GlobalColor.red) # 红色
            self.cursor.setCharFormat(textFormat) # 当前文档光标格式
            self.cursor.insertText(currentDateTime)
        else:
            # 给答案中的时间增加格式
            self.cursor.insertImage(f"{current_dir}\images\star.png") # 星
            textFormat.setForeground(Qt.GlobalColor.darkRed) # 暗红
            self.cursor.setCharFormat(textFormat)
            self.cursor.insertText(currentDateTime)
        # 给时间以下的内容增加格式
        font.setItalic(False)
        font.setBold(False)
        textFormat.setFont(font)
        textFormat.setForeground(Qt.GlobalColor.black) # 黑色
        self.cursor.setCharFormat(textFormat)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())