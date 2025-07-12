#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File     :   db.py
@Time     :   2025/06/22 09:37:08
@Author   :   yangff
@Version  :   1.0
@微信公众号 : 学点编程吧
'''

import sqlite3

class StoryDB:
    '''
    数据库类，用于管理好感度和历程数据
    '''
    
    def __init__(self):
        self.conn = sqlite3.connect('love.db')
        self.cursor = self.conn.cursor()

    def update_favorability(self, name, new_favorability):
        """
        更新指定名称的好感度
        :name: 女主姓名
        :new_favorability: 新的好感度数值
        """
        try:
            self.cursor.execute('''
                INSERT INTO favorability (name, favorability) VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET favorability = favorability + ?
            ''', (name, new_favorability, new_favorability))
            self.conn.commit()
        except Exception as e:
            print(f"更新失败: {e}")

    def query_favorability(self, name):
        """
        查询指定名称的好感度
        :name: 女主姓名
        :return: 好感度数值，好感度小于0的话，直接返回0，不返回负数。
        """
        try:
            self.cursor.execute('''
                SELECT favorability FROM favorability WHERE name = ?
            ''', (name,))
            result = self.cursor.fetchone()
            favorability = result[0]
            return max(0, min(100, favorability))
        except Exception as e:
            print(f"查询失败: {e}")
            return 0

    def clear_favorability(self):
        """
        清空所有好感度数据
        """
        try:
            self.cursor.execute('UPDATE favorability SET favorability = 0')
            self.conn.commit()
        except Exception as e:
            print(f"清空失败: {e}")

    def clear_history(self):
        """
        清空所有历程数据
        """
        try:
            self.cursor.execute('UPDATE story SET datetime = NULL')
            self.cursor.execute('DELETE FROM ignoreT')
            self.conn.commit()
        except Exception as e:
            print(f"清空失败: {e}")

    def update_datetime(self, movie, new_datetime):
        '''
        更新datetime
        :movie: 视频名称
        :new_datetime: 新的时间
        '''
        try:
            self.cursor.execute('''
                UPDATE story
                SET datetime =?
                WHERE movie =?
            ''', (new_datetime, movie))
            self.conn.commit()
        except Exception as e:
            print(f"更新失败: {e}")


    def query_non_empty_datetime(self):
        '''
        查询datetime不为空的数据
        :return: 包含所有数据的列表
        '''
        try:
            self.cursor.execute('''
                SELECT movie, description, datetime, image FROM story
                WHERE datetime IS NOT NULL
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            print(f"查询失败: {e}")
            return []

    def query_latest_datetime(self):
        '''
        查询最新时间的数据
        :return: 包含所有数据的列表
        '''
        try:
            self.cursor.execute('''
                SELECT movie FROM story ORDER BY datetime DESC LIMIT 1
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            print(f"查询失败: {e}")
            return []
    
    def query_skipday(self):
        '''
        查询跳过的天数
        :return: 跳过的天数
        '''
        try:
            self.cursor.execute('''
                SELECT skipday FROM ignoreT
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            print(f"查询失败: {e}")
            return []
    
    def insertSkipday(self, day):
        """
        插入跳过的天数
        """
        # 先检查 skipday 中是否已有该数据
        try:
            self.cursor.execute('SELECT 1 FROM ignoreT WHERE skipday = ?', (day,))
            if not self.cursor.fetchone():
                self.cursor.execute('''
                    INSERT INTO ignoreT (skipday) VALUES(?) 
                ''', (day,))
                self.conn.commit()
        except Exception as e:
            print(f"插入失败: {e}")
        
    def close(self):
        '''
        关闭数据库连接
        '''
        self.conn.close()

