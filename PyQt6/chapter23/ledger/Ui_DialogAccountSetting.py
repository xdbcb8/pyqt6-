# Form implementation generated from reading ui file 'D:\onedrive\document\PythonDocument\PyQt6ToImprovement\ArticleMaterial\PyQt6\chapter23\ledger\DialogAccountSetting.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogAccount_Setting(object):
    def setupUi(self, DialogAccount_Setting):
        DialogAccount_Setting.setObjectName("DialogAccount_Setting")
        DialogAccount_Setting.resize(342, 602)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogAccount_Setting)
        self.verticalLayout.setObjectName("verticalLayout")
        self.AccountSettingTree = QtWidgets.QTreeView(parent=DialogAccount_Setting)
        self.AccountSettingTree.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.AccountSettingTree.setObjectName("AccountSettingTree")
        self.verticalLayout.addWidget(self.AccountSettingTree)

        self.retranslateUi(DialogAccount_Setting)
        QtCore.QMetaObject.connectSlotsByName(DialogAccount_Setting)

    def retranslateUi(self, DialogAccount_Setting):
        _translate = QtCore.QCoreApplication.translate
        DialogAccount_Setting.setWindowTitle(_translate("DialogAccount_Setting", "账户分类设置"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogAccount_Setting = QtWidgets.QDialog()
    ui = Ui_DialogAccount_Setting()
    ui.setupUi(DialogAccount_Setting)
    DialogAccount_Setting.show()
    sys.exit(app.exec())
