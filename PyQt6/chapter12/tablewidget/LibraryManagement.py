#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   LibraryUI.py
@Time    :   2023/08/10 18:44:25
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第12章第3节QTableWidget--主程序

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QApplication, QTableWidget, QSplitter, QHBoxLayout, QVBoxLayout, QSizePolicy, 
                             QLineEdit, QComboBox, QPushButton, QGroupBox, QLabel, QFormLayout, QTextEdit, QMainWindow, 
                             QTableWidgetItem, QMessageBox, QHeaderView, QMenu)
from PyQt6.QtGui import QAction, QPixmap
from datamanagement import BookManagement
from dialogBook import BookD, BookClassificationSettingD, CountrySettingD

class LibraryM(QMainWindow):
    """
    简单图书管理主界面
    """

    def __init__(self):
        super().__init__()
        self.bookdb = BookManagement() # 图书数据操作对象
        self.booklist = [] # 存放图书的列表
        self.initUI()
        self.showtable()

    def initUI(self):
        self.setWindowTitle("简单图书管理系统")
        self.resize(1200, 600)
        # 主窗体左侧表格等控件布局
        widgetLeft = QWidget()
        self.searchLine = QLineEdit(widgetLeft) # 搜索栏
        self.searchLine.setClearButtonEnabled(True)
        self.combobox = QComboBox(widgetLeft) # 搜索选项
        searchkey = ["书名", "作者", "ISBN"]
        self.combobox.addItems(searchkey)
        searchButton = QPushButton("搜索", widgetLeft) # 搜索按钮
        hlayoutLeft = QHBoxLayout()
        hlayoutLeft.addWidget(self.searchLine)
        hlayoutLeft.addWidget(self.combobox)
        hlayoutLeft.addWidget(searchButton)

        self.bookTable = QTableWidget(widgetLeft) # 图书表格
        self.bookTable.setColumnCount(6) # 6列
        header_labels = ["国家（地区）", "ISBN", "书名", "作者", "图书分类", "价格"]
        for col, header_text in enumerate(header_labels): # 设置表头
            header_item = QTableWidgetItem(header_text)
            self.bookTable.setHorizontalHeaderItem(col, header_item)
        # 第1、3、4列（从0开始）的列宽随内容拓展，其它列的列宽可以手动拓展
        self.bookTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.bookTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.bookTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        # 表格中的右键菜单设置
        self.bookTable.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.bookTable.customContextMenuRequested.connect(self.booktablecontextMenuEvent)
        # 主窗体左侧总体布局
        vlayoutLeft = QVBoxLayout(widgetLeft)
        vlayoutLeft.addLayout(hlayoutLeft)
        vlayoutLeft.addWidget(self.bookTable)
        widgetLeft.setLayout(vlayoutLeft)

        # 主窗体右侧图书详细信息控件布局
        widgetRight = QWidget()
        groupbox = QGroupBox(widgetRight)
        groupbox.setTitle("更多图书信息")
        self.countryLabel = QLabel(groupbox) # 作者国籍
        self.ISBNLabel = QLabel(groupbox) # ISBN编号
        self.titleLabel = QLabel(groupbox) # 书名
        self.authorLabel = QLabel(groupbox) # 作者
        self.BookClassificationLabel = QLabel(groupbox) # 图书分类
        self.PublisherLabel = QLabel(groupbox) # 出版社
        self.PagesLabel = QLabel(groupbox) # 页数
        self.YearPublicationLabel = QLabel(groupbox) # 出版日期
        self.PricingLabel = QLabel(groupbox) # 价格
        self.IntroductionTextEdit = QTextEdit(groupbox) # 图书简介
        self.IntroductionTextEdit.setReadOnly(True)
        self.bookCoversLabel = QLabel(widgetRight) # 图书封面
        formLayout = QFormLayout()
        formLayout.addRow("国    家", self.countryLabel)
        formLayout.addRow("I S B N", self.ISBNLabel)
        formLayout.addRow("书    名", self.titleLabel)
        formLayout.addRow("作    者", self.authorLabel)
        formLayout.addRow("图书分类", self.BookClassificationLabel)
        formLayout.addRow("出版单位", self.PublisherLabel)
        formLayout.addRow("页    数", self.PagesLabel)
        formLayout.addRow("出版年份", self.YearPublicationLabel)
        formLayout.addRow("定    价", self.PricingLabel)
        formLayout.addRow("内容简介", self.IntroductionTextEdit)

        hlayoutRight = QHBoxLayout()
        hlayoutRight.addWidget(self.bookCoversLabel)
        hlayoutRight.addLayout(formLayout)
        groupbox.setLayout(hlayoutRight)

        buttonAdd = QPushButton("新增图书...", widgetRight)
        buttonAdd.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # 主窗体右侧总体布局
        vlayoutRight = QVBoxLayout(widgetRight)
        vlayoutRight.addWidget(groupbox)
        vlayoutRight.addWidget(buttonAdd)

        # 分裂器，左右侧的布局
        splitter = QSplitter(self) # 分裂器
        splitter.addWidget(widgetLeft)
        splitter.addWidget(widgetRight)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        # 设置菜单
        menu = self.menuBar().addMenu("设置(&S)")
        countryAct = QAction("设置国家(&C)", self)
        menu.addAction(countryAct)
        menu.addSeparator()
        BookClassificationAct = QAction("设置分类(&B)", self)
        menu.addAction(BookClassificationAct)

        self.setCentralWidget(splitter) # 设置中央控件
        self.show()

        # 信号与槽连接
        self.combobox.activated.connect(self.settingSearchLine)
        searchButton.clicked.connect(self.searchBook)
        buttonAdd.clicked.connect(self.AddNewBook)
        countryAct.triggered.connect(self.settingCountry)
        BookClassificationAct.triggered.connect(self.settingBookClassification)
        self.bookTable.cellClicked.connect(self.booktable_showmore)
        self.bookTable.cellDoubleClicked.connect(self.execModify)

    def settingSearchLine(self, index):
        """
        选择筛选条件的设置
        index：查找选项索引
        """
        self.searchLine.clear() # 搜索栏清空一下
        if index == 2:
            # 设置成利用ISBN搜索时，搜索栏设置输入掩码，便于输入控制
            self.searchLine.setInputMask("999-9-99999-999-9;*")
        else:
            self.searchLine.setInputMask("")
        self.searchLine.setFocus()

    def searchBook(self):
        """
        查找图书
        """
        op = self.combobox.currentText()
        keyword = self.searchLine.text()
        if not keyword or keyword == "----": # 无搜索内容时无响应
            return
        if op == "书名":
            isquery = self.bookdb.query_book_db(bookname=keyword)
        elif op == "作者":
            isquery = self.bookdb.query_book_db(author=keyword)
        elif op == "ISBN":
            isquery = self.bookdb.query_book_db(isbn=keyword)
        if isquery == -1:
            QMessageBox.information(self, "提示", "没有找到相关的书籍")
        else: # 找到后直接到那一行
            self.bookTable.selectRow(isquery)

    def AddNewBook(self):
        """
        新增图书
        """
        newBook = BookD(0, self.bookdb)
        newBook.refresh.connect(self.refreshdata)
        newBook.exec()

    def settingCountry(self):
        """
        设置国家信息
        """
        newCountry = CountrySettingD(self)
        newCountry.exec()

    def settingBookClassification(self):
        """
        设置图书分类信息
        """
        newBookClassification = BookClassificationSettingD(self)
        newBookClassification.exec()

    def showtable(self):
        """
        表格呈现
        """
        # self.booklist这个变量是我们通过读取存储在硬盘上的“book.dat”来获取整个图书档案列表
        self.booklist = self.bookdb.loadBook()
        list_rows = len(self.booklist)
        table_rows = self.bookTable.rowCount()
        # 分别描述了图书档案中有多少本图书、以及当前表格中有多少行图书信息
        if table_rows == 0 and list_rows > 0:
            self.selectTable(self.booklist)
            # 原来没有书的话就直接载入书
        elif table_rows > 0 and list_rows > 0:
            # 原来有图书的话，再次新增图书的话，我们要先将原来的表格中全部行删除，再重载表格数据。
            self.removeRows(table_rows)
            self.selectTable(self.booklist)
            
    def selectTable(self, booklist):
        """
        表格呈现具体的数据
        """
        for i, book in enumerate(booklist):
            isbn = book["isbn"]
            country = book["country"]
            subtitle = book["subtitle"]
            author = book["author"]
            price = book["price"]
            classification = book["classification"] 
            # 往表格中第i行插入一个空行
            self.bookTable.insertRow(i)
            
            # 在表格中插入图书信息，都是水平、垂直居中
            isbn_item = QTableWidgetItem(isbn)
            isbn_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            isbn_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)  # 设置单元格的标志位：可以选择和启用，不可编辑

            country_item = QTableWidgetItem(country)
            country_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            country_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled) 

            bookname_item = QTableWidgetItem(subtitle)
            bookname_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            bookname_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled) 

            author_item = QTableWidgetItem(author)
            author_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            author_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled) 

            classification_item = QTableWidgetItem(classification)
            classification_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            classification_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled) 

            price_item = QTableWidgetItem(str(price))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            price_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled) 

            self.bookTable.setItem(i, 0, country_item)
            self.bookTable.setItem(i, 1, isbn_item)
            self.bookTable.setItem(i, 2, bookname_item)
            self.bookTable.setItem(i, 3, author_item)
            self.bookTable.setItem(i, 4, classification_item)
            self.bookTable.setItem(i, 5, price_item)

    def booktable_showmore(self, row, column):
        """
        单击显示图书详细信息
        """
        if self.bookTable.rowCount() > 0: # 至少要有一本书
            self.countryLabel.setText(self.booklist[row]["country"])
            self.ISBNLabel.setText(self.booklist[row]["isbn"])
            self.titleLabel.setText(self.booklist[row]["subtitle"])
            self.authorLabel.setText(self.booklist[row]["author"])
            self.PublisherLabel.setText(self.booklist[row]["publisher"])
            self.PricingLabel.setText(str(self.booklist[row]["price"]))
            self.YearPublicationLabel.setText(self.booklist[row]["pubdate"])
            self.BookClassificationLabel.setText(self.booklist[row]["classification"])           
            self.PagesLabel.setText(str(self.booklist[row]["pages"]))
            self.IntroductionTextEdit.setText(self.booklist[row]["summary"])
            img = self.booklist[row]["img"]
            bookcover = QPixmap(img)
            if bookcover.isNull(): # 如果图书封面无法显示的处理
                self.bookCoversLabel.setText("应该是图书封面的路径有问题，<p><b>双击表格</b>中的图书修改一下。")
            else:
                self.bookCoversLabel.setPixmap(QPixmap(img))

    def execModify(self, row, column):
        """
        执行修改图书
        """
        if self.bookTable.rowCount() > 0:
            # 图书的各种信息
            tablerow = row # 图书记录在booklist的位置的
            isbn = self.booklist[row]["isbn"]
            country = self.booklist[row]["country"]
            title = self.booklist[row]["subtitle"]
            author = self.booklist[row]["author"]
            publisher = self.booklist[row]["publisher"]
            price = self.booklist[row]["price"]
            pubdate = self.booklist[row]["pubdate"]
            classification = self.booklist[row]["classification"]
            pages = self.booklist[row]["pages"]
            introduction = self.booklist[row]["summary"]
            img = self.booklist[row]["img"]
            bookinfo = [isbn, country, title, author, publisher, price, pubdate, classification, pages, introduction, img]
            modifyBook = BookD(1, self.bookdb, self.booklist, tablerow)
            modifyBook.loadBookData(bookinfo)
            modifyBook.refresh.connect(self.refreshdata) # 修改后刷新一下图书表格
            modifyBook.exec()

    def refreshdata(self, n):
        """
        刷新表格中的数据
        n：行号
        """
        self.showtable()
        if n != -100: # 不等于-100表明是修改图书
            self.bookTable.setCurrentCell(n, 0)
            self.bookTable.cellClicked.emit(n, 0)

    def booktablecontextMenuEvent(self, position):
        """
        右键菜单
        """
        if self.bookTable.rowCount() > 0:
            pmenu = QMenu(self)
            pDeleteAct = QAction("删除此行", self.bookTable)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleterows)
            pmenu.exec(self.bookTable.mapToGlobal(position))

    def deleterows(self):
        """
        删除行
        """
        isyes = QMessageBox.warning(self, "注意", "确认删除？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, defaultButton=QMessageBox.StandardButton.No)
        if isyes == QMessageBox.StandardButton.Yes:
            curow = self.bookTable.currentRow()
            selections = self.bookTable.selectionModel()
            selectedsList = selections.selectedRows()
            rows = []
            for r in selectedsList:
                rows.append(r.row())
            print(rows)
            if len(rows) == 0:
                rows.append(curow)
            self.removeRows(rows, isdel_list=1) # 当我们选中一个单元格的时候，其实行是没有选中的，所以我们给rows列表增加当前行。如果直接选了行，则就增加我们选中的行。然后就可以删除了。
            # 删除完毕后，回到第一个单元格，并模拟单击一下，使得右侧更多图书信息也更新一下，避免留下残留信息
            self.bookTable.setCurrentCell(0, 0)
            self.bookTable.cellClicked.emit(0, 0)

    def removeRows(self, rows, isdel_list = 0):
        """
        删除单元格
        isdel_list：判断是否全部删除图书数据，默认是全部删除
        """
        if isdel_list != 0:
            rows.reverse()
            # 倒序删除，否则可能会出错！

            for i in rows:
                self.bookTable.removeRow(i)
                del self.booklist[i]
            self.bookdb.save_book_db(self.booklist)
            # 先从表格中删除第i行及其所有项目，然后删除self.booklist中的。最后保存一下。
        else:
            for i in range(rows-1, -1, -1):
                self.bookTable.removeRow(i)
                # 清除表格中的所有行（注意不是内容，而是包括行及其单元格对象）
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LibraryM()
    sys.exit(app.exec())