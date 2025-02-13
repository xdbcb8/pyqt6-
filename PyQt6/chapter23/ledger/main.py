#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/02/06 13:02:16
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow
from Ui_main import Ui_MainWindow
from DialogPwdSettingFunction import Dialog_pwd_settingFunction
from DialogAccountSettingFunction import DialogAccountSettingFunction
from DialogChargeClassificationSettingFunction import DialogChargeClassificationSettingFunction
from DialogChargeToAccountFunction import DialogCharge2AccountFunction
from DialogFlowFunction import Form_FlowFunction
from OverView import overViewWidget
from DialogReport import Form_report

# 主界面

class MainWindowFunction(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.reflush() # 执行财务概况菜单

    def reflush(self):
        """
        财务概况信息刷新一下
        """
        self.action_overview.triggered.emit()

    @pyqtSlot()
    def on_action_overview_triggered(self):
        """
        财务概况信息展示
        """
        ov = overViewWidget(self)
        self.setCentralWidget(ov)

    @pyqtSlot()
    def on_action_charge_triggered(self):
        """
        记账
        """
        chargeD = DialogCharge2AccountFunction(self)
        chargeD.dosignal.connect(self.reflush)
        chargeD.exec()

    @pyqtSlot()
    def on_action_flow_triggered(self):
        """
        收支流水展示
        """
        Flow = Form_FlowFunction(self)
        self.setCentralWidget(Flow)

    @pyqtSlot()
    def on_action_report_triggered(self):
        """
        报表
        """
        report = Form_report(self)
        self.setCentralWidget(report)

    @pyqtSlot()
    def on_action_classification_setting_out_triggered(self):
        """
        支出分类设置
        """
        claD = DialogChargeClassificationSettingFunction("out", self)
        claD.exec()

    @pyqtSlot()
    def on_action_classification_setting_in_triggered(self):
        """
        收入分类设置
        """
        claD = DialogChargeClassificationSettingFunction("in", self)
        claD.exec()

    @pyqtSlot()
    def on_action_account_setting_triggered(self):
        """
        账户设置
        """
        accountD = DialogAccountSettingFunction()
        accountD.exec()

    @pyqtSlot()
    def on_action_pwd_setting_triggered(self):
        """
        密码设置
        """
        pwdD = Dialog_pwd_settingFunction(self)
        pwdD.exec()