# Form implementation generated from reading ui file 'D:\onedrive\document\PythonDocument\PyQt6ToImprovement\ArticleMaterial\PyQt6\chapter23\ledger\DialogPwdSetting.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_pwd_setting(object):
    def setupUi(self, Dialog_pwd_setting):
        Dialog_pwd_setting.setObjectName("Dialog_pwd_setting")
        Dialog_pwd_setting.resize(400, 158)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_pwd_setting)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(parent=Dialog_pwd_setting)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 2)
        self.label_confirm = QtWidgets.QLabel(parent=Dialog_pwd_setting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_confirm.sizePolicy().hasHeightForWidth())
        self.label_confirm.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_confirm.setFont(font)
        self.label_confirm.setObjectName("label_confirm")
        self.gridLayout.addWidget(self.label_confirm, 2, 0, 1, 1)
        self.lineEdit_pwd_new = QtWidgets.QLineEdit(parent=Dialog_pwd_setting)
        self.lineEdit_pwd_new.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_pwd_new.setObjectName("lineEdit_pwd_new")
        self.gridLayout.addWidget(self.lineEdit_pwd_new, 1, 1, 1, 2)
        self.checkBox_showPWD = QtWidgets.QCheckBox(parent=Dialog_pwd_setting)
        self.checkBox_showPWD.setObjectName("checkBox_showPWD")
        self.gridLayout.addWidget(self.checkBox_showPWD, 3, 0, 1, 1)
        self.lineEdit_pwd_new2 = QtWidgets.QLineEdit(parent=Dialog_pwd_setting)
        self.lineEdit_pwd_new2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_pwd_new2.setObjectName("lineEdit_pwd_new2")
        self.gridLayout.addWidget(self.lineEdit_pwd_new2, 2, 1, 1, 2)
        self.lineEdit_pwd_old = QtWidgets.QLineEdit(parent=Dialog_pwd_setting)
        self.lineEdit_pwd_old.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_pwd_old.setObjectName("lineEdit_pwd_old")
        self.gridLayout.addWidget(self.lineEdit_pwd_old, 0, 1, 1, 2)
        self.label_old_pwd = QtWidgets.QLabel(parent=Dialog_pwd_setting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_old_pwd.sizePolicy().hasHeightForWidth())
        self.label_old_pwd.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_old_pwd.setFont(font)
        self.label_old_pwd.setObjectName("label_old_pwd")
        self.gridLayout.addWidget(self.label_old_pwd, 0, 0, 1, 1)
        self.label_pwd = QtWidgets.QLabel(parent=Dialog_pwd_setting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_pwd.sizePolicy().hasHeightForWidth())
        self.label_pwd.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_pwd.setFont(font)
        self.label_pwd.setObjectName("label_pwd")
        self.gridLayout.addWidget(self.label_pwd, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_ok = QtWidgets.QPushButton(parent=Dialog_pwd_setting)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtWidgets.QPushButton(parent=Dialog_pwd_setting)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog_pwd_setting)
        self.pushButton_cancel.clicked.connect(Dialog_pwd_setting.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog_pwd_setting)
        Dialog_pwd_setting.setTabOrder(self.lineEdit_pwd_old, self.lineEdit_pwd_new)
        Dialog_pwd_setting.setTabOrder(self.lineEdit_pwd_new, self.lineEdit_pwd_new2)
        Dialog_pwd_setting.setTabOrder(self.lineEdit_pwd_new2, self.checkBox_showPWD)
        Dialog_pwd_setting.setTabOrder(self.checkBox_showPWD, self.pushButton_ok)
        Dialog_pwd_setting.setTabOrder(self.pushButton_ok, self.pushButton_cancel)

    def retranslateUi(self, Dialog_pwd_setting):
        _translate = QtCore.QCoreApplication.translate
        Dialog_pwd_setting.setWindowTitle(_translate("Dialog_pwd_setting", "设置密码"))
        self.label_4.setText(_translate("Dialog_pwd_setting", "如果没有旧密码，可以不用填写。"))
        self.label_confirm.setText(_translate("Dialog_pwd_setting", "密码确认："))
        self.checkBox_showPWD.setText(_translate("Dialog_pwd_setting", "显示密码"))
        self.label_old_pwd.setText(_translate("Dialog_pwd_setting", "旧 密 码 ："))
        self.label_pwd.setText(_translate("Dialog_pwd_setting", "新 密 码 ："))
        self.pushButton_ok.setText(_translate("Dialog_pwd_setting", "确定"))
        self.pushButton_cancel.setText(_translate("Dialog_pwd_setting", "取消"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_pwd_setting = QtWidgets.QDialog()
    ui = Ui_Dialog_pwd_setting()
    ui.setupUi(Dialog_pwd_setting)
    Dialog_pwd_setting.show()
    sys.exit(app.exec())
