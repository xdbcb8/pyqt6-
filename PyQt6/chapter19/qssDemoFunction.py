#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   qssDemoFunction.py
@Time    :   2023/11/08 19:11:58
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

# 第19章窗体美化

import imgRes_rc
import sys
import os
import codecs
import qdarkstyle
from PyQt6.QtCore import pyqtSlot, Qt, QAbstractTableModel, QSortFilterProxyModel
from PyQt6.QtWidgets import QMainWindow, QHeaderView, QApplication, QLabel, QMenu
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from Ui_qssDemo import Ui_MainWindow

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data  # 存储表格数据

    def rowCount(self, parent=None):
        return len(self._data)  # 返回表格的行数

    def columnCount(self, parent=None):
        return len(self._data[0])  # 返回表格的列数

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:  # 如果角色是显示角色
            return self._data[index.row()][index.column()]  # 返回对应单元格的数据
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:  # 如果角色是显示角色且方向是水平
            if section == 0:
                return "姓名"  # 返回第一列的表头文本
            elif section == 1:
                return "年龄"  # 返回第二列的表头文本
            elif section == 2:
                return "性别"  # 返回第三列的表头文本
            elif section == 3:
                return "身高"  # 返回第四列的表头文本
            elif section == 4:
                return "爱好"  # 返回第五列的表头文本
            elif section == 5:
                return "职业"  # 返回第六列的表头文本
        return None

class FunctionMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("QSS举例")
        self.tableView.verticalHeader().setDefaultSectionSize(22)  # 默认行高22
        self.tableView.setAlternatingRowColors(True)  # 交替行颜色
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # 列宽自动分配

        data = [
            ["王丽", 23, "女", 165, "旅游", "自由职业者"],
            ["李四", 31, "男", 182, "健身", "教师"],
            ["赵刚", 29, "男", 178, "游泳", "医生"],
            ["刘云", 27, "女", 168, "看电影", "设计师"],
            ["陈华", 26, "男", 180, "打篮球", "律师"],
            ["王芳", 33, "女", 172, "唱歌", "企业家"],
            ["张伟", 28, "男", 179, "跑步", "程序员"],
            ["杨柳", 24, "女", 166, "跳舞", "教师"],
            ["吴明", 30, "男", 185, "骑行", "摄影师"],
            ["郑小琴", 28, "女", 170, "画画", "服务员"]
        ]

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(TableModel(data))
        self.tableView.setModel(self.proxy_model)
        self.tableView.setSortingEnabled(True)  # 开启排序功能
        self.tableView.sortByColumn(1, Qt.SortOrder.AscendingOrder)  # 按第2列升序排序

        # 创建一个QSortFilterProxyModel对象，用于对数据进行过滤和排序
        self.proxy_model = QSortFilterProxyModel()
        # 设置代理模型的数据源为TableModel(data)，其中data是一个包含表格数据的列表
        self.proxy_model.setSourceModel(TableModel(data))
        self.tableView.setModel(self.proxy_model)
        self.tableView.setSortingEnabled(True) # 启用表格视图的排序功能
        self.tableView.sortByColumn(1, Qt.SortOrder.AscendingOrder) # 按照第二列（索引为1）进行升序排序

        # 树形结构的数据模拟
        self.treeModel = QStandardItemModel(self)
        self.treeView.setModel(self.treeModel)
        self.treeView.setColumnWidth(0, 50) # 列宽
        self.treeModel.setHorizontalHeaderLabels(["项目"])  # 设置标题标签
        self.root = self.treeModel.invisibleRootItem() # 总的根节点
        item1 = QStandardItem("节点1")
        item2 = QStandardItem("节点2")
        item3 = QStandardItem("节点3")
        item4 = QStandardItem("节点4")
        self.root.appendRows([item1, item2, item3, item4])
        childItem1 = QStandardItem("子节点1")
        childItem2 = QStandardItem("子节点2")
        childItem3 = QStandardItem("子节点3")
        childItem4 = QStandardItem("子节点4")
        item4.appendRows([childItem1, childItem2, childItem3, childItem4])
        child2Item = QStandardItem("子节点5")
        childItem4.appendRow(child2Item)
        self.treeView.expandAll() # 默认是节点展开

        # 状态栏的标签设置
        statusBarLabel = QLabel("Hello, PyQt6!")
        self.statusBar.addWidget(statusBarLabel)

        # 按钮菜单设置
        menu = QMenu(self)
        menu.addAction("菜单项1")
        menu.addSeparator()
        menu.addAction("菜单项2")
        menu.addSeparator()
        menu.addAction("菜单项3")
        self.pushButton_3.setMenu(menu)

    @pyqtSlot()
    def on_action_2_triggered(self):
        """
        不加载样式
        """
        self.setStyleSheet("")

    @pyqtSlot()
    def on_action_3_triggered(self):
        """
        加载自定义样式
        """
        qssPath = f"{current_dir}\\style.qss"
        # qssPath = f"{current_dir}\\QSS-master\\Ubuntu.qss"
        # qssPath = f"{current_dir}\\QSS-master\\MaterialDark.qss"
        # qssPath = f"{current_dir}\\QSS-master\\MacOS.qss"
        with codecs.open(qssPath, "r", "utf-8") as f:
            qssContent = f.read()
            self.setStyleSheet(qssContent)

    @pyqtSlot()
    def on_actionQDarkStyleSheet_2_triggered(self):
        """
        加载QDarkStyleSheet样式
        """
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())

    @pyqtSlot(bool)
    def on_radioButton_clicked(self, checked):
        """
        下拉框可编辑
        """
        if checked:
            self.comboBox.setEditable(True)

    @pyqtSlot(bool)
    def on_radioButton_2_clicked(self, checked):
        """
        下拉框不可编辑
        """
        if checked:
            self.comboBox.setEditable(False)

    @pyqtSlot(int)
    def on_horizontalScrollBar_sliderMoved(self, value):
        """
        水平滚动条
        """
        self.progressBar_4.setValue(value)

    @pyqtSlot(int)
    def on_verticalScrollBar_sliderMoved(self, value):
        """
        垂直滚动条
        """
        self.progressBar_3.setValue(value)

    @pyqtSlot(int)
    def on_horizontalSlider_sliderMoved(self, value):
        """
        水平滑块
        """
        self.progressBar_2.setValue(value)

    @pyqtSlot(int)
    def on_verticalSlider_sliderMoved(self, value):
        """
        垂直滑块
        """
        self.progressBar.setValue(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = FunctionMainWindow()
    example.show()
    sys.exit(app.exec())