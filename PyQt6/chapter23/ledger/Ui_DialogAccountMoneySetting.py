# Form implementation generated from reading ui file 'D:\onedrive\document\PythonDocument\PyQt6ToImprovement\ArticleMaterial\PyQt6\chapter23\ledger\DialogAccountMoneySetting.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(396, 129)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_bank = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_bank.sizePolicy().hasHeightForWidth())
        self.label_bank.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_bank.setFont(font)
        self.label_bank.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_bank.setObjectName("label_bank")
        self.gridLayout.addWidget(self.label_bank, 0, 0, 1, 1)
        self.pushButton_Money_cancel = QtWidgets.QPushButton(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Money_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_Money_cancel.setSizePolicy(sizePolicy)
        self.pushButton_Money_cancel.setObjectName("pushButton_Money_cancel")
        self.gridLayout.addWidget(self.pushButton_Money_cancel, 3, 3, 1, 1)
        self.comboBox_Money = QtWidgets.QComboBox(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_Money.setFont(font)
        self.comboBox_Money.setObjectName("comboBox_Money")
        self.comboBox_Money.addItem("")
        self.comboBox_Money.addItem("")
        self.comboBox_Money.addItem("")
        self.comboBox_Money.addItem("")
        self.comboBox_Money.addItem("")
        self.comboBox_Money.addItem("")
        self.gridLayout.addWidget(self.comboBox_Money, 0, 1, 1, 3)
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)
        self.pushButton_Money_ok = QtWidgets.QPushButton(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Money_ok.sizePolicy().hasHeightForWidth())
        self.pushButton_Money_ok.setSizePolicy(sizePolicy)
        self.pushButton_Money_ok.setDefault(True)
        self.pushButton_Money_ok.setObjectName("pushButton_Money_ok")
        self.gridLayout.addWidget(self.pushButton_Money_ok, 3, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_money = QtWidgets.QLineEdit(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_money.setFont(font)
        self.lineEdit_money.setObjectName("lineEdit_money")
        self.gridLayout.addWidget(self.lineEdit_money, 1, 1, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(Dialog)
        self.pushButton_Money_cancel.clicked.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.comboBox_Money, self.lineEdit_money)
        Dialog.setTabOrder(self.lineEdit_money, self.pushButton_Money_ok)
        Dialog.setTabOrder(self.pushButton_Money_ok, self.pushButton_Money_cancel)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "添加储蓄卡信息"))
        self.label_bank.setText(_translate("Dialog", "现金币种："))
        self.pushButton_Money_cancel.setText(_translate("Dialog", "取消"))
        self.comboBox_Money.setItemText(0, _translate("Dialog", "人民币"))
        self.comboBox_Money.setItemText(1, _translate("Dialog", "美元"))
        self.comboBox_Money.setItemText(2, _translate("Dialog", "日元"))
        self.comboBox_Money.setItemText(3, _translate("Dialog", "英镑"))
        self.comboBox_Money.setItemText(4, _translate("Dialog", "欧元"))
        self.comboBox_Money.setItemText(5, _translate("Dialog", "其他币种"))
        self.pushButton_Money_ok.setText(_translate("Dialog", "确定"))
        self.label_2.setText(_translate("Dialog", "账户名称："))
        self.label.setText(_translate("Dialog", "只做演示，账户统计时不考虑汇率因素"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
