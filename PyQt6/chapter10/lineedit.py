#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   self.lineedit.py
@Time    :   2023/07/22 09:25:00
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第10章第1节QLineEdit

import sys
import os
from PyQt6.QtWidgets import QWidget, QApplication, QLineEdit, QFormLayout, QLabel, QCompleter
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QRegularExpressionValidator, QStandardItemModel, QKeyEvent, QKeySequence
from PyQt6.QtCore import QDir, Qt, QRegularExpression, QEvent, QTimer

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class PwdLineEdit(QLineEdit):
    """
    自定义密码输入框
    """
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.m_LineEditText = "" # 记录真实的密码
        self.m_LastCharCount = 0 # 密码出现变化前的长度
        
        self.Action()
    
    def Action(self):
        '''
        一些初始设置
        '''
        self.cursorPositionChanged.connect(self.DisplayPasswordAfterEditSlot) # 光标发生移动时产生，返回两个整型变量并调用槽函数
        self.textEdited.connect(self.GetRealTextSlot) # 密码输入时调用GetRealTextSlot
        self.time = QTimer(self)# 设置一个定时器
        self.time.setInterval(200)# 200毫秒超时，也就是200毫秒把单个字符变成★
        self.time.start()
        self.show()
    
    def DisplayPasswordAfterEditSlot(self, old, new):
        '''
        显示密文
        old：旧的光标位置
        new：新的光标位置
        '''
        if old >= 0 and new >= 0:
            if new > old:
                self.time.timeout.connect(self.DisplayPasswordSlot)# 密码在增加，自动转换成★
            else:
                self.setCursorPosition(old)# 尝试注释这个，你可以看看效果，非常爽！

    def DisplayPasswordSlot(self):
        '''
        在密码输入框把密码变成★
        '''
        self.setText(self.GetMaskString())

    def GetRealTextSlot(self, text):
        '''
        获取真实密码
        '''
        self.m_LastCharCount = len(self.m_LineEditText) # 当前没有变化时密码的长度
        
        if len(text) > self.m_LastCharCount:
            self.m_LineEditText += text[-1]
        # 当前的长度大于之前记录的密码长度，密码在新增字符，将新增的字符和原有的密码进行合并。
            
        elif len(text) <= self.m_LastCharCount:
            self.m_LineEditText = self.m_LineEditText[:-1]
        # 密码删除中，真实密码也在变少。

    def GetMaskString(self):
        '''
        把明文密码变成★
        '''
        mask = ""
        count = len(self.text())
        if count > 0:
            for i in range(count):
                mask += "\u2605" # 五角星
        return mask
    
    def GetPassword(self):
        '''
        获得真实密码
        '''
        return self.m_LineEditText

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLineEdit举例")
        self.resize(400, 350)
        QDir.addSearchPath("icon", f"{current_dir}\images")
        self.isOpen = True
        self.initUI()
        self.setting()
        
    def initUI(self):
        self.lineEditNormal = QLineEdit("普通单行输入栏", self)
        self.lineEditSelect = QLineEdit(self)
        self.lineEditholderText = QLineEdit(self)
        self.lineEditClear = QLineEdit(self)
        self.lineEditZMSZ = QLineEdit(self)
        self.lineEditIp = QLineEdit(self)
        self.lineEditMAC = QLineEdit(self)
        self.lineEditDate = QLineEdit(self)
        self.lineEditLicense = QLineEdit(self)
        self.lineEditPwd = QLineEdit(self)
        self.lineEditPwdStop = QLineEdit(self)
        self.lineEditPwdNoEcho = QLineEdit(self)
        self.lineEditPwdPlus = QLineEdit(self)
        self.lineEditPwdPlusColor = QLineEdit(self)
        self.lineEditPwdPlus3 = PwdLineEdit(self)
        self.lineEditAutoComplete = QLineEdit(self)

        self.labelPwdNoEcho = QLabel(self)
        self.labelPwdPlus3 = QLabel(self)

        # 布局
        layout = QFormLayout(self)
        layout.addRow("普通型", self.lineEditNormal)
        layout.addRow("自动全选", self.lineEditSelect)
        layout.addRow("带占位字符串", self.lineEditholderText)
        layout.addRow("带消除按钮", self.lineEditClear)
        layout.addRow("只能输入字母、数字", self.lineEditZMSZ)
        layout.addRow("IP地址", self.lineEditIp)
        layout.addRow("MAC地址", self.lineEditMAC)
        layout.addRow("日期", self.lineEditDate)
        layout.addRow("License", self.lineEditLicense)
        layout.addRow("普通密码", self.lineEditPwd)
        layout.addRow("禁止复制粘贴全选", self.lineEditPwdStop)
        layout.addRow("不可见密码", self.lineEditPwdNoEcho)
        layout.addRow("不可见密码为", self.labelPwdNoEcho)
        layout.addRow("密码（不再编辑后加密）", self.lineEditPwdPlus)
        layout.addRow("密码加强版（长度校验）", self.lineEditPwdPlusColor)
        layout.addRow("边输入边加密成★", self.lineEditPwdPlus3)
        layout.addRow("显示★密码为", self.labelPwdPlus3)
        layout.addRow("自动补全网址", self.lineEditAutoComplete)

        self.lineEditPwdStop.installEventFilter(self)
        self.lineEditPwdNoEcho.textChanged.connect(self.showPwdNoEcho)
        self.lineEditPwdPlusColor.textChanged.connect(self.verify)
        self.lineEditPwdPlus3.textChanged.connect(self.showPwdPlus3)
        self.lineEditAutoComplete.textChanged.connect(self.autoComplete)

        self.show()

    def showPwdNoEcho(self):
        """
        显示不可见密码
        """
        self.labelPwdNoEcho.setText(self.lineEditPwdNoEcho.text())
    
    def showPwdPlus3(self):
        """
        显示加密成★的密码
        """
        pwd = self.lineEditPwdPlus3.GetPassword()
        self.labelPwdPlus3.setText(pwd)

    def setting(self):
        """
        各个单行输入栏的设置
        """
        # 设置自动全选文字
        self.lineEditSelect.setFocus()
        self.lineEditSelect.setText("这些都是自动全选的文字")
        self.lineEditSelect.setSelection(4, 4)
        # 设置占位文字
        self.lineEditholderText.setPlaceholderText("你可以在这里输入喜欢的文字")
        # 设置清除按钮
        self.lineEditClear.setText("注意观察单行输入栏右侧的清除按钮")
        self.lineEditClear.setClearButtonEnabled(True)
        # 设置只允许输入字母和数字的正则表达式
        regx = QRegularExpression("^[a-zA-Z][0-9A-Za-z]{20}$")
        validator = QRegularExpressionValidator(regx, self.lineEditZMSZ)
        self.lineEditZMSZ.setValidator(validator)
        # IP掩码
        self.lineEditIp.setInputMask("000.000.000.000;-")
        # MAC掩码
        self.lineEditMAC.setInputMask("HH-HH-HH-HH-HH-HH;#")
        # 日期掩码
        self.lineEditDate.setInputMask("0000-00-00;0")
        # License掩码
        self.lineEditLicense.setInputMask(">NNNN-NNNN-NNNN-NNNN-NNNN;#")
        # 给单行输入栏设置一个按钮
        self.lineEditPwd.setEchoMode(QLineEdit.EchoMode.Password) # 普通密码形式
        self.openIcon = QIcon("icon:open.png")
        self.closeIcon = QIcon("icon:close.png")
        self.pwdAct = QAction(self)
        self.pwdAct.setIcon(self.openIcon)
        self.pwdAct.triggered.connect(self.showPwd)
        self.lineEditPwd.addAction(self.pwdAct, QLineEdit.ActionPosition.TrailingPosition) # 执行动作显示在文本右侧
        # 禁止复制、粘贴、全选等操作
        self.lineEditPwdStop.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)# 不支持上下文菜单
        self.lineEditPwdStop.setEchoMode(QLineEdit.EchoMode.Password)
        # 输入密码不显示
        self.lineEditPwdNoEcho.setEchoMode(QLineEdit.EchoMode.NoEcho)
        # 输入密码开始是明文后自动变成密文
        self.lineEditPwdPlus.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        # 输入呈现普通密码类型
        self.lineEditPwdPlusColor.setEchoMode(QLineEdit.EchoMode.Password)

        # 自动补全
        self.m_model = QStandardItemModel(0, 1, self)
        m_completer = QCompleter(self.m_model, self)
        self.lineEditAutoComplete.setCompleter(m_completer)
        m_completer.activated.connect(self.suffixChoosed)

    def eventFilter(self, object, event):
        '''
        事件过滤器，主要是对密码输入框进行操作的。
        '''
        if object == self.lineEditPwdStop:
            if event.type() == QEvent.Type.MouseMove or event.type() == QEvent.Type.MouseButtonDblClick:
                return True # 鼠标移动、鼠标双击过滤掉
            elif event.type() == QEvent.Type.KeyPress:
                key = QKeyEvent(event.type(), event.key(), event.modifiers()) # 构建键盘事件对象
                if key.matches(QKeySequence.StandardKey.SelectAll) or key.matches(QKeySequence.StandardKey.Copy) or key.matches(QKeySequence.StandardKey.Paste):
                    return True # 键盘全选、复制、粘贴快捷键过滤掉
        return super().eventFilter(object, event)

    def showPwd(self):
        """
        通过按钮设置是否显示密码
        """
        self.isOpen = not self.isOpen
        if self.isOpen:
            self.pwdAct.setIcon(self.openIcon)
            self.lineEditPwd.setEchoMode(QLineEdit.EchoMode.Password) # 密文形式
        else:
            self.pwdAct.setIcon(self.closeIcon)
            self.lineEditPwd.setEchoMode(QLineEdit.EchoMode.Normal) # 明文形式

    def verify(self):
        """
        密码长度校验
        """
        self.lineEditPwdPlusColor.setAutoFillBackground(True) # 自动背景填充
        palette = QPalette() # 创建调色盘
        if len(self.lineEditPwdPlusColor.text()) < 6: # 密码长度小于6位
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.red) # 设置文字颜色
            palette.setColor(QPalette.ColorRole.Base, QColor(255,182,193)) # 设置背景淡粉色
            self.lineEditPwdPlusColor.setPalette(palette) # 将调色盘应用到密码输入栏上
        elif 5 < len(self.lineEditPwdPlusColor.text()) < 9: # 密码长度在6～8位
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.gray) # 灰色
            palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.yellow) # 黄色
            self.lineEditPwdPlusColor.setPalette(palette)
        elif len(self.lineEditPwdPlusColor.text()) > 8: # 密码长度大于8位
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black) # 黑色
            palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white) # 白色
            self.lineEditPwdPlusColor.setPalette(palette)

    def autoComplete(self, url):
        """
        自动补全网址
        url：正在输入的网址
        """
        if self.lineEditAutoComplete.text().count(".") >= 2: # 当.的数量大于等于2时就不自动补全了
            return
        suffixList = [ ".com" , ".cn", ".com.cn", ".org", ".top", ".live", ".net"]
        self.m_model.removeRows(0, self.m_model.rowCount()) # 每次都要清空之前的数据，否则会有大量垃圾数据
        for i in range(0, len(suffixList)):
            self.m_model.insertRow(0)
            self.m_model.setData(self.m_model.index(0, 0), url + suffixList[i])

    def suffixChoosed(self, url):
        """
        选中生成的网址
        url：生成的网址
        """
        self.lineEditAutoComplete.setText(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())