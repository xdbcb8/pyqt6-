#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   datetimeExample.py
@Time    :   2023/07/09 19:44:46
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# QDateTime举例：日期和时间比较

import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QDateTime, Qt, QTimeZone, QByteArray

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        beijing_time = QDateTime.currentDateTime()   # 获取当前本地时间
        newyork_time = beijing_time.toTimeZone(QTimeZone(QByteArray(b'America/New_York')))    # 本地时间转换为纽约时区的时间
        beijing_time_str = beijing_time.toString(Qt.DateFormat.ISODate)   # 获取北京时间的字符串表示
        newyork_time_str = newyork_time.toString(Qt.DateFormat.ISODate)   # 获取纽约时间的字符串表示
        utc_time_str = beijing_time.toUTC().toString(Qt.DateFormat.ISODate)   # 获取UTC时间的字符串表示
        print("北京时间：", beijing_time_str)
        print("纽约时间：", newyork_time_str)
        print("UTC 时间：", utc_time_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())