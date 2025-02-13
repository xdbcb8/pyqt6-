#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   toolbox.py
@Time    :   2023/08/01 19:42:10
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第11章第1节QToolBox

import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QToolButton, QApplication, QToolBox, QGroupBox, QVBoxLayout, QMenu,
                             QDialog, QInputDialog, QMessageBox, QLineEdit, QFormLayout, QPushButton,
                             QFileDialog, QDialogButtonBox, QLabel, QSizePolicy, QFileIconProvider, QWidget)
from PyQt6.QtCore import Qt, pyqtSignal, QProcess, QFileInfo, QSize

class NewTool(QDialog):

    toolSignal = pyqtSignal(list) # 传递工具按钮的名称、路径和图标的信号

    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.provider = QFileIconProvider() # 根据应用程序确定图标
        self.setWindowTitle("设置应用程序的路径")
        layoutd = QFormLayout(self)
        self.title = QLineEdit(self)
        button = QPushButton("单击选择",self)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layoutd.addRow("按钮名称", self.title)
        layoutd.addRow("选择应用程序", button)
        buttonBox = QDialogButtonBox(self)
        buttonBox.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        buttonBox.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        self.exeInfo = QLabel(self)
        layoutd.addWidget(self.exeInfo)
        layoutd.addWidget(buttonBox)
        self.setLayout(layoutd)
        button.clicked.connect(self.selectExE)
        buttonBox.accepted.connect(self.settingExE)
        buttonBox.rejected.connect(self.reject)

    def selectExE(self):
        """
        选择应用程序
        """
        path = QFileDialog.getOpenFileName(self, "选择应用程序", "./", "应用程序 (*.exe)")
        if path:
            self.exeInfo.setText(path[0]) # 把路径显示在对话框窗体上
            self.icon = self.provider.icon(QFileInfo(path[0]))

    def settingExE(self):
        """
        工具按钮名称和路径必须选择后“确定”按钮方可生效
        """
        if not all([self.title.text(), self.exeInfo.text()]):
            return
        self.toolSignal.emit([self.title.text(), self.exeInfo.text(), self.icon]) # 将应用程序的信息通过信号传递出去
        self.accept()

class ToolBox(QToolBox):
    def __init__(self, Parent=None):
        super().__init__(Parent)
        # 自定义右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu) 
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, position):

        context_menu = QMenu(self)
        new_action = QAction("新建分组", self)
        context_menu.addAction(new_action)
        if self.count() > 0:
            rename_action = QAction("重命名分组", self)
            del_action = QAction("删除分组", self)
            tool_action = QAction("新建一个工具", self)
            context_menu.addAction(rename_action)
            context_menu.addAction(del_action)
            context_menu.addAction(tool_action)
        # 连接动作的信号和槽函数
            rename_action.triggered.connect(self.renameItem)
            del_action.triggered.connect(self.delItem)
            tool_action.triggered.connect(self.newTool)
        new_action.triggered.connect(self.newItem)

        # 在指定位置显示自定义菜单
        context_menu.exec(self.mapToGlobal(position))
    
    def newItem(self):
        """
        新增分组
        """
        itemName, isok = QInputDialog.getText(self, "新分组", "分组名称：", text="在这里输入新的分组名称")
        if isok:
            groupbox = QGroupBox()
            vlayout = QVBoxLayout(groupbox)
            # 居中对齐
            vlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            groupbox.setLayout(vlayout)
            self.addItem(groupbox, itemName)

    def renameItem(self):
        """
        重命名分组
        """
        itemNewName, isok = QInputDialog.getText(self, "重命名分组", "分组名称：", text="在这里修改分组名称")
        if isok:
            self.setItemText(self.currentIndex(), itemNewName)

    def delItem(self):
        """
        删除分组
        """
        currentItemText = self.itemText(self.currentIndex()) # 获得当前分组名称
        isok = QMessageBox.question(self, "删除分组", f"确定删除{currentItemText}分组？", defaultButton=QMessageBox.StandardButton.No)
        if isok == QMessageBox.StandardButton.Yes:
            self.removeItem(self.currentIndex())

    def newTool(self):
        """
        新工具按钮
        """
        tool = NewTool(self)
        tool.toolSignal.connect(self.addTool)
        tool.exec()
    
    def addTool(self, info):
        """
        新增工具
        """
        name = info[0] # 按钮名称
        exePath = info[1] # 工具路径
        icon = info[2] # 工具图标
        toolButton = QToolButton()
        toolButton.setIconSize(QSize(32, 32)) # 图标尺寸
        toolButton.setText(name)
        toolButton.setIcon(icon)
        toolButton.setAutoRaise(True)
        # 文字在图标下方
        toolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        vlayout = self.currentWidget().layout() # 获得当前分组的布局
        vlayout.addWidget(toolButton)
        toolButton.clicked.connect(lambda:self.execExE(exePath))

    def execExE(self, path):
        """
        执行第三方程序，这只是一个示例，建议还是通过多线程调用
        """
        process = QProcess()
        process.start(path)  # 第三方exe应用程序的路径

        if process.waitForStarted():
                if process.waitForFinished():  # 等待应用程序完成
                    output = process.readAllStandardOutput()
                    error = process.readAllStandardError()
                    print('输出:', output.data().decode())
                    print('错误:', error.data().decode())
        else:
            QMessageBox.warning(self, "警告", "无法启动应用程序")

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QToolbox举例")
        self.resize(100, 100)
        layout = QVBoxLayout(self)
        toolbox = ToolBox(self)
        layout.addWidget(toolbox)
        self.setLayout(layout)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())