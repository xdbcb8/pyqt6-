# Form implementation generated from reading ui file 'D:\onedrive\document\PythonDocument\PyQt6ToImprovement\ArticleMaterial\PyQt6\chapter23\ledger\DialogAccountBankSetting.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(396, 132)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_bank = QtWidgets.QComboBox(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_bank.setFont(font)
        self.comboBox_bank.setObjectName("comboBox_bank")
        self.gridLayout.addWidget(self.comboBox_bank, 0, 1, 1, 3)
        self.label_bankID = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_bankID.sizePolicy().hasHeightForWidth())
        self.label_bankID.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_bankID.setFont(font)
        self.label_bankID.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_bankID.setObjectName("label_bankID")
        self.gridLayout.addWidget(self.label_bankID, 1, 0, 1, 1)
        self.lineEdit_bankID = QtWidgets.QLineEdit(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_bankID.setFont(font)
        self.lineEdit_bankID.setObjectName("lineEdit_bankID")
        self.gridLayout.addWidget(self.lineEdit_bankID, 1, 1, 1, 3)
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
        self.pushButton_bank_cancel = QtWidgets.QPushButton(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_bank_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_bank_cancel.setSizePolicy(sizePolicy)
        self.pushButton_bank_cancel.setObjectName("pushButton_bank_cancel")
        self.gridLayout.addWidget(self.pushButton_bank_cancel, 3, 3, 1, 1)
        self.pushButton_bank_ok = QtWidgets.QPushButton(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_bank_ok.sizePolicy().hasHeightForWidth())
        self.pushButton_bank_ok.setSizePolicy(sizePolicy)
        self.pushButton_bank_ok.setObjectName("pushButton_bank_ok")
        self.gridLayout.addWidget(self.pushButton_bank_ok, 3, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 1, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        self.pushButton_bank_cancel.clicked.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "添加储蓄卡信息"))
        self.label_bankID.setText(_translate("Dialog", "卡号后4位："))
        self.lineEdit_bankID.setInputMask(_translate("Dialog", "0000;-"))
        self.label_bank.setText(_translate("Dialog", "银行名称："))
        self.pushButton_bank_cancel.setText(_translate("Dialog", "取消"))
        self.pushButton_bank_ok.setText(_translate("Dialog", "确定"))
        self.label.setText(_translate("Dialog", "卡号后4位要全部填写"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
