#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   firstWindows.py
@Time    :   2023/04/07 15:17:08
@Author  :   yangff 
@Version :   1.0
@微信公众号:  xdbcb8
'''

import sys
from PyQt6.QtWidgets import QApplication, QWidget

# 简单窗体

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(400, 300)
    w.setWindowTitle('微信公众号：学点编程吧')
    w.show()
    sys.exit(app.exec())