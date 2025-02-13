#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mainFunction.py
@Time    :   2023/11/28 15:56:19
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第21章简单浏览器--主程序

import img_rc
import sys
from PyQt6.QtCore import pyqtSlot, QUrl, Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QLineEdit, QLabel, QCompleter, QProgressBar
from PyQt6.QtGui import QStandardItemModel
from webPageTab import BrowserTabWidget
from PyQt6.QtWebEngineCore import QWebEnginePage
from Ui_main import Ui_MainWindow
from bookmark import loadAction2Bar, add2Bar

class LineEdit(QLineEdit):
    """
    自定义URL输入栏
    """
    def __init__(self, Parent=None):  
        super().__init__(Parent)  
  
    def mousePressEvent(self, event): 
        # 在URL输入栏内单击一下会全选里面的URL
        if event.button() == Qt.MouseButton.LeftButton:
            if self.text():
                self.selectAll()

class FunctionMW(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        """
        界面上还有一些控件需要添加
        """
        self.URL_Line = LineEdit(self.toolBar_url) # URL地址栏
        self.URL_Line.setClearButtonEnabled(True)
        self.URL_Line.returnPressed.connect(self.returnloadURL) # 按下回车键后触发
        self.URL_Line.textChanged.connect(self.autoURL) # URL输入时触发
        self.toolBar_url.addWidget(self.URL_Line)
        self.toolBar_bookmark.actionTriggered.connect(self.ActionLoadURL)

        self.loadProgress = QProgressBar(self) # 网页载入进度条
        self.loadProgress.setTextVisible(False) # 不显示进度数字
        self.loadProgress.setHidden(True) # 开始时隐藏

        self.statusBar.addPermanentWidget(self.loadProgress) # 状态栏添加进度条
        self.zoomLabel = QLabel("100%", self) # 缩放状态
        self.statusBar.addPermanentWidget(self.zoomLabel) # 状态栏添加页面大小

        self.webPageTabWidget = BrowserTabWidget(self)
        self.setCentralWidget(self.webPageTabWidget)
        # webPageTabWidget自定义信号的触发
        self.webPageTabWidget.hoveredSignal.connect(self.showURL)
        self.webPageTabWidget.currentViewUrlSignal.connect(self.currentChange)
        self.webPageTabWidget.zoomStatusSignal.connect(self.updateZoomLabel)
        self.webPageTabWidget.urlChangeSignal.connect(self.currentChange)
        self.webPageTabWidget.loadProgressSignal.connect(self.showLoadProgress)
        self.newTabLoadURL("") # 新标签是空URL
        self.showMaximized() # 最大化
        self.getModel()
        self.loadingAction()

    def showLoadProgress(self, value):
        """
        使用进度条显示页面载入进度
        value：页面载入进度
        """
        self.loadProgress.setHidden(False)
        self.loadProgress.setValue(value)
        if value == 100:
            self.loadProgress.setValue(0)
            self.loadProgress.setHidden(True)

    def loadingAction(self):
        """
        添加收藏URL到工具栏
        """
        loadAction2Bar(self.toolBar_bookmark)

    def ActionLoadURL(self, action):
        """
        单击收藏的URL打开网页
        action：收藏URL对应的菜单项
        """
        ActionURL = action.data()
        self.newTabLoadURL(ActionURL)

    def updateZoomLabel(self, p):
        """
        调整浏览器页面大小的状态
        p：页面大小
        """
        value = f"{p*100:.0f}%"
        self.zoomLabel.setText(value)

    def getModel(self):
        '''
        URL自动补全
        '''
        self.m_model = QStandardItemModel(0, 1, self)
        m_completer = QCompleter(self.m_model, self)
        self.URL_Line.setCompleter(m_completer)
        m_completer.activated[str].connect(self.onUrlChoosed)

    def onUrlChoosed(self, URL):
        '''
        自动补全URL
        '''
        self.URL_Line.setText(URL)

    def returnloadURL(self):
        """
        按下回车后载入地址栏的URL
        """
        lineEditURL = self.URL_Line.text().strip() # 地址栏中的URL
        if not lineEditURL:
            return
        else:
            webURL = QUrl.fromUserInput(lineEditURL)
            if webURL.isValid():
                self.webPageTabWidget.load(webURL)

    def autoURL(self, text):
        '''
        URL输入栏，自动补全功能
        '''
        urlGroup = text.split(".")
        if len(urlGroup) == 3 and urlGroup[-1]:
            return
        elif len(urlGroup) == 3 and not(urlGroup[-1]):
            wwwList = ["com", "cn", "net", "org", "gov", "cc"]
            self.m_model.removeRows(0, self.m_model.rowCount())
            for i in range(0, len(wwwList)):
                self.m_model.insertRow(0)
                self.m_model.setData(self.m_model.index(0, 0), text + wwwList[i])
        # 当我们输入类似“www.baidu.”后，会判断一下，最后一个“.”是否为空，要是为空就把常见的域名后缀加上，否则就返回

    def newTabLoadURL(self, URL):
        """
        新建标签
        URL：URL地址
        """
        self.webPageTabWidget.addnewTab().load(QUrl(URL))

    def showURL(self, URL):
        """
        在状态栏显示URL
        """
        self.statusBar.showMessage(URL)

    def currentChange(self, URL):
        """
        在URL输入栏显示URL和调整当前页面的缩放因子显示
        URL：正在浏览的URL
        """
        self.URL_Line.setText(URL)
        zoomFactor = self.webPageTabWidget.getZoomFactor() # 当前页面的缩放因子
        self.updateZoomLabel(zoomFactor)
        # 以下是前进、后退菜单项是否启用的设置
        isForwardEnable = self.webPageTabWidget.currentWidget().page().action(QWebEnginePage.WebAction.Forward).isEnabled()
        isBackEnable = self.webPageTabWidget.currentWidget().page().action(QWebEnginePage.WebAction.Back).isEnabled()
        self.action_F.setEnabled(isForwardEnable)
        self.action_B.setEnabled(isBackEnable)

    @pyqtSlot()
    def on_action_New_triggered(self):
        """
        新增标签
        """
        self.newTabLoadURL("")

    @pyqtSlot()
    def on_action_Quit_triggered(self):
        """
        退出浏览器
        """
        QApplication.quit()

    @pyqtSlot()
    def on_action_CW_triggered(self):
        """
        关闭当前标签
        """
        currentIndex = self.webPageTabWidget.currentIndex()
        self.webPageTabWidget.closeTab(currentIndex)

    @pyqtSlot()
    def on_action_F_triggered(self):
        """
        前进
        """
        self.webPageTabWidget.forward()

    @pyqtSlot()
    def on_action_B_triggered(self):
        """
        退后
        """
        self.webPageTabWidget.back()

    @pyqtSlot()
    def on_action_R_triggered(self):
        """
        刷新
        """
        self.webPageTabWidget.reload()
    
    @pyqtSlot()
    def on_action_Stop_triggered(self):
        """
        停止
        """
        self.webPageTabWidget.stop()
    
    @pyqtSlot()
    def on_action_HOME_triggered(self):
        """
        打开主页
        """
        self.newTabLoadURL("https://cn.bing.com")
        self.currentChange("https://cn.bing.com")
        # self.newTabLoadURL("https://pan.baidu.com/download#win")
        # self.currentChange("https://pan.baidu.com/download#win")

    @pyqtSlot()
    def on_action_sc2bar_triggered(self):
        """
        收藏的URL添加到工具栏
        """
        currentWebView = self.webPageTabWidget.currentWidget()
        webURL = currentWebView.url() # URL
        title = currentWebView.title() # 标题
        icon = currentWebView.icon() # 图标
        add2Bar(webURL, title, icon, self.toolBar_bookmark)

    @pyqtSlot()
    def on_action_I_triggered(self):
        """
        页面放大
        """
        self.webPageTabWidget.zoomIn()

    @pyqtSlot()
    def on_action_O_triggered(self):
        """
        页面缩小
        """
        self.webPageTabWidget.zoomOut()

    @pyqtSlot()
    def on_action_Reset_triggered(self):
        """
        页面恢复
        """
        self.webPageTabWidget.zoomReset()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    webBrowser = FunctionMW()
    webBrowser.show()
    sys.exit(app.exec())