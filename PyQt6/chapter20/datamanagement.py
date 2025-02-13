#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   datamanagement.py
@Time    :   2023/11/15 16:41:41
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

# 第20章--数据操作

from dbmanagement import DbManager

dataBase = DbManager() # 连接数据库初始化

class CountryManagement:
    """
    国籍（地区）操作类
    """

    def insert_country_db(self, country):
        """
        新增国籍（地区）信息
        """
        sql = f"INSERT INTO countries(countryName) VALUES('{country}')"
        issuccess = dataBase.execute(sql)
        if issuccess: # 数据库操作失败返回-1，下同
            return -1

    def del_country_db(self, country):
        """
        删除国籍（地区）信息
        """
        sql = f"DELETE FROM countries WHERE countryName = '{country}'"
        issuccess = dataBase.execute(sql)
        if issuccess:
            return -1

    def modify_country_db(self, old, new):
        """
        修改国籍（地区）信息
        old：原有的国籍（地区）名称
        new：新的国籍（地区）名称
        """
        sql = f"UPDATE countries SET countryName = '{new}' WHERE countryName = '{old}'"
        issuccess = dataBase.execute(sql)
        if issuccess:
            return -1
        
    def loadCountry(self):
        """
        载入国籍（地区）数据
        """
        sql = "SELECT countryName FROM countries"
        countryList = dataBase.query(sql)
        return countryList

class ClassificationManagement:
    """
    图书分类操作类
    """

    def insert_classification_db(self, classification):
        """
        新增图书分类信息
        """
        sql = f"INSERT INTO classification(classificationName) VALUES('{classification}')"
        issuccess = dataBase.execute(sql)
        if issuccess:
            return -1
        
    def del_classification_db(self, classification):
        """
        删除图书分类信息
        """
        sql = f"DELETE FROM classification WHERE classificationName = '{classification}'"
        issuccess = dataBase.execute(sql)
        if issuccess:
            return -1
        
    def modify_classification_db(self, old, new):
        """
        修改图书分类信息
        """
        sql = f"UPDATE classification SET classificationName = '{new}' WHERE classificationName = '{old}'"
        issuccess = dataBase.execute(sql)
        if issuccess:
            return -1

    def loadClassification(self):
        """
        载入图书分类数据
        """
        sql = "SELECT classificationName FROM classification"
        classificationList = dataBase.query(sql)
        return classificationList

class BookManagement:
    """
    图书操作类
    """
    def insert_book_db(self, bookinfo):
        """
        新增一条图书记录
        bookinfo：一本图书的字典信息
        """
        issuccess = dataBase.executeInsertBook(bookinfo)
        if issuccess:
            return -1
        
    def del_book_db(self, isbn):
        """
        删除图书
        isbn：isbn编号
        """
        sql = f"DELETE FROM books WHERE isbn = '{isbn}'"
        issuccess = dataBase.execute(sql)
        if issuccess:
            return -1

    def save_book_db(self, bookinfo):
        """
        保存修改后的图书档案
        bookinfo：一本图书的字典信息
        """
        isbn = bookinfo["isbn"]
        country = bookinfo["country"]
        subtitle = bookinfo["subtitle"]
        author = bookinfo["author"]
        classification = bookinfo["classification"]
        publisher = bookinfo["publisher"]
        pages = bookinfo["pages"]
        pubdate = bookinfo["pubdate"]
        price = bookinfo["price"]
        summary = bookinfo["summary"]
        img = bookinfo["img"]
        sql = f"UPDATE books SET country = '{country}', subtitle = '{subtitle}', author = '{author}', classification = '{classification}', \
            publisher = '{publisher}', pages = {pages}, pubdate = '{pubdate}', price = {price}, summary = '{summary}', img = '{img}' WHERE isbn = '{isbn}'"
        result = dataBase.execute(sql)
        if result:
            return -1

    def query_book_db(self, isbn="", author="", subtitle=""):
        """
        查找某本书
        """
        if isbn:
            # 按照isbn查找
            conditions = f"isbn LIKE '%{isbn}%'"
        if author:
            # 按照作者查找
            conditions = f"author LIKE '%{author}%'"
        if subtitle:
            # 按照书名查找
            conditions = f"subtitle LIKE '%{subtitle}%'"     
        sql = f"SELECT country, isbn, subtitle, author, classification, publisher, pages, pubdate, price, summary, img FROM books WHERE {conditions}"
        booksList = dataBase.queryBook(sql)
        return booksList

    def loadBook(self):
        """
        载入全部图书数据
        """
        sql = "SELECT country, isbn, subtitle, author, classification, publisher, pages, pubdate, price, summary, img FROM books"
        booksList = dataBase.queryBook(sql)
        return booksList