# Form implementation generated from reading ui file 'D:\onedrive\document\PythonDocument\PyQt6ToImprovement\ArticleMaterial\PyQt6\chapter23\ledger\DialogChargeClassificationSetting.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogChargeClassificationSetting(object):
    def setupUi(self, DialogChargeClassificationSetting):
        DialogChargeClassificationSetting.setObjectName("DialogChargeClassificationSetting")
        DialogChargeClassificationSetting.resize(335, 602)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogChargeClassificationSetting)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ChargeClassificationTree = QtWidgets.QTreeView(parent=DialogChargeClassificationSetting)
        self.ChargeClassificationTree.setObjectName("ChargeClassificationTree")
        self.verticalLayout.addWidget(self.ChargeClassificationTree)

        self.retranslateUi(DialogChargeClassificationSetting)
        QtCore.QMetaObject.connectSlotsByName(DialogChargeClassificationSetting)

    def retranslateUi(self, DialogChargeClassificationSetting):
        _translate = QtCore.QCoreApplication.translate
        DialogChargeClassificationSetting.setWindowTitle(_translate("DialogChargeClassificationSetting", "支出/收入分类设置"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogChargeClassificationSetting = QtWidgets.QDialog()
    ui = Ui_DialogChargeClassificationSetting()
    ui.setupUi(DialogChargeClassificationSetting)
    DialogChargeClassificationSetting.show()
    sys.exit(app.exec())
