#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   schedule.py
@Time    :   2023/06/24 05:33:37
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 日程提醒

import sys
from PyQt6.QtWidgets import (QCalendarWidget, QApplication, QMenu, QDialog, QWidget, 
                             QFormLayout, QLineEdit, QDialogButtonBox, QTimeEdit, QLabel,
                            QMainWindow, QListWidget, QVBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTime
from PyQt6.QtGui import QBrush, QColor, QFont, QTextCharFormat

class ScheduleDialog(QDialog):

    signal = pyqtSignal(dict) # 发送对话框中日程的信号，类型：dict

    def __init__(self, planDate, Parent=None):
        super().__init__(Parent)
        self.date = planDate.toString("yyyy-MM-dd") # 将传递过来的QDate转换成字符串类型
        self.initUi()

    def initUi(self):
        """对话框控件布局"""
        self.setWindowTitle("新建日程")
        layout = QFormLayout(self)
        self.lineEdit = QLineEdit(self)
        layout.addRow("日程内容(&S)", self.lineEdit)
        layout.addRow("日程日期", QLabel(self.date))
        self.scheduletime = QTimeEdit() # 时间控件
        self.scheduletime.setTime(QTime.currentTime()) # 以现在时间作为开始时间，用户自己可以改
        self.scheduletimeEnd = QTimeEdit()
        self.scheduletimeEnd.setTime(QTime.currentTime().addSecs(3600)) # 预计结束时间是开始时间的后一个小时
        layout.addRow("开始时间(&T)", self.scheduletime)
        layout.addRow("预计结束时间(&E)", self.scheduletimeEnd)
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel) # 增加ok和取消按钮
        layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.setSchedule)
        buttonBox.rejected.connect(self.reject) # 对话框中的取消

    def setSchedule(self):
        """
        发送日程信息
        """
        if self.scheduletimeEnd.time() < self.scheduletime.time(): # 做一个简单起止时间判断
            QMessageBox.warning(self, "警告", "结束时间不能早于开始时间！")
        else:
            scheduleInfo = self.lineEdit.text() # 日程内容
            scheduleTime = self.scheduletime.time().toString()  # 日程开始时间，QTime转成字符串类型
            duration = self.scheduletime.time().secsTo(self.scheduletimeEnd.time()) / 3600

            infomation = "日程内容："+ scheduleInfo + "\n日程日期：" + self.date + "\n开始时间：" + scheduleTime + \
                "\n预计持续时间：" + str(duration) + " 小时\n----------------------------"
            self.signal.emit({self.date:infomation}) #对话框的日程信息发射出去给自定义日历控件
            self.accept() # 对话框中的接受

class MyCalendarWidget(QCalendarWidget):

    scheduleSignal = pyqtSignal(dict) # 发送日程的信号，类型：dict

    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu) # 设置成CustomContextMenu菜单，控件会发出customContextMenuRequested信号
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def show_context_menu(self, pos):
        """
        显示的右键菜单样式
        pos：光标坐标
        """
        date = self.selectedDate()  # 获取当前选中的日期，QDate类型
        menu = QMenu(self)
        action = menu.addAction("添加提醒")
        action.triggered.connect(lambda: self.add_reminder(date))  # 菜单项被点击时触发add_reminder方法
        menu.exec(self.mapToGlobal(pos))
        
    def add_reminder(self, date):
        """
        打开日程提醒对话框
        date：当前选中的日期
        """
        dialog = ScheduleDialog(date, self)
        dialog.signal.connect(self.getSchedule)
        res = dialog.exec()
        if res: # 对于有日程的日期进行格式设置
            font = QFont()
            font.setBold(True) # 加粗
            format = QTextCharFormat()
            format.setFont(font) # 设置字体
            format.setBackground(QBrush(QColor(255, 255, 0))) # 黄色
            format.setForeground(QBrush(QColor(128, 0, 128))) # 紫色
            self.setDateTextFormat(date, format) # 设置当前日期的格式
        
    def getSchedule(self, info):
        self.scheduleSignal.emit(info) # 日程信息发射出去给列表控件
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.pos())
        else:
            super().mousePressEvent(event)

class ScheduleReminder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scheduleDict = {} # 存储日程信息的字典，格式是：{日期:具体的日程}
        self.initUI()

    def initUI(self):
        self.setWindowTitle("日程提醒")

        self.calendar = MyCalendarWidget()
        self.calendar.scheduleSignal.connect(self.saveSchedule)
        self.calendar.selectionChanged.connect(self.update_reminder_list)

        self.reminder_list = QListWidget()
        self.reminder_list.addItem("暂无日程")

        # 添加自定义日历控件和列表控件
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.reminder_list)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.show()

    def update_reminder_list(self):
        """
        刷新提醒日程
        """
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd") # 选中的日期，QDate转字符串格式
        reminder_text = self.scheduleDict.get(selected_date) # 去字典中看看对应的日期是否有日程
        self.reminder_list.clear()
        if reminder_text: # 有日程的话显示日程信息
            self.reminder_list.addItem(reminder_text)
        else:
            self.reminder_list.addItem("暂无日程")
    
    def saveSchedule(self, scheduleInfoDict):
        """
        将日历发送过来的日程信息存入scheduleInfoDict
        scheduleInfoDict：发送过来的日程信息，类型：字典
        """
        self.scheduleDict.update(scheduleInfoDict)
        self.update_reminder_list()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reminder = ScheduleReminder()
    sys.exit(app.exec())
