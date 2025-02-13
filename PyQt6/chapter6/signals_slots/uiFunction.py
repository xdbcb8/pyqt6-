# -*- coding: utf-8 -*-

"""
Module implementing Password.
"""

# 用多继承方式实现界面与功能的分离

import sys
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget, QApplication

from Ui_ui import Ui_Form


class Password(QWidget, Ui_Form):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setupUi(self) # 载入UI设计
        self.num = ""  # 记录当前的数字组合

    @pyqtSlot()
    def on_pushButton9_clicked(self):
        """
        单击数字9
        """
        self.num += "9"
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButton4_clicked(self):
        """
        单击数字4
        """
        self.num += "4"
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButton5_clicked(self):
        """
        单击数字5
        """
        self.num += "5"
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButton8_clicked(self):
        """
        单击数字8
        """
        self.num += "8"
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButton7_clicked(self):
        """
        单击数字7
        """
        self.num += "7"
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButton6_clicked(self):
        """
        单击数字6
        """
        self.num += "6"
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButton1_clicked(self):
        """
        单击数字1
        """
        self.num += "1"
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButton2_clicked(self):
        """
        单击数字2
        """
        self.num += "2"
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButton3_clicked(self):
        """
        单击数字3
        """
        self.num += "3"
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButtonClear_clicked(self):
        """
        单击清除按钮
        """
        self.num = ""
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButton0_clicked(self):
        """
        单击数字0
        """
        self.num += "0"
        self.label.setText(self.num)

    @pyqtSlot()
    def on_pushButtonback_clicked(self):
        """
        单击后退按钮
        """
        self.num = self.num[0:-1]
        self.label.setText(self.num)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pwd = Password()
    pwd.show()
    sys.exit(app.exec())