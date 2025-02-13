#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   LibraryUI.py
@Time    :   2023/08/10 18:44:25
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第12章第3节QTableWidget--对话框程序

import os
from PyQt6.QtCore import QEvent, Qt, QDate, pyqtSignal
from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel, QFormLayout,
                             QTextEdit, QDialog, QSpinBox, QDateEdit, QDialogButtonBox, QFileDialog, QListWidget, 
                             QMessageBox)
from PyQt6.QtGui import QPixmap
from datamanagement import CountryManagement, ClassificationManagement

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class BookD(QDialog):
    """
    新增/修改图书对话框
    """
    refresh = pyqtSignal(int) # 让表格中的数据刷新一下，参数是修改图书时对应表格中图书的行号

    def __init__(self, flag, db, booklist=[], tablerow=0, Parent=None):
        super().__init__(Parent)
        self.bookdbM = db # 图书数据操作对象
        self.booklist = booklist # 图书载入后的列表
        self.tablerow = tablerow # 记录在表格中行号
        self.flag = flag # 标志，判断是修改还是新增图书
        self.initUI()
        self.loadData()

    def initUI(self):
        """
        图书界面
        """
        # 控件布置
        self.countrycombox = QComboBox(self) # 作者国家
        self.ISBNLine = QLineEdit(self) # ISBN编号
        self.titleLine = QLineEdit(self) # 书名
        self.authorLine = QLineEdit(self) # 作者
        self.BookClassificationcombox = QComboBox(self) # 图书分类
        self.PublisherLine = QLineEdit(self) # 出版社
        self.Pagesspinbox = QSpinBox(self) # 页数
        self.YearPublicationDate = QDateEdit(self) # 出版日期
        self.Pricingdouspinbox = QSpinBox(self) # 价格
        self.IntroductionTextEditD = QTextEdit(self) # 图书简介
        self.buttonBox = QDialogButtonBox(self) # 确定/取消
        # 默认图书封面
        self.bookCoversLabel = QLabel(self)
        self.bookcoverFineName = current_dir + "\\res\\book\\BookCovers.png"
        self.bookCoversLabel.setPixmap(QPixmap(str(self.bookcoverFineName)))
        # 对话框右侧图书信息布局
        formLayout = QFormLayout()
        formLayout.addRow("国    家", self.countrycombox)
        formLayout.addRow("I S B N", self.ISBNLine)
        formLayout.addRow("书    名", self.titleLine)
        formLayout.addRow("作    者", self.authorLine)
        formLayout.addRow("图书分类", self.BookClassificationcombox)
        formLayout.addRow("出版单位", self.PublisherLine)
        formLayout.addRow("页    数", self.Pagesspinbox)
        formLayout.addRow("出版年份", self.YearPublicationDate)
        formLayout.addRow("定    价", self.Pricingdouspinbox)
        formLayout.addRow("内容简介", self.IntroductionTextEditD)
        formLayout.addWidget(self.buttonBox)
        # 图书封面布局
        vlayout = QVBoxLayout()
        vlayout.addStretch()
        vlayout.addWidget(self.bookCoversLabel)
        vlayout.addWidget(QLabel("双击图片可以更换封面"))
        vlayout.addStretch()
        # 对话框布局
        hlayout = QHBoxLayout(self)
        hlayout.addLayout(vlayout)
        hlayout.addLayout(formLayout)
        self.setLayout(hlayout)
        # 控件设置
        self.ISBNLine.setClearButtonEnabled(True)
        self.ISBNLine.setInputMask("999-9-99999-999-9;*") # ISBN编码输入控制
        self.titleLine.setClearButtonEnabled(True)
        self.authorLine.setClearButtonEnabled(True)
        self.PublisherLine.setClearButtonEnabled(True)
        self.Pagesspinbox.setRange(1, 10000) # 页面设置
        self.YearPublicationDate.setCalendarPopup(True)
        self.Pricingdouspinbox.setRange(1, 10000) # 价格设置
        buttonOK = self.buttonBox.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        buttonCancel = self.buttonBox.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        self.bookCoversLabel.installEventFilter(self) # 安装事件过滤器，便于能换图书封面
        if self.flag == 0:
            self.setWindowTitle("新增图书")
            self.ISBNLine.setEnabled(True) # 新增图书ISBN号可以编辑
        else:
            self.setWindowTitle("修改图书")
            self.ISBNLine.setEnabled(False) # 修改图书ISBN号不可以编辑
        # 信号与槽连接
        buttonOK.clicked.connect(self.ModifyOrNewBook)
        buttonCancel.clicked.connect(self.reject)
    
    def ModifyOrNewBook(self):
        """
        新增或者修改图书
        """
        country = self.countrycombox.currentText() # 作者国家
        isbn = self.ISBNLine.text() # ISBN编号
        title = self.titleLine.text() # 书名
        author = self.authorLine.text() # 作者
        classification = self.BookClassificationcombox.currentText() # 图书分类
        publisher = self.PublisherLine.text() # 出版社
        pages = self.Pagesspinbox.value() # 页数
        publishdate = self.YearPublicationDate.date().toString("yyyy-MM-dd") # 出版日期
        price = self.Pricingdouspinbox.value() # 价格
        introduction = self.IntroductionTextEditD.toPlainText() # 图书简介
        img = self.bookcoverFineName # 图书封面
        # 部分内容不能为空
        if all([country, title, author, publisher, introduction]) and isbn != "----":
            currentbooinfo =  self.get_bookinfo(isbn, title, author, publishdate, classification, publisher, price, pages, introduction, img, country)
            if self.flag == 0: # 新增图书
                insertok = self.bookdbM.insert_book_db(currentbooinfo)
                if insertok == -1:
                    QMessageBox.information(self, "提示", "已经有重复ISBN的书存储了！")
                else:
                    self.refresh.emit(-100) # -100信号表明是新增图书
                    self.accept()
            else: # 修改图书
                self.booklist[self.tablerow] = currentbooinfo # 将当前图书信息保存其在self.booklist中的位置
                self.bookdbM.save_book_db(self.booklist)
                self.refresh.emit(self.tablerow) # 将该图书对应表格中的行号也传递出去
                self.accept()
        else:
            QMessageBox.information(self, "提示", "部分内容未填写！")

    def eventFilter(self, object, event):
        """
        双击图书封面，更换图书封面
        """
        if object == self.bookCoversLabel:
            if event.type() == QEvent.Type.MouseButtonDblClick:
                bookcoverPath = QFileDialog.getOpenFileName(self, "选择图片", "./", "图片文件 (*.png *.jpg)")
                if bookcoverPath[0]:
                    self.bookCoversLabel.setPixmap(QPixmap(bookcoverPath[0]))
                    self.bookcoverFineName = bookcoverPath[0]
        return super().eventFilter(object, event)
    
    def loadData(self):
        """
        载入国家、分类信息
        """
        countryList = CountryManagement().loadCountry() # 国家数据
        currentClassificationList = ClassificationManagement().loadClassification() # 分类数据
        self.countrycombox.addItems(countryList)
        self.BookClassificationcombox.addItems(currentClassificationList)

    def loadBookData(self, bookinfo):
        """
        载入图书数据
        bookinfo：图书信息
        """
        self.countrycombox.setCurrentText(bookinfo[1]) # 作者国家
        self.ISBNLine.setText(bookinfo[0]) # ISBN编号
        self.titleLine.setText(bookinfo[2]) # 书名
        self.authorLine.setText(bookinfo[3]) # 作者
        self.BookClassificationcombox.setCurrentText(bookinfo[7]) # 图书分类
        self.PublisherLine.setText(bookinfo[4]) # 出版社
        self.Pagesspinbox.setValue(bookinfo[8]) # 页数
        self.YearPublicationDate.setDate(QDate.fromString(bookinfo[6], "yyyy-M-dd")) # 出版日期
        self.Pricingdouspinbox.setValue(bookinfo[5]) # 价格
        self.IntroductionTextEditD.setText(bookinfo[9]) # 图书简介
        self.bookcoverFineName = bookinfo[10] # 图书封面
        bookcover = QPixmap(self.bookcoverFineName)
        if bookcover.isNull(): # 如果图书封面为空
            self.bookCoversLabel.setText("应该是封面的位置不对，<p><b>双击这里</b>试着重新选择一下封面，<p>默认封面在当前目录下的<p>res/book<p><p>")
        else:
            self.bookCoversLabel.setPixmap(QPixmap(self.bookcoverFineName))

    def get_bookinfo(self, isbn, subtitle, author, pubdate, classification, publisher, price, pages, summary, img, country):
        """
        返回图书信息，本质上每本图书时一个字典，所有的字典会统一放到一个列表中
        """
        book = {"isbn" : isbn, "subtitle" : subtitle, "author" : author, "pubdate" : pubdate, "classification" : classification, 
                "publisher" : publisher, "price" : price, "pages" : pages, "summary" : summary, "img" : img, "country" : country
                }
        return book

