#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   itemWindow.py
@Time    :   2023/04/16 07:54:38
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

# QWidget的个性化设置

import sys
import img_rc
from itemWindow import ItemWidget
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QIcon
from Ui_widgetExample import Ui_Form


class Form(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)
        self.__initUi()

    def __initUi(self):
        self.item = ItemWidget()
        pos = self.item.pos()
        if pos.x() < 0:
            pos.setX(0)
        if pos.y() < 0:
            pos.setY(0)
        self.item.move(pos)

    @pyqtSlot(str)
    def on_lineEditTitle_textEdited(self, title):
        """
        设置窗体标题
        """
        self.setWindowTitle(title)

    @pyqtSlot(int)
    def on_horizontalSliderTransparency_valueChanged(self, value):
        """
        窗体透明度,v的范围0-1，每次0.1，0是透明，1是不透明
        """
        v = value/10
        self.setWindowOpacity(v)
    
#----------------------WindowsIcon-----------------------

    @pyqtSlot()
    def on_radioButton_icon1_clicked(self):
        """
        设置图标1
        """

        self.setWindowIcon(QIcon(":/icon/pic/titleA.png"))

    @pyqtSlot()
    def on_radioButton_icon2_clicked(self):
        """
        设置图标2
        """
        self.setWindowIcon(QIcon(":/icon/pic/titleB.png"))

    @pyqtSlot()
    def on_radioButton_icon3_clicked(self):
        """
        设置图标3
        """
        self.setWindowIcon(QIcon(":/icon/pic/titleC.png"))    

    #----------------------WindowsType-----------------------

    @pyqtSlot()
    def on_radioButtonDialog_clicked(self):
        """
        WindowFlags:Dialog
        对话框的窗口，标题栏中通常没有最大化或最小化按钮。
        """
        self.item.setFlags(Qt.WindowType.Dialog)
        self.item.show()
        

    @pyqtSlot()
    def on_radioButtonToolTip_clicked(self):
        """
        WindowFlags:ToolTip
        工具提示
        """
        self.item.setFlags(Qt.WindowType.ToolTip)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonSplashScreen_clicked(self):
        """
        WindowFlags:SplashScreen
        实现启动界面
        """
        self.item.setFlags(Qt.WindowType.SplashScreen)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonSheet_clicked(self):
        """
        WindowFlags:Sheet
        指示窗口是 macOS 上的工作表。由于使用工作表意味着窗口模态，因此推荐的方法是使用 setWindowModality()或 open()。windows系统无法演示。
        """
        self.item.setFlags(Qt.WindowType.Sheet)
        self.item.show()


    @pyqtSlot()
    def on_radioButtonWindow_clicked(self):
        """
        WindowFlags:Window
        这是 QWidget 的默认类型。此类型的小部件是子窗口（如果有父小部件）和独立窗口（如果它们没有父窗口）。
        """
        self.item.setFlags(Qt.WindowType.Window)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonTool_clicked(self):
        """
        WindowFlags:Tool
        工具窗口。工具窗口通常是标题栏和装饰小于通常的小窗口，通常用于工具按钮的集合。
        """
        self.item.setFlags(Qt.WindowType.Tool)
        self.item.show()


    @pyqtSlot()
    def on_radioButtonPopup_clicked(self):
        """
        WindowFlags:Popup
        是一个弹出的顶级窗口，即它是模态的，但具有适用于弹出菜单的窗口系统框架。
        """
        self.item.setFlags(Qt.WindowType.Popup)
        self.item.show()
    
    #----------------------WindowsHint-----------------------

    @pyqtSlot()
    def on_radioButtonWindowShadeButton_clicked(self):
        """
        WindowFlags:WindowShadeButtonHint
        添加一个阴影按钮来代替最小化按钮（如果基础窗口管理器支持它）。
        """
        self.item.setFlags(Qt.WindowType.WindowShadeButtonHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonWindowCloseButton_clicked(self):
        """
        WindowFlags:WindowCloseButtonHint
        添加关闭按钮。在某些平台上，这意味着Qt.WindowType.WindowSystemMenuHint可以工作。
        """
        self.item.setFlags(Qt.WindowType.WindowCloseButtonHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonFramelessWindow_clicked(self):
        """
        WindowFlags:FramelessWindowHint
        生成无边框窗口。
        """
        self.item.setFlags(Qt.WindowType.FramelessWindowHint)
        self.item.show()


    @pyqtSlot()
    def on_radioButtonWindowNoShadow_clicked(self):
        """
        WindowFlags:NoDropShadowWindowHint
        禁用支持平台上的窗口投影。
        """
        self.item.setFlags(Qt.WindowType.NoDropShadowWindowHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonWindowContextHelpButton_clicked(self):
        """
        WindowFlags:WindowContextHelpButtonHint
        向对话框添加上下文帮助按钮。在某些平台上，这意味着Qt.WindowType.WindowSystemMenuHint可以工作。
        """
        self.item.setFlags(Qt.WindowType.WindowContextHelpButtonHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonWindowMaximizeButton_clicked(self):
        """
        WindowFlags:WindowMaximizeButtonHint
        添加最大化按钮。在某些平台上，这意味着Qt.WindowType.WindowSystemMenuHint可以工作。
        """
        self.item.setFlags(Qt.WindowType.WindowMaximizeButtonHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonMsWindowsFixedSizeDialog_clicked(self):
        """
        WindowFlags:MSWindowsFixedSizeDialogHint
        在窗口上为窗口提供细对话框边框。此样式传统上用于固定大小的对话框。
        """
        self.item.setFlags(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonWindowSystemMenu_clicked(self):
        """
        WindowFlags:WindowSystemMenuHint
        添加窗口系统菜单，并可能添加关闭按钮（例如在 Mac 上）。如果需要隐藏或显示关闭按钮，使用 WindowCloseButtonHint 会更便携。
        """
        self.item.setFlags(Qt.WindowType.WindowSystemMenuHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonWindowTitle_clicked(self):
        """
        WindowFlags:WindowTitleHint
        为窗口提供标题栏。
        """
        self.item.setFlags(Qt.WindowType.WindowTitleHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonWindowStaysOnTop_clicked(self):
        """
        WindowFlags:WindowStaysOnTopHint
        窗口应位于所有其他窗口的顶部。
        请注意，在 X11 上的某些窗口管理器上，您还必须传递 Qt.WindowType.X11BypassWindowManagerHint 才能使此标志正常工作。
        """
        self.item.setFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonX11BypassWindowManager_clicked(self):
        """
        WindowFlags:X11BypassWindowManagerHint
        完全绕过窗口管理器。这会导致一个完全不受管理的无边框窗口（即，除非您手动调用 activateWindow()，否则没有键盘输入）。
        """
        self.item.setFlags(Qt.WindowType.X11BypassWindowManagerHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonWindowStaysOnBottom_clicked(self):
        """
        WindowFlags:WindowStaysOnBottomHint
        该窗口应位于所有其他窗口的底部。
        """
        self.item.setFlags(Qt.WindowType.WindowStaysOnBottomHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonWindowMinimizeButton_clicked(self):
        """
        WindowFlags:WindowMinimizeButtonHint
        添加最小化按钮。在某些平台上，这意味着Qt.vWindowSystemMenuHint可以工作。
        """
        self.item.setFlags(Qt.WindowType.WindowMinimizeButtonHint)
        self.item.show()

    @pyqtSlot()
    def on_radioButtonCustomizeWindowHint_clicked(self):
        """
        WindowFlags:CustomizeWindowHint
        关闭默认窗口标题提示。
        """
        self.item.setFlags(Qt.WindowType.CustomizeWindowHint)
        self.item.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())