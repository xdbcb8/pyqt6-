# Form implementation generated from reading ui file 'D:\onedrive\document\PythonDocument\PyQt6ToImprovement\ArticleMaterial\PyQt6\chapter23\ledger\DialogChargeToAccount.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_charge2account(object):
    def setupUi(self, Dialog_charge2account):
        Dialog_charge2account.setObjectName("Dialog_charge2account")
        Dialog_charge2account.resize(514, 276)
        Dialog_charge2account.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_charge2account)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget_charge = QtWidgets.QTabWidget(parent=Dialog_charge2account)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tabWidget_charge.setFont(font)
        self.tabWidget_charge.setObjectName("tabWidget_charge")
        self.tab_zhichu = QtWidgets.QWidget()
        self.tab_zhichu.setObjectName("tab_zhichu")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_zhichu)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_expend_unit = QtWidgets.QLabel(parent=self.tab_zhichu)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_expend_unit.setFont(font)
        self.label_expend_unit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_expend_unit.setObjectName("label_expend_unit")
        self.gridLayout.addWidget(self.label_expend_unit, 0, 2, 1, 1)
        self.toolButton_classificaiton_expend = QtWidgets.QToolButton(parent=self.tab_zhichu)
        self.toolButton_classificaiton_expend.setObjectName("toolButton_classificaiton_expend")
        self.gridLayout.addWidget(self.toolButton_classificaiton_expend, 1, 2, 1, 1)
        self.label_account_expend = QtWidgets.QLabel(parent=self.tab_zhichu)
        self.label_account_expend.setObjectName("label_account_expend")
        self.gridLayout.addWidget(self.label_account_expend, 2, 0, 1, 1)
        self.label_expend = QtWidgets.QLabel(parent=self.tab_zhichu)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_expend.setFont(font)
        self.label_expend.setObjectName("label_expend")
        self.gridLayout.addWidget(self.label_expend, 0, 0, 1, 1)
        self.label_classification_expend = QtWidgets.QLabel(parent=self.tab_zhichu)
        self.label_classification_expend.setObjectName("label_classification_expend")
        self.gridLayout.addWidget(self.label_classification_expend, 1, 0, 1, 1)
        self.toolButton_account_expend = QtWidgets.QToolButton(parent=self.tab_zhichu)
        self.toolButton_account_expend.setObjectName("toolButton_account_expend")
        self.gridLayout.addWidget(self.toolButton_account_expend, 2, 2, 1, 1)
        self.lineEdit_remark_expend = QtWidgets.QLineEdit(parent=self.tab_zhichu)
        self.lineEdit_remark_expend.setClearButtonEnabled(True)
        self.lineEdit_remark_expend.setObjectName("lineEdit_remark_expend")
        self.gridLayout.addWidget(self.lineEdit_remark_expend, 4, 1, 1, 2)
        self.doubleSpinBox_expend = QtWidgets.QDoubleSpinBox(parent=self.tab_zhichu)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox_expend.setFont(font)
        self.doubleSpinBox_expend.setStyleSheet("color: rgb(0, 170, 0);")
        self.doubleSpinBox_expend.setMaximum(99999999.99)
        self.doubleSpinBox_expend.setObjectName("doubleSpinBox_expend")
        self.gridLayout.addWidget(self.doubleSpinBox_expend, 0, 1, 1, 1)
        self.lineEdit_account_expend = QtWidgets.QLineEdit(parent=self.tab_zhichu)
        self.lineEdit_account_expend.setReadOnly(True)
        self.lineEdit_account_expend.setObjectName("lineEdit_account_expend")
        self.gridLayout.addWidget(self.lineEdit_account_expend, 2, 1, 1, 1)
        self.label_remark_expend = QtWidgets.QLabel(parent=self.tab_zhichu)
        self.label_remark_expend.setObjectName("label_remark_expend")
        self.gridLayout.addWidget(self.label_remark_expend, 4, 0, 1, 1)
        self.dateTimeEdit_expend = QtWidgets.QDateTimeEdit(parent=self.tab_zhichu)
        self.dateTimeEdit_expend.setCalendarPopup(True)
        self.dateTimeEdit_expend.setObjectName("dateTimeEdit_expend")
        self.gridLayout.addWidget(self.dateTimeEdit_expend, 3, 1, 1, 2)
        self.label_dateTime_expend = QtWidgets.QLabel(parent=self.tab_zhichu)
        self.label_dateTime_expend.setObjectName("label_dateTime_expend")
        self.gridLayout.addWidget(self.label_dateTime_expend, 3, 0, 1, 1)
        self.lineEdit_classificaiton_expend = QtWidgets.QLineEdit(parent=self.tab_zhichu)
        self.lineEdit_classificaiton_expend.setReadOnly(True)
        self.lineEdit_classificaiton_expend.setObjectName("lineEdit_classificaiton_expend")
        self.gridLayout.addWidget(self.lineEdit_classificaiton_expend, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.tabWidget_charge.addTab(self.tab_zhichu, "")
        self.tab_shouru = QtWidgets.QWidget()
        self.tab_shouru.setObjectName("tab_shouru")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_shouru)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_income_unit = QtWidgets.QLabel(parent=self.tab_shouru)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_income_unit.setFont(font)
        self.label_income_unit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_income_unit.setObjectName("label_income_unit")
        self.gridLayout_4.addWidget(self.label_income_unit, 0, 2, 1, 1)
        self.toolButton_classificaiton_income = QtWidgets.QToolButton(parent=self.tab_shouru)
        self.toolButton_classificaiton_income.setObjectName("toolButton_classificaiton_income")
        self.gridLayout_4.addWidget(self.toolButton_classificaiton_income, 1, 2, 1, 1)
        self.label_account_income = QtWidgets.QLabel(parent=self.tab_shouru)
        self.label_account_income.setObjectName("label_account_income")
        self.gridLayout_4.addWidget(self.label_account_income, 2, 0, 1, 1)
        self.label_income = QtWidgets.QLabel(parent=self.tab_shouru)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_income.setFont(font)
        self.label_income.setObjectName("label_income")
        self.gridLayout_4.addWidget(self.label_income, 0, 0, 1, 1)
        self.label_classification_income = QtWidgets.QLabel(parent=self.tab_shouru)
        self.label_classification_income.setObjectName("label_classification_income")
        self.gridLayout_4.addWidget(self.label_classification_income, 1, 0, 1, 1)
        self.toolButton_account_income = QtWidgets.QToolButton(parent=self.tab_shouru)
        self.toolButton_account_income.setObjectName("toolButton_account_income")
        self.gridLayout_4.addWidget(self.toolButton_account_income, 2, 2, 1, 1)
        self.lineEdit_remark_income = QtWidgets.QLineEdit(parent=self.tab_shouru)
        self.lineEdit_remark_income.setClearButtonEnabled(True)
        self.lineEdit_remark_income.setObjectName("lineEdit_remark_income")
        self.gridLayout_4.addWidget(self.lineEdit_remark_income, 4, 1, 1, 2)
        self.doubleSpinBox_income = QtWidgets.QDoubleSpinBox(parent=self.tab_shouru)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox_income.setFont(font)
        self.doubleSpinBox_income.setStyleSheet("color: rgb(255, 0, 0);")
        self.doubleSpinBox_income.setMaximum(99999999.99)
        self.doubleSpinBox_income.setObjectName("doubleSpinBox_income")
        self.gridLayout_4.addWidget(self.doubleSpinBox_income, 0, 1, 1, 1)
        self.lineEdit_account_income = QtWidgets.QLineEdit(parent=self.tab_shouru)
        self.lineEdit_account_income.setReadOnly(True)
        self.lineEdit_account_income.setObjectName("lineEdit_account_income")
        self.gridLayout_4.addWidget(self.lineEdit_account_income, 2, 1, 1, 1)
        self.label_remark_income = QtWidgets.QLabel(parent=self.tab_shouru)
        self.label_remark_income.setObjectName("label_remark_income")
        self.gridLayout_4.addWidget(self.label_remark_income, 4, 0, 1, 1)
        self.dateTimeEdit_income = QtWidgets.QDateTimeEdit(parent=self.tab_shouru)
        self.dateTimeEdit_income.setCalendarPopup(True)
        self.dateTimeEdit_income.setObjectName("dateTimeEdit_income")
        self.gridLayout_4.addWidget(self.dateTimeEdit_income, 3, 1, 1, 2)
        self.label_dateTime_income = QtWidgets.QLabel(parent=self.tab_shouru)
        self.label_dateTime_income.setObjectName("label_dateTime_income")
        self.gridLayout_4.addWidget(self.label_dateTime_income, 3, 0, 1, 1)
        self.lineEdit_classificaiton_income = QtWidgets.QLineEdit(parent=self.tab_shouru)
        self.lineEdit_classificaiton_income.setReadOnly(True)
        self.lineEdit_classificaiton_income.setObjectName("lineEdit_classificaiton_income")
        self.gridLayout_4.addWidget(self.lineEdit_classificaiton_income, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_4)
        self.tabWidget_charge.addTab(self.tab_shouru, "")
        self.tab_zz = QtWidgets.QWidget()
        self.tab_zz.setObjectName("tab_zz")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_zz)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_account_transfer_out = QtWidgets.QLineEdit(parent=self.tab_zz)
        self.lineEdit_account_transfer_out.setReadOnly(True)
        self.lineEdit_account_transfer_out.setObjectName("lineEdit_account_transfer_out")
        self.gridLayout_3.addWidget(self.lineEdit_account_transfer_out, 1, 1, 1, 1)
        self.toolButton_account_transfer_in = QtWidgets.QToolButton(parent=self.tab_zz)
        self.toolButton_account_transfer_in.setObjectName("toolButton_account_transfer_in")
        self.gridLayout_3.addWidget(self.toolButton_account_transfer_in, 2, 2, 1, 1)
        self.label_account_transfer_in = QtWidgets.QLabel(parent=self.tab_zz)
        self.label_account_transfer_in.setObjectName("label_account_transfer_in")
        self.gridLayout_3.addWidget(self.label_account_transfer_in, 2, 0, 1, 1)
        self.label_transfer = QtWidgets.QLabel(parent=self.tab_zz)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_transfer.setFont(font)
        self.label_transfer.setObjectName("label_transfer")
        self.gridLayout_3.addWidget(self.label_transfer, 0, 0, 1, 1)
        self.lineEdit_account_transfer_in = QtWidgets.QLineEdit(parent=self.tab_zz)
        self.lineEdit_account_transfer_in.setReadOnly(True)
        self.lineEdit_account_transfer_in.setObjectName("lineEdit_account_transfer_in")
        self.gridLayout_3.addWidget(self.lineEdit_account_transfer_in, 2, 1, 1, 1)
        self.toolButton_account_transfer_out = QtWidgets.QToolButton(parent=self.tab_zz)
        self.toolButton_account_transfer_out.setObjectName("toolButton_account_transfer_out")
        self.gridLayout_3.addWidget(self.toolButton_account_transfer_out, 1, 2, 1, 1)
        self.label_remark_transfer = QtWidgets.QLabel(parent=self.tab_zz)
        self.label_remark_transfer.setObjectName("label_remark_transfer")
        self.gridLayout_3.addWidget(self.label_remark_transfer, 4, 0, 1, 1)
        self.label_dateTime_transfer = QtWidgets.QLabel(parent=self.tab_zz)
        self.label_dateTime_transfer.setObjectName("label_dateTime_transfer")
        self.gridLayout_3.addWidget(self.label_dateTime_transfer, 3, 0, 1, 1)
        self.label_account_transfer_out = QtWidgets.QLabel(parent=self.tab_zz)
        self.label_account_transfer_out.setObjectName("label_account_transfer_out")
        self.gridLayout_3.addWidget(self.label_account_transfer_out, 1, 0, 1, 1)
        self.toolButton_transfer = QtWidgets.QToolButton(parent=self.tab_zz)
        self.toolButton_transfer.setObjectName("toolButton_transfer")
        self.gridLayout_3.addWidget(self.toolButton_transfer, 1, 3, 2, 1)
        self.label_transfer_unit = QtWidgets.QLabel(parent=self.tab_zz)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_transfer_unit.setFont(font)
        self.label_transfer_unit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_transfer_unit.setObjectName("label_transfer_unit")
        self.gridLayout_3.addWidget(self.label_transfer_unit, 0, 3, 1, 1)
        self.dateTimeEdit_transfer = QtWidgets.QDateTimeEdit(parent=self.tab_zz)
        self.dateTimeEdit_transfer.setCalendarPopup(True)
        self.dateTimeEdit_transfer.setObjectName("dateTimeEdit_transfer")
        self.gridLayout_3.addWidget(self.dateTimeEdit_transfer, 3, 1, 1, 3)
        self.lineEdit_remark_transfer = QtWidgets.QLineEdit(parent=self.tab_zz)
        self.lineEdit_remark_transfer.setClearButtonEnabled(True)
        self.lineEdit_remark_transfer.setObjectName("lineEdit_remark_transfer")
        self.gridLayout_3.addWidget(self.lineEdit_remark_transfer, 4, 1, 1, 3)
        self.doubleSpinBox_transfer = QtWidgets.QDoubleSpinBox(parent=self.tab_zz)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox_transfer.setFont(font)
        self.doubleSpinBox_transfer.setMaximum(99999999.99)
        self.doubleSpinBox_transfer.setObjectName("doubleSpinBox_transfer")
        self.gridLayout_3.addWidget(self.doubleSpinBox_transfer, 0, 1, 1, 2)
        self.verticalLayout_5.addLayout(self.gridLayout_3)
        self.tabWidget_charge.addTab(self.tab_zz, "")
        self.tab_ye = QtWidgets.QWidget()
        self.tab_ye.setObjectName("tab_ye")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_ye)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.toolButton_account_balance = QtWidgets.QToolButton(parent=self.tab_ye)
        self.toolButton_account_balance.setObjectName("toolButton_account_balance")
        self.gridLayout_2.addWidget(self.toolButton_account_balance, 1, 2, 1, 1)
        self.label_balance_unit = QtWidgets.QLabel(parent=self.tab_ye)
        self.label_balance_unit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_balance_unit.setObjectName("label_balance_unit")
        self.gridLayout_2.addWidget(self.label_balance_unit, 0, 2, 1, 1)
        self.doubleSpinBox_balance = QtWidgets.QDoubleSpinBox(parent=self.tab_ye)
        self.doubleSpinBox_balance.setMinimum(-99999999.0)
        self.doubleSpinBox_balance.setMaximum(99999999.99)
        self.doubleSpinBox_balance.setObjectName("doubleSpinBox_balance")
        self.gridLayout_2.addWidget(self.doubleSpinBox_balance, 0, 1, 1, 1)
        self.label_account_balance = QtWidgets.QLabel(parent=self.tab_ye)
        self.label_account_balance.setObjectName("label_account_balance")
        self.gridLayout_2.addWidget(self.label_account_balance, 1, 0, 1, 1)
        self.label_balance = QtWidgets.QLabel(parent=self.tab_ye)
        self.label_balance.setObjectName("label_balance")
        self.gridLayout_2.addWidget(self.label_balance, 0, 0, 1, 1)
        self.label_remark_balance = QtWidgets.QLabel(parent=self.tab_ye)
        self.label_remark_balance.setObjectName("label_remark_balance")
        self.gridLayout_2.addWidget(self.label_remark_balance, 3, 0, 1, 1)
        self.lineEdit_account_balance = QtWidgets.QLineEdit(parent=self.tab_ye)
        self.lineEdit_account_balance.setReadOnly(True)
        self.lineEdit_account_balance.setObjectName("lineEdit_account_balance")
        self.gridLayout_2.addWidget(self.lineEdit_account_balance, 1, 1, 1, 1)
        self.lineEdit_remark_balance = QtWidgets.QLineEdit(parent=self.tab_ye)
        self.lineEdit_remark_balance.setClearButtonEnabled(True)
        self.lineEdit_remark_balance.setObjectName("lineEdit_remark_balance")
        self.gridLayout_2.addWidget(self.lineEdit_remark_balance, 3, 1, 1, 2)
        self.label_dateTime_balance = QtWidgets.QLabel(parent=self.tab_ye)
        self.label_dateTime_balance.setObjectName("label_dateTime_balance")
        self.gridLayout_2.addWidget(self.label_dateTime_balance, 2, 0, 1, 1)
        self.dateTimeEdit_balance = QtWidgets.QDateTimeEdit(parent=self.tab_ye)
        self.dateTimeEdit_balance.setObjectName("dateTimeEdit_balance")
        self.gridLayout_2.addWidget(self.dateTimeEdit_balance, 2, 1, 1, 2)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.tabWidget_charge.addTab(self.tab_ye, "")
        self.verticalLayout.addWidget(self.tabWidget_charge)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_ok = QtWidgets.QPushButton(parent=Dialog_charge2account)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_ok.sizePolicy().hasHeightForWidth())
        self.pushButton_ok.setSizePolicy(sizePolicy)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtWidgets.QPushButton(parent=Dialog_charge2account)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_cancel.setSizePolicy(sizePolicy)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog_charge2account)
        self.tabWidget_charge.setCurrentIndex(0)
        self.pushButton_ok.clicked.connect(Dialog_charge2account.accept) # type: ignore
        self.pushButton_cancel.clicked.connect(Dialog_charge2account.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog_charge2account)

    def retranslateUi(self, Dialog_charge2account):
        _translate = QtCore.QCoreApplication.translate
        Dialog_charge2account.setWindowTitle(_translate("Dialog_charge2account", "收支记录对话框"))
        self.label_expend_unit.setText(_translate("Dialog_charge2account", "元"))
        self.toolButton_classificaiton_expend.setText(_translate("Dialog_charge2account", "..."))
        self.label_account_expend.setText(_translate("Dialog_charge2account", "账户："))
        self.label_expend.setText(_translate("Dialog_charge2account", "金额："))
        self.label_classification_expend.setText(_translate("Dialog_charge2account", "分类："))
        self.toolButton_account_expend.setText(_translate("Dialog_charge2account", "..."))
        self.label_remark_expend.setText(_translate("Dialog_charge2account", "备注："))
        self.label_dateTime_expend.setText(_translate("Dialog_charge2account", "时间："))
        self.tabWidget_charge.setTabText(self.tabWidget_charge.indexOf(self.tab_zhichu), _translate("Dialog_charge2account", "支出"))
        self.label_income_unit.setText(_translate("Dialog_charge2account", "元"))
        self.toolButton_classificaiton_income.setText(_translate("Dialog_charge2account", "..."))
        self.label_account_income.setText(_translate("Dialog_charge2account", "账户："))
        self.label_income.setText(_translate("Dialog_charge2account", "金额："))
        self.label_classification_income.setText(_translate("Dialog_charge2account", "分类："))
        self.toolButton_account_income.setText(_translate("Dialog_charge2account", "..."))
        self.label_remark_income.setText(_translate("Dialog_charge2account", "备注："))
        self.label_dateTime_income.setText(_translate("Dialog_charge2account", "时间："))
        self.tabWidget_charge.setTabText(self.tabWidget_charge.indexOf(self.tab_shouru), _translate("Dialog_charge2account", "收入"))
        self.toolButton_account_transfer_in.setText(_translate("Dialog_charge2account", "..."))
        self.label_account_transfer_in.setText(_translate("Dialog_charge2account", "转入账户："))
        self.label_transfer.setText(_translate("Dialog_charge2account", "金      额："))
        self.toolButton_account_transfer_out.setText(_translate("Dialog_charge2account", "..."))
        self.label_remark_transfer.setText(_translate("Dialog_charge2account", "备      注："))
        self.label_dateTime_transfer.setText(_translate("Dialog_charge2account", "时      间："))
        self.label_account_transfer_out.setText(_translate("Dialog_charge2account", "转出账户："))
        self.toolButton_transfer.setToolTip(_translate("Dialog_charge2account", "账户相互调换"))
        self.toolButton_transfer.setText(_translate("Dialog_charge2account", "换"))
        self.label_transfer_unit.setText(_translate("Dialog_charge2account", "元"))
        self.tabWidget_charge.setTabText(self.tabWidget_charge.indexOf(self.tab_zz), _translate("Dialog_charge2account", "转账"))
        self.toolButton_account_balance.setText(_translate("Dialog_charge2account", "..."))
        self.label_balance_unit.setText(_translate("Dialog_charge2account", "元"))
        self.label_account_balance.setText(_translate("Dialog_charge2account", "账户："))
        self.label_balance.setText(_translate("Dialog_charge2account", "余额："))
        self.label_remark_balance.setText(_translate("Dialog_charge2account", "备注："))
        self.label_dateTime_balance.setText(_translate("Dialog_charge2account", "时间："))
        self.tabWidget_charge.setTabText(self.tabWidget_charge.indexOf(self.tab_ye), _translate("Dialog_charge2account", "余额"))
        self.pushButton_ok.setText(_translate("Dialog_charge2account", "确定"))
        self.pushButton_cancel.setText(_translate("Dialog_charge2account", "取消"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_charge2account = QtWidgets.QDialog()
    ui = Ui_Dialog_charge2account()
    ui.setupUi(Dialog_charge2account)
    Dialog_charge2account.show()
    sys.exit(app.exec())
