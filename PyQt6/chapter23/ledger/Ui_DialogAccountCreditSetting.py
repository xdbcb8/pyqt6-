# Form implementation generated from reading ui file 'D:\onedrive\document\PythonDocument\PyQt6ToImprovement\ArticleMaterial\PyQt6\chapter23\ledger\DialogAccountCreditSetting.ui'
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
        self.lineEdit_CreditID = QtWidgets.QLineEdit(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_CreditID.setFont(font)
        self.lineEdit_CreditID.setObjectName("lineEdit_CreditID")
        self.gridLayout.addWidget(self.lineEdit_CreditID, 1, 1, 1, 3)
        self.label_CreditID = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_CreditID.sizePolicy().hasHeightForWidth())
        self.label_CreditID.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_CreditID.setFont(font)
        self.label_CreditID.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_CreditID.setObjectName("label_CreditID")
        self.gridLayout.addWidget(self.label_CreditID, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.comboBox_Credit = QtWidgets.QComboBox(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_Credit.setFont(font)
        self.comboBox_Credit.setObjectName("comboBox_Credit")
        self.gridLayout.addWidget(self.comboBox_Credit, 0, 1, 1, 3)
        self.label_Credit = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Credit.sizePolicy().hasHeightForWidth())
        self.label_Credit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_Credit.setFont(font)
        self.label_Credit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Credit.setObjectName("label_Credit")
        self.gridLayout.addWidget(self.label_Credit, 0, 0, 1, 1)
        self.pushButton_credit_cancel = QtWidgets.QPushButton(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_credit_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_credit_cancel.setSizePolicy(sizePolicy)
        self.pushButton_credit_cancel.setObjectName("pushButton_credit_cancel")
        self.gridLayout.addWidget(self.pushButton_credit_cancel, 2, 3, 1, 1)
        self.pushButton_credit_ok = QtWidgets.QPushButton(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_credit_ok.sizePolicy().hasHeightForWidth())
        self.pushButton_credit_ok.setSizePolicy(sizePolicy)
        self.pushButton_credit_ok.setObjectName("pushButton_credit_ok")
        self.gridLayout.addWidget(self.pushButton_credit_ok, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        self.pushButton_credit_cancel.clicked.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "添加信用卡信息"))
        self.lineEdit_CreditID.setInputMask(_translate("Dialog", "0000;-"))
        self.label_CreditID.setText(_translate("Dialog", "卡号后4位："))
        self.label_Credit.setText(_translate("Dialog", "银行名称："))
        self.pushButton_credit_cancel.setText(_translate("Dialog", "取消"))
        self.pushButton_credit_ok.setText(_translate("Dialog", "确定"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