class CountrySettingD(QDialog):
    """
    作者所在国家管理
    """
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.currentCountryList = [] # 记录载入数据时的国家名称
        self.initUI()
        self.loadData()
    
    def initUI(self):
        # 控件布置
        self.setWindowTitle("作者国家管理")
        self.comboboxOP = QComboBox(self)
        self.comboboxOP.addItems(["增加", "修改", "删除"])
        self.newCountry = QLineEdit(self)
        self.newCountry.setClearButtonEnabled(True)
        self.buttonop = QPushButton("新增国家", self)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonOKCountry = self.buttonBox.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonCancelCountry = self.buttonBox.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        # 布局
        formlayout = QFormLayout()
        formlayout.addRow("操作方式：", self.comboboxOP)
        formlayout.addRow("国家名称：", self.newCountry)
        formlayout.addRow("开始操作：", self.buttonop)
        formlayout.addWidget(self.buttonBox)
        self.countryListWidget = QListWidget(self)
        hlayout = QHBoxLayout(self)
        hlayout.addWidget(self.countryListWidget)
        hlayout.addLayout(formlayout)
        self.setLayout(hlayout)
        # 信号与槽连接
        self.countryListWidget.itemPressed.connect(self.premodify)
        self.comboboxOP.activated.connect(self.settingButton)
        self.buttonop.clicked.connect(self.operate)
        self.buttonOKCountry.clicked.connect(self.saveCountryList)
        self.buttonCancelCountry.clicked.connect(self.reject)
    
    def loadData(self):
        """
        载入国家数据，并放入到国家列表控件中
        """
        self.countryM = CountryManagement()
        self.currentCountryList = self.countryM.loadCountry()
        if self.currentCountryList:
            self.countryListWidget.addItems(self.currentCountryList)

    def saveCountryList(self):
        """
        保存国家数据
        """
        self.countryM.save_country_db(self.currentCountryList)
        self.accept()

    def settingButton(self, n):
        """
        根据下拉框的选择修改操作按钮
        """
        self.newCountry.clear() # 每次下拉框变化时新国家输入栏要清空
        if n == 0:
            self.buttonop.setText("新增国家")
            self.newCountry.setEnabled(True) # 新国家输入栏启用
        elif n == 1:
            self.buttonop.setText("修改国家")
            self.newCountry.setEnabled(True)
        else:
            self.buttonop.setText("删除国家")
            self.newCountry.setEnabled(False) # 新国家输入栏禁用

    def operate(self):
        """
        操作
        """
        if self.sender().text() == "新增国家":
            self.addCountry()
        elif self.sender().text() == "修改国家":
            self.modifyCountry()
        else: # 删除国家
            self.delCountry()

    def addCountry(self):
        """
        新增国家
        """
        newCountry = self.newCountry.text()
        # 国家名称不能为空或者不能重复才能新增
        if not newCountry or self.countryListWidget.findItems(newCountry, Qt.MatchFlag.MatchExactly):
            return
        self.countryListWidget.addItem(newCountry)
        self.currentCountryList.append(newCountry)

    def premodify(self, currentItem):
        """
        准备修改国家信息
        """
        currentCountry = currentItem.text()
        if self.buttonop.text() != "新增国家":
            self.newCountry.setText(currentCountry)

    def modifyCountry(self):
        """
        修改国家信息
        """
        newcountry = self.newCountry.text() # 新国家名称
        if newcountry and self.countryListWidget.currentItem(): # 只有选中的列表中国家及新国家名称都有时才能修改
            oldCountry = self.countryListWidget.currentItem().text() # 旧国家名称
            oldcountryIndex = self.countryListWidget.currentIndex().row() # 旧国家索引的行号
            self.countryListWidget.takeItem(oldcountryIndex) # 删除旧国家
            self.countryListWidget.insertItem(oldcountryIndex, newcountry) # 在旧国家位置处添加新国家名称
            # 更新self.currentCountryList中的国家数据
            self.currentCountryList.remove(oldCountry)
            self.currentCountryList.insert(oldcountryIndex, newcountry)

    def delCountry(self):
        """
        删除国家信息
        """
        country = self.newCountry.text()
        # 列表控件中至少保留一个国家，且待删除的国家必须要在国家输入栏的位置出现
        if self.countryListWidget.count() > 1 and country:
            isdel = QMessageBox.question(self, "删除", "删除这个国家？",defaultButton=QMessageBox.StandardButton.No)
            if isdel == QMessageBox.StandardButton.Yes:
                self.countryListWidget.takeItem(self.countryListWidget.currentIndex().row())
                self.currentCountryList.remove(country)
                self.countryListWidget.setCurrentRow(0)
                self.newCountry.setText(self.countryListWidget.currentItem().text())

