#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dbmanagement.py
@Time    :   2023/11/15 16:42:39
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

# 第20章--数据库管理

import sys
import os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtSql import QSqlQuery, QSqlDatabase

current_dir = os.path.dirname(os.path.abspath(__file__))

class DbManager:
    # 构造函数
    def __init__(self):
        self.connectDatabase()

    def connectDatabase(self):
        '''
        连接数据库
        '''
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.dbPath = f"{current_dir}\\db\\book.db" # 数据库的路径
        self.db.setDatabaseName(self.dbPath)
        isSuccess = self.db.open()
        if not isSuccess:
            QMessageBox.critical(None, "严重错误", "数据连接失败，程序无法使用，请按取消键退出", QMessageBox.StandardButton.Cancel)
            print(self.db.lastError().text())
            sys.exit()

    def closeDB(self):
        '''
        关闭数据库
        '''
        self.db.close()

    def execute(self, sql):
        '''
        执行数据库的sql语句
        sql：sql语句
        '''
        query = QSqlQuery()
        result = query.exec(sql)
        if not result:
            return query.lastError().text()
        
    def executeInsertBook(self, bookinfo):
        """
        插入图书
        bookinfo：图书字典信息
        """
        query = QSqlQuery()
        query.prepare("INSERT INTO books (isbn, country, subtitle, author, classification, publisher, pages, pubdate, price, summary, img) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        query.addBindValue(bookinfo["isbn"])
        query.addBindValue(bookinfo["country"])
        query.addBindValue(bookinfo["subtitle"])
        query.addBindValue(bookinfo["author"])
        query.addBindValue(bookinfo["classification"])
        query.addBindValue(bookinfo["publisher"])
        query.addBindValue(bookinfo["pages"])
        query.addBindValue(bookinfo["pubdate"])
        query.addBindValue(bookinfo["price"])
        query.addBindValue(bookinfo["summary"])
        query.addBindValue(bookinfo["img"])
        result = query.exec()
        if not result:
            return query.lastError().text() # 出错了
        
    def query(self, sql):
        '''
        查询非图书所有数据
        sql：sql语句
        '''
        result = []
        query = QSqlQuery(sql)
        while query.next():
            result.append(query.value(0))
        return result
    
    def queryBook(self, sql):
        '''
        查询所有图书数据
        sql：sql语句
        '''
        result = []
        query = QSqlQuery(sql)
        while query.next():
            country = query.value(0)
            isbn = query.value(1)
            subtitle = query.value(2)
            author = query.value(3)
            classificationName = query.value(4)
            publisher = query.value(5)
            pages = query.value(6)
            pubdate = query.value(7)
            price = query.value(8)
            summary = query.value(9)
            img = query.value(10)
            book = {"country" : country, "isbn" : isbn, "subtitle" : subtitle, "author" : author, "classification" : classificationName, 
                    "publisher" : publisher, "pages" : pages, "pubdate" : pubdate, "price" : price, "summary" : summary, "img" : img}
            result.append(book)
        return result