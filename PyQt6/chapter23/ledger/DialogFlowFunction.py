#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DialogFlowFunction.py
@Time    :   2024/02/04 12:26:35
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot, QModelIndex, QDate, QItemSelectionModel, Qt
from PyQt6.QtWidgets import QWidget, QHeaderView
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from datamanagement import FlowFunds
from Ui_DialogFlow import Ui_Form_Flow
from DialogFlowDetailFunction import DialogFlowDetailFunction

# 流水展示

class Form_FlowFunction(QWidget, Ui_Form_Flow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.flag = "out" # 收、支分类的标志，默认支出
        self.dateStart, self.dateEditEnd = "", "" # 开始日期和结束日期
        self.pages = 1  # 总的页数
        self.currentPage = 1  # 当前页数
        self.setDateInterval()
        self.initTable()

    def setDateInterval(self):
        """
        设置默认的日期区间是当前月份的第一天和最后一天
        """
        firstDayOfMonth = QDate(QDate.currentDate().year(), QDate.currentDate().month(), 1) # 当前月份的第一天
        lastDayOfMonth = firstDayOfMonth.addMonths(1).addDays(-1) # 当前月份的最后一天
        self.dateEdit_start.setDate(firstDayOfMonth)
        self.dateEdit_end.setDate(lastDayOfMonth)

    def setHeadView(self):
        """
        设置表头
        """
        headerTitle = ['日    期', '一级账户', '二级账户', '一级分类', '二级分类', '金    额']
        self.model.setHorizontalHeaderLabels(headerTitle)  # 设置表头

    def initTable(self):
        """
        表格初始化
        """
        self.flowfundsM = FlowFunds()
        self.table_Row = 30  # 原始表格数据为30行
        self.table_Column = 8 # 原始表格数据为8列

        self.tableView_flowfunds.verticalHeader().setDefaultSectionSize(22)  # 默认行高22
        self.tableView_flowfunds.setAlternatingRowColors(True)  # 交替行颜色

        self.model = QStandardItemModel(self.table_Row, self.table_Column, self)
        self.tableView_flowfunds.setModel(self.model)  # 设置数据模型

        self.tableView_flowfunds.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # 列宽自动分配

        self.selectionModel = QItemSelectionModel(self.model)  # Item选择模型
        self.tableView_flowfunds.setSelectionModel(self.selectionModel)

        self.tableView_flowfunds.setSortingEnabled(True) # 可排序

        qss = """/* 设置QTableView的整体样式 */  
QTableView {  
    border: 1px solid #8f8f91; /* 边框颜色和宽度 */  
    background-color: #f0f0f0; /* 背景色 */  
    gridline-color: #d0d0d0; /* 网格线颜色 */  
    alternate-background-color: #e0e0e0; /* 交替行背景色 */ 
    font-family: 'Microsoft YaHei'; /* 字体设置为微软雅黑 */  
    font-size: 12pt; /* 字体大小设置为12号 */   
}  
  
/* 设置QTableView的标题栏样式 */  
QTableView QHeaderView::section {  
    background-color: #c0c0c0; /* 标题栏背景色 */  
    border: none; /* 去除标题栏边框 */  
    padding: 4px; /* 标题栏内边距 */  
    font-family: 'Microsoft YaHei'; /* 标题栏字体 */  
    font-size: 12pt; /* 标题栏字体大小 */  
    color: black; /* 标题栏字体颜色 */  
}  
 """
        self.setStyleSheet(qss)
        self.showTableContent(self.dateStart, self.dateEnd, (self.currentPage-1)*30, 30) # 分页显示表格内容

    def showTableContent(self, dateS, dateE, start, end):
        """
        表格内容展示
        dateS：开始日期
        dateE：结束日期
        start：开始数据
        end：结束数据
        """
        self.model.clear() # 每次先将数据清空
        self.setHeadView()
        rowItems = self.flowfundsM.loadAllFlowfunds(self.flag, dateS, dateE, start, end)
        if rowItems:
            if len(rowItems) < 30: # 流水记录数量小于30，返回的就是记录数量，否则就是30行的记录
                self.table_Row = len(rowItems)
            else:
                self.table_Row = 30
            for i in range(self.table_Row):
                for j in range(self.table_Column):
                    item = QStandardItem(str(rowItems[i][j]))
                    if j == 0:
                        dateTimestr = rowItems[i][j].toString("yyyy-MM-dd HH:mm") # 记录的日期时间
                        item = QStandardItem(dateTimestr)
                    if j in [3, 4] and rowItems[i][j] == None:
                        item = QStandardItem("")      
                    self.model.setItem(i, j, item)
                    self.model.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)  # 表格内容居中
        self.tableView_flowfunds.setColumnHidden(6, True) # 第6、7列隐藏，这个在详情中显示
        self.tableView_flowfunds.setColumnHidden(7, True)
        self.cnt_pages(dateS, dateE)

    def reflushTable(self):
        """
        刷新表格数据
        """
        self.pushButton_select.clicked.emit()
        

    def cnt_pages(self, dateStart, dateEnd):
        """
        一共多少页的数据
        """
        page = self.flowfundsM.totalPages(self.flag, dateStart, dateEnd)
        if page:
            if page[0][0] % 30 == 0:
                self.pages = page[0][0] // 30
            else:
                self.pages = page[0][0] // 30 + 1
            self.label_pages.setText(f"第{self.currentPage}/{self.pages}页")
            if self.currentPage == 1:
                self.pushButton_up.setEnabled(False)  # 当前页为第一页，上一页禁用
            if self.currentPage == self.pages:
                self.pushButton_down.setEnabled(False)  # 当前页为总页数，下一页禁用
            if self.pages > 1 and self.currentPage != self.pages:  # 当总的页数大于1，且当前页数不是总的页数时
                self.pushButton_down.setEnabled(True)  # 下一页启用
                self.toolButton_go.setEnabled(True)  # 跳转页启用
                self.spinBox_page.setEnabled(True)  # 跳转框启用

    @pyqtSlot(QDate)
    def on_dateEdit_start_dateChanged(self, date):
        """
        开始日期选择
        """
        self.dateStart = date.toString("yyyy-MM-dd")

    @pyqtSlot(QDate)
    def on_dateEdit_end_dateChanged(self, date):
        """
        结束日期选择
        """
        self.dateEnd = date.toString("yyyy-MM-dd")

    @pyqtSlot()
    def on_radioButton_out_clicked(self):
        """
        选择支出
        """
        self.flag = "out"

    @pyqtSlot()
    def on_radioButton_in_clicked(self):
        """
        选择收入
        """
        self.flag = "in"

    @pyqtSlot()
    def on_pushButton_select_clicked(self):
        """
        筛选
        """
        self.currentPage = 1 # 回到第一页
        self.spinBox_page.setValue(1)
        self.showTableContent(self.dateStart, self.dateEnd, (self.currentPage-1)*30, 30)
        self.cnt_pages(self.dateStart, self.dateEnd)

    @pyqtSlot(QModelIndex)
    def on_tableView_flowfunds_activated(self, index):
        """
        查看流水明细
        """
        id = self.model.item(index.row(), 7).text() # 流水id
        account = self.model.item(index.row(), 1).text() # 一级账户
        subaccount = self.model.item(index.row(), 2).text() # 二级账户
        classification = self.model.item(index.row(), 3).text() # 一级分类
        subclassification = self.model.item(index.row(), 4).text() # 二级分类
        money = float(self.model.item(index.row(), 5).text()) # 金额
        beizhu = self.model.item(index.row(), 6).text() # 备注
        dateTime = self.model.item(index.row(), 0).text() # 流水日期时间
        detailD = DialogFlowDetailFunction()
        detailD.setData(id, account, subaccount, classification, subclassification, money, beizhu, dateTime)
        detailD.successSignal.connect(self.reflushTable)
        detailD.exec()

    @pyqtSlot()
    def on_pushButton_up_clicked(self):
        """
        上一页
        """
        self.currentPage -= 1
        if self.currentPage >= 1:
            self.label_pages.setText(f"第{self.currentPage}/{self.pages}页")
            self.pushButton_down.setEnabled(True)
            self.showTableContent(self.dateStart, self.dateEnd, (self.currentPage-1)*30, 30)
        else:
            self.currentPage = 1

    @pyqtSlot()
    def on_pushButton_down_clicked(self):
        """
        下一页
        """
        self.currentPage += 1
        if self.currentPage <= self.pages:
            self.pushButton_up.setEnabled(True)  # 当前的页数在第1页~最后一页之间，上一页启用
            self.label_pages.setText(f"第{self.currentPage}/{self.pages}页")
            self.showTableContent(self.dateStart, self.dateEnd, (self.currentPage-1)*30, 30)
        else:
            self.currentPage = self.pages

    @pyqtSlot()
    def on_toolButton_go_clicked(self):
        """
        跳转
        """
        goPage = self.spinBox_page.value()  # 跳转页
        if goPage > self.pages:  # 跳转页大于总的页数
            return
        else:
            self.currentPage = goPage
            self.label_pages.setText(f"第{self.currentPage}/{self.pages}页")
            if goPage == 1 and goPage < self.pages: # 跳转到第1页
                self.pushButton_up.setEnabled(False)
                self.pushButton_down.setEnabled(True)
            elif goPage != 1 and goPage < self.pages: # 跳转到第1页~最后一页之间
                self.pushButton_up.setEnabled(True)
                self.pushButton_down.setEnabled(True)
            elif goPage == self.pages: # 跳转到最后一页
                self.pushButton_up.setEnabled(True)
                self.pushButton_down.setEnabled(False)
            self.showTableContent(self.dateStart, self.dateEnd, (self.currentPage-1)*30, 30)