class BookClassificationSettingD(QDialog):
    """
    图书分类管理
    """
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.currentClassificationList = [] # 记录载入数据时的分类名称
        self.initUI()
        self.loadData()
    
    def initUI(self):
        # 控件布置
        self.setWindowTitle("图书分类管理")
        self.resize(600, 600)
        self.comboboxOP = QComboBox(self)
        self.comboboxOP.addItems(["增加", "修改", "删除"])
        self.newBookClassification = QLineEdit(self)
        self.newBookClassification.setClearButtonEnabled(True)
        self.buttonop = QPushButton("新增分类", self)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonOKClassification = self.buttonBox.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonCancelClassification = self.buttonBox.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        # 布局
        formlayout = QFormLayout()
        formlayout.addRow("操作方式：", self.comboboxOP)
        formlayout.addRow("图书分类：", self.newBookClassification)
        formlayout.addWidget(self.buttonop)
        formlayout.addWidget(self.buttonBox)
        self.bookClassificationWidget = QListWidget(self)
        hlayout = QHBoxLayout(self)
        hlayout.addWidget(self.bookClassificationWidget)
        hlayout.addLayout(formlayout)
        self.setLayout(hlayout)
        # 信号与槽连接
        self.bookClassificationWidget.itemPressed.connect(self.premodify)
        self.comboboxOP.activated.connect(self.settingButton)
        self.buttonop.clicked.connect(self.operate)
        self.buttonOKClassification.clicked.connect(self.saveClassificationList)
        self.buttonCancelClassification.clicked.connect(self.reject)

    def loadData(self):
        """
        载入分类数据
        """
        self.classificationM = ClassificationManagement()
        self.currentClassificationList = self.classificationM.loadClassification()
        if self.currentClassificationList:
            self.bookClassificationWidget.addItems(self.currentClassificationList)

    def saveClassificationList(self):
        """
        保存分类数据
        """
        self.classificationM.save_classification_db(self.currentClassificationList)
        self.accept()

    def settingButton(self, n):
        """
        根据下拉框的选择修改操作按钮
        """
        self.newBookClassification.clear() # 每次下拉框选项变化时新分类输入栏要清空
        if n == 0:
            self.buttonop.setText("新增分类")
            self.newBookClassification.setEnabled(True) # 新分类输入栏启用
        elif n == 1:
            self.buttonop.setText("修改分类")
            self.newBookClassification.setEnabled(True)
        else:
            self.buttonop.setText("删除分类")
            self.newBookClassification.setEnabled(False) # 新分类输入栏禁用

    def operate(self):
        """
        操作
        """
        if self.sender().text() == "新增分类":
            self.addClassification()
        elif self.sender().text() == "修改分类":
            self.modifyClassification()
        else: # 删除分类
            self.delClassification()

    def addClassification(self):
        """
        新增分类
        """
        newClassification = self.newBookClassification.text()
        # 分类名称不能为空或者不能重复才能新增
        if not newClassification or self.bookClassificationWidget.findItems(newClassification, Qt.MatchFlag.MatchExactly):
            return
        self.bookClassificationWidget.addItem(newClassification)
        self.currentClassificationList.append(newClassification)

    def premodify(self, currentItem):
        """
        准备修改分类信息
        """
        currentClassification = currentItem.text()
        if self.buttonop.text() != "新增分类":
            self.newBookClassification.setText(currentClassification)

    def modifyClassification(self):
        """
        修改分类信息
        """
        newClassification = self.newBookClassification.text() # 新分类名称
        if newClassification and self.bookClassificationWidget.currentItem(): # 只有选中的列表中分类及新分类名称都有时才能修改
            oldClassification = self.bookClassificationWidget.currentItem().text() # 旧分类名称
            oldClassificationIndex = self.bookClassificationWidget.currentIndex().row() # 旧分类索引的行号
            self.bookClassificationWidget.takeItem(oldClassificationIndex) # 删除旧分类
            self.bookClassificationWidget.insertItem(oldClassificationIndex, newClassification) # 在旧分类位置处添加新分类名称
            self.currentClassificationList.remove(oldClassification)
            self.currentClassificationList.insert(oldClassificationIndex, newClassification)

    def delClassification(self):
        """
        删除分类信息
        """
        classification = self.newBookClassification.text()
        # 至少保留一个分类，且待删除的分类必须出现在分类输入栏时才能删除
        if classification and self.bookClassificationWidget.count() > 1:
            isdel = QMessageBox.question(self, "删除", "删除这个分类？",defaultButton=QMessageBox.StandardButton.No)
            if isdel == QMessageBox.StandardButton.Yes:
                self.bookClassificationWidget.takeItem(self.bookClassificationWidget.currentIndex().row())
                self.currentClassificationList.remove(classification)
                self.bookClassificationWidget.setCurrentRow(0)
                self.newBookClassification.setText(self.bookClassificationWidget.currentItem().text())