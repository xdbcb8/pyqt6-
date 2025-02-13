#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dbmanagement.py
@Time    :   2024/01/22 15:07:22
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

import sys
import logging
import os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtSql import QSqlQuery, QSqlDatabase

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

# 加入日志
# 获取logger实例
logger = logging.getLogger("dbError")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s%(levelname)-8s:%(message)s')

# 文件日志
errPath = f"{current_dir}\\dbError.log"
file_handler = logging.FileHandler(errPath, encoding="utf-8")
file_handler.setFormatter(formatter)

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 添加具体的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

class DbManager:
    def __init__(self):
        self.connectDatabase()
        self.shutdownMySQl()

    def connectDatabase(self):
        '''
        连接数据库
        '''
        # 用户名和密码保存在系统环境变量当中
        username = os.environ["MySQLusrname"] # 用户名
        pwd = os.environ["MySQLpwd"] # 密码
        self.db = QSqlDatabase.addDatabase("QODBC")
        self.db.setHostName("127.0.0.1")
        self.db.setPort(3306)
        self.db.setDatabaseName("financeData") # Data Source Name输入栏中的内容：financeData
        self.db.setUserName(username) # 请替换成自己的MySQL用户名
        self.db.setPassword(pwd) # 请替换成自己的MySQL密码
        isSuccess = self.db.open()
        if not isSuccess:
            QMessageBox.critical(None, "严重错误", "数据连接失败，程序无法使用，请按取消键退出", QMessageBox.StandardButton.Cancel)
            logger.error("数据库连接失败！")
            sys.exit()

    def shutdownMySQl(self):
        """
        关闭MySQL安全模式，这个请自行酌情考虑
        """
        sql = "set SQL_SAFE_UPDATES = 0"
        self.execute(sql)

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
            logger.error("数据库执行失败！")
            self.closeDB()
            return "execut_error"

    def query(self, sql):
        '''
        查询所有数据
        sql：sql语句
        '''
        result = []
        query = QSqlQuery(sql)
        record = query.record()
        fieldCount = record.count() # 获取相关表的字段数目
        while query.next():
            fieldResult = []
            for i in range(fieldCount):
                fieldResult.append(query.value(i))
            result.append(fieldResult)
        return result