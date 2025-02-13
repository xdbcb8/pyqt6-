#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   run.py
@Time    :   2024/02/09 16:24:29
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''


# 整个简单记账本的入口文件

import sys
from PyQt6.QtWidgets import QApplication
from DialogPwd import Dialog_pwd

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Dialog_pwd()
    login.show()
    sys.exit(app.exec())