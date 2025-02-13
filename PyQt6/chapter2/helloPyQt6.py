#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   helloPyQt6.py
@Time    :   2023/12/25 18:30:49
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import PYQT_VERSION_STR

if __name__=='__main__':
    import sys
    app=QApplication(sys.argv)
    print(f"Hello PyQt{PYQT_VERSION_STR}") # 显示PyQt的版本
    sys.exit(app.exec())
