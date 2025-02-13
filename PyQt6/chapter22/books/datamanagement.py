#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   datamanagement.py
@Time    :   2023/08/10 21:50:38
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第12章第3节QTableWidget--数据操作

import pickle
import codecs
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

class CountryManagement:
    """
    国家操作类
    简便操作，只有载入和保存两个方法，增删改在界面处完成后，统一保存即可
    """
    countryFileName = current_dir + "\\res\\country.dat"
    
    def save_country_db(self, countryInfo):
        """
        保存所有国家信息
        """
        with codecs.open(self.countryFileName, "wb") as f:
            pickle.dump(countryInfo, f)
       
    def loadCountry(self):
        """
        载入国家数据
        """
        if not(os.path.exists(self.countryFileName) and os.path.isfile(self.countryFileName)):
            with codecs.open(self.countryFileName, "wb") as f:
                countryList = []
                pickle.dump(countryList, f)
            #要是没有country.dat我们就建一个

        with codecs.open(self.countryFileName, "rb") as f:
            countryList = pickle.load(f)
        return countryList
    

class ClassificationManagement:
    """
    图书分类操作类
    """
    classificationInfoFileName = current_dir + "\\res\\classification.dat"

    def save_classification_db(self, classificationInfo):
        """
        保存图书分类信息
        """
        with codecs.open(self.classificationInfoFileName, "wb") as f:
            pickle.dump(classificationInfo, f)
       
    def loadClassification(self):
        """
        载入图书分类数据
        """
        if not(os.path.exists(self.classificationInfoFileName) and os.path.isfile(self.classificationInfoFileName)):
            with codecs.open(self.classificationInfoFileName, "wb") as f:
                classificationList = []
                pickle.dump(classificationList, f)
            #要是没有classification.dat我们就建一个
        with codecs.open(self.classificationInfoFileName, "rb") as f:
            classificationList = pickle.load(f)
        return classificationList

class BookManagement:
    """
    图书操作类
    """
    books = [] # 暂存载入的图书信息的列表

    bookFileName = current_dir + "\\res\\book.dat"

    def insert_book_db(self, bookinfo):
        """
        新增一条图书记录
        """
        self.books = self.loadBook()
        for book in self.books:
            if book["isbn"] == bookinfo["isbn"]:
                return -1
        else:
            self.books.append(bookinfo)
            with codecs.open(self.bookFileName, "wb") as f:
                pickle.dump(self.books, f)
            return 1

    def save_book_db(self, bookinfo):
        """
        保存所有图书档案
        """
        with codecs.open(self.bookFileName, "wb") as f:
            pickle.dump(bookinfo, f)

    def query_book_db(self, isbn="", author="", bookname=""):
        """
        查找某本书
        """
        self.books = self.loadBook()
        if isbn:
            # 按照isbn查找
            for i, book in enumerate(self.books):
                if book["isbn"] == isbn:
                    return i
            else:
                return -1
        if author:
            # 按照作者查找
            for i, book in enumerate(self.books):
                if book["author"] == author:
                    return i
            else:
                return -1
        if bookname:
            # 按照书名查找
            for i, book in enumerate(self.books):
                if book["subtitle"] == bookname:
                    return i
            else:
                return -1            

    def loadBook(self):
        """
        载入图书数据
        """

        if not(os.path.exists(self.bookFileName) and os.path.isfile(self.bookFileName)):
            with codecs.open(self.bookFileName, "wb") as f:
                pickle.dump(self.books, f)
            #要是没有book.dat我们就建一个

        with codecs.open(self.bookFileName, "rb") as f:
            books = pickle.load(f)
        return books