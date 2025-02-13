#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   TableDelegate.py
@Time    :   2023/08/21 13:05:36
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 第13章第3节QTableView--代理

from datetime import datetime
from PyQt6.QtWidgets import QStyledItemDelegate, QComboBox, QSpinBox, QApplication, QStyle, QStyleOptionProgressBar, QDateEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from Circle import CircleRating

## ==============客户等级显示的代理====================

class CircleshowD(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def setItems(self, itemList):
        self.itemList = itemList

    def paint(self, painter, option, index):
        '''
        画圆圈
        '''
        level = int(index.data())  # 客户等级
        circle = CircleRating(maxCount = level)
        circle.paint(painter, option.rect)

    ## 自定义代理必须继承以下4个方法
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.setFrame(False)
        editor.addItems(self.itemList)
        return editor

    def setEditorData(self, editor, index):
        model = index.model()
        text = model.data(index, Qt.ItemDataRole.DisplayRole)
        levelList = ["一级", "二级", "三级", "四级", "五级"] # 根据客户等级（数字）从列表中确定客户等级（文字），并设置成当前下拉框的文字
        editor.setCurrentText(levelList[int(text)-1])

    def setModelData(self, editor, model, index):
        text = editor.currentText()
        leveldic = {"一级":1, "二级":2, "三级":3, "四级":4, "五级":5}
        reallevel = leveldic.get(text)
        model.setData(index, reallevel, Qt.ItemDataRole.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

## ==============客户性别的代理====================

class SexD(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def setItems(self, itemList):
        self.itemList = itemList

    ## 自定义代理必须继承以下4个方法
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent) # 客户性别下拉框
        editor.setFrame(False)
        editor.addItems(self.itemList)
        return editor

    def setEditorData(self, editor, index):
        model = index.model()
        sex = model.data(index, Qt.ItemDataRole.DisplayRole)
        editor.setCurrentText(sex)

    def setModelData(self, editor, model, index):
        realsex = editor.currentText()
        model.setData(index, realsex, Qt.ItemDataRole.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

## ==============客户国籍的代理====================

class CountryD(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def setItems(self, itemList,):
        self.itemList = itemList

    ## 自定义代理必须继承以下4个方法
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent) # 客户国籍下拉框
        editor.setFrame(False)
        editor.addItems(self.itemList)
        return editor

    def setEditorData(self, editor, index):
        model = index.model()
        sex = model.data(index, Qt.ItemDataRole.DisplayRole)
        editor.setCurrentText(sex)

    def setModelData(self, editor, model, index):
        realcountry = editor.currentText()
        model.setData(index, realcountry, Qt.ItemDataRole.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

## ==============客户收入的代理====================
class IncomeD(QStyledItemDelegate):
    def __init__(self):
        super().__init__() 

## 自定义代理组件必须继承以下4个方法
    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent) # 客户收入输入框
        editor.setFrame(False)
        editor.setRange(8, 100)  # 客户收入8-100
        return editor

    def setEditorData(self,editor,index):
        model = index.model()
        income = model.data(index, Qt.ItemDataRole.DisplayRole)
        editor.setValue(int(income))

    def setModelData(self,editor,model,index):
        realincome = editor.value()
        model.setData(index, realincome, Qt.ItemDataRole.DisplayRole)

    def updateEditorGeometry(self,editor,option,index):
        editor.setGeometry(option.rect)

## ==============洽谈进度的代理====================
class ProgressD(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def paint(self, painter, option, index):
        progress_value = int(index.data())  # 洽谈进度
        progressWidget = QStyleOptionProgressBar()
        progressWidget.rect = option.rect
        progressWidget.minimum = 1
        progressWidget.maximum = 100
        progressWidget.progress = progress_value
        progressWidget.text = str(progress_value) + "%"
        progressWidget.textVisible = True

        painter.save()
        QApplication.style().drawControl(QStyle.ControlElement.CE_ProgressBar, progressWidget, painter)  # 画进度条
        painter.restore()

## 自定义代理组件必须继承以下4个方法
    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent) # 洽谈进度输入框
        editor.setFrame(False)
        editor.setRange(1, 100)
        return editor

    def setEditorData(self,editor,index):
        model = index.model()
        progress = model.data(index, Qt.ItemDataRole.DisplayRole)
        editor.setValue(int(progress))

    def setModelData(self,editor,model,index):
        realprogress = editor.value()
        model.setData(index, realprogress, Qt.ItemDataRole.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

## ==============客户生日的代理====================

class BirthdateD(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setFrame(False)
        editor.setCalendarPopup(True)
        return editor

    def setEditorData(self, editor, index):
        model = index.model()
        birthdate = model.data(index, Qt.ItemDataRole.DisplayRole)
        dt = datetime.strptime(birthdate, "%Y/%m/%d") # 将数据按格式转化成日期对象
        editor.setDate(dt)

    def setModelData(self, editor, model, index):
        birth = editor.date().toPyDate()
        dt =birth.strftime("%Y/%m/%d")  # 按格式转换成字符串
        model.setData(index, dt, Qt.ItemDataRole.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)