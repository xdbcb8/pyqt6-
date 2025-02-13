#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   AIAnswer.py
@Time    :   2023/09/07 06:24:51
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

# 第14章第3节QThread
# 本程序运行前，请务必保证运行环境中已经安装websocket、websocket-client模块

import os
import sys
import codecs
import ssl
import websocket
import json
import SparkApi
from PyQt6.QtWidgets import (QWidget, QApplication, QMainWindow, QTextEdit, QPushButton, 
                             QPlainTextEdit, QHBoxLayout, QSplitter, QMenu, QFileDialog)
from PyQt6.QtCore import QSettings, Qt, pyqtSignal, QDateTime, QThread
from PyQt6.QtGui import QAction, QTextCursor, QFont, QTextCharFormat, QKeySequence
from dialog import errorDialog, KeyDialog

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class Response(QThread):

    aiErrorSignal = pyqtSignal(str) # AI错误信号
    aiContent = pyqtSignal(str) # AI回答信号
    aiFinish = pyqtSignal() # AI回答完毕信号

    def __init__(self, Parent=None):
        super().__init__(Parent)

    def setting(self, ws, APP_iD, ques):
        """
        多线程的一些配置
        """
        self.wsParam = ws # Ws_Param对象，为下步鉴权URL准备
        self.APP_iD = APP_iD
        self.ques = ques # 问题
    
    def run(self):
        """
        从星火模型中得到答案
        """
        wsUrl = self.wsParam.create_url()
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(wsUrl, on_message=self.on_message, on_error=self.on_error, on_close=SparkApi.on_close, on_open=SparkApi.on_open)
        ws.appid = self.APP_iD
        ws.question = self.ques
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def on_error(self, ws, error):
        """
        错误处理
        """
        SparkApi.on_error(ws, error)
        self.aiErrorSignal.emit("connect_error")
        
    def on_message(self, ws, message):
        """
        收到websocket消息的处理
        有关数据中如“header”这些属性的含义请查看星火模型的文档
        """
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            SparkApi.error(code, data)
            self.aiErrorSignal.emit("request_error")
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            self.aiContent.emit(content)
            if status == 2: # 表示已经回答完毕
                ws.close() # 关闭websocket连接
                self.aiFinish.emit()

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.SparkDesksettings = QSettings("SparkDesk", "APIKey")
        # APP_iD、API_Secret、API_Key、GPT_Url 默认值
        self.APP_iD = ""
        self.API_Secret = ""
        self.API_Key = ""
        self.GPT_Url = ""
        self.beginAnswer = 0 # 开始回答的标志
        self.position = 0 # 记录开始回答的位置
        self.answer = "" # 完整的答案
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
        self.chatQue = QPlainTextEdit(widget)
        fontQue = QFont()
        fontQue.setPointSize(11)
        self.chatQue.setFont(fontQue)
        self.chatQue.setPlaceholderText("可以在这里输入你的问题，按下Ctrl+Enter键可以发送问题，按下Ctrl+Up键可以显示刚才的问题")
        self.chatAnswer = QTextEdit()
        self.chatAnswer.setReadOnly(True)
        self.chatAnswer.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.chatAnswer.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoNone) # 不自动格式化
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
        实现按下Ctrl+Enter组合键发送问题
        """
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Return:
            self.sendButton.click() # Ctrl+Enter 发送问题
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and  event.key() == Qt.Key.Key_Up:
            self.chatQue.clear()
            self.chatQue.setPlainText(self.question) # Ctrl+UP 提问区显示刚才的问题
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

    def setRespondQue(self, ques):
        """
        将问题发送到聊天窗体
        ques：问题
        """
        self.setFormatText("Q")
        self.setFormatText("M")
        self.cursor.insertText(ques + '\n')
        self.setRespondAnswer(ques)

    def setRespondAnswer(self, ques):
        """
        得到问题的反馈
        ques：问题
        """
        self.setFormatText("A")
        self.setFormatText("M")
        self.cursor.insertText("AI思考中……")
        response = Response(self) # 使用多线程调用
        response.setting(self.wsParam, self.APP_iD, ques)
        response.aiErrorSignal.connect(self.showError)
        response.aiContent.connect(self.showAnswer)
        response.aiFinish.connect(self.doneAnswer)
        response.start()

    def doneAnswer(self):
        """
        回答完毕
        """
        self.beginAnswer = 0 # 重置开始回答的标志
        self.cursor.setPosition(self.position)
        self.cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        self.cursor.deleteChar()
        # 以上三行代码是删除之前答案，因为有些答案是markdown形式，需要进一步的转换
        self.cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor)
        self.cursor.insertMarkdown(self.answer) # 插入markdown
        self.answer = "" # 重置完整答案
        self.setFormatText("M")
        self.cursor.insertText("\n\nAI回答完毕！\n----------------------------------------\n\n")
        self.chatAnswer.verticalScrollBar().setValue(self.chatAnswer.verticalScrollBar().maximum()) # 滚动条随内容增加而滚动
    
    def showAnswer(self, content):
        """
        显示答案
        content：答案
        """
        if self.beginAnswer == 0: # 开始回答的标志
            self.cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
            self.cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
            self.cursor.deleteChar()
            # 以上三段代码的含义就是删除“AI思考中……”这句话
            self.beginAnswer = 1 # 正式回答的标志
            self.setFormatText("M")
            self.position = self.cursor.position() # 记录正式答案的光标位置
        
        self.answer += content
        self.cursor.insertText(content) # 插入答案
        self.chatAnswer.verticalScrollBar().setValue(self.chatAnswer.verticalScrollBar().maximum()) # 滚动条随内容增加而滚动

    def showError(self, error):
        """
        调用错误时显示错误信息
        """
        if error == "connect_error":
            self.chatAnswer.append("<p><b><font color='#FF0000'>连接错误，详细原因请查找日志！</font></b><p>")
        elif error == "request_error":
            self.chatAnswer.append("<p><b><font color='#FF0000'>请求错误，详细原因请查找日志！</font></b><p>")

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
        self.question = self.chatQue.toPlainText()
        if not self.question:
            return
        self.chatQue.clear() #发送问题后，提问处需要清屏
        self.setRespondQue(self.question)
    
    def setFormatText(self, Q_A_M):
        """
        格式化问答
        Q_A_M：识别是问题、答案还详细信息
        """
        currentDateTime = ' ' + self.getCurrentDateTime() + '\n'
        textFormat = QTextCharFormat()
        font = QFont()
        font.setItalic(True) # 斜体
        font.setBold(True) # 加粗
        textFormat.setFont(font)
        if Q_A_M == "Q":
            # 给问题中的时间增加格式
            self.cursor.insertImage(f"{current_dir}\\images\\heart.png") # 爱心
            textFormat.setForeground(Qt.GlobalColor.red) # 红色
            self.cursor.setCharFormat(textFormat) # 当前文档光标格式
            self.cursor.insertText(currentDateTime)
        elif Q_A_M == "A":
            # 给答案中的时间增加格式
            self.cursor.insertImage(f"{current_dir}\\images\\star.png") # 星
            textFormat.setForeground(Qt.GlobalColor.darkRed) # 暗红
            self.cursor.setCharFormat(textFormat)
            self.cursor.insertText(currentDateTime)
        # 给时间以下的内容增加格式
        elif Q_A_M == "M":
            font.setItalic(False)
            font.setBold(False)
            textFormat.setFont(font)
            textFormat.setForeground(Qt.GlobalColor.black) # 黑色
            self.cursor.setCharFormat(textFormat)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())