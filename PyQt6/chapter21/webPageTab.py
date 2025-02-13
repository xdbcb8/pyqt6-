#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   webPageTab.py
@Time    :   2023/11/29 14:43:20
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第21章简单浏览器--页面标签页

from PyQt6.QtWidgets import QTabWidget, QTabBar, QMenu, QProgressDialog, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest
from webview import WebView
from downLoadDialog import DownLoadDialog
from datetime import datetime

class BrowserTabWidget(QTabWidget):
    hoveredSignal = pyqtSignal(str) # 光标移动到网页URL上产生的信号
    currentViewUrlSignal = pyqtSignal(str) # 当前浏览URL的信号
    zoomStatusSignal = pyqtSignal(float) # 浏览页面是否放大的信号
    urlChangeSignal = pyqtSignal(str) # 当前浏览URL变化时的信号
    loadProgressSignal = pyqtSignal(int) # 载入进度的信号

    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.setDocumentMode(True)
        # 此属性保存选项卡窗口小部件是否以适合文档页面的模式呈现。此设置下对于显示页面覆盖大部分选项卡小部件区域的文档类型页面非常有用。

        self.setMovable(True) # 标签页可以移动
        self.setTabsClosable(True) # 标签页可以关闭
        self.webviewsList = [] # 暂存网页浏览控件的列表
        self.currentChanged.connect(self.tabChange)
        self.tabCloseRequested.connect(self.closeTab)

        tab_bar = self.tabBar()
        tab_bar.setSelectionBehaviorOnRemove(QTabBar.SelectionBehavior.SelectPreviousTab)
        # 删除当前标签页后以上次选择的标签页作为当前标签页
        tab_bar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu) 
        tab_bar.customContextMenuRequested.connect(self.contextMenuTab) # 标签右键菜单

    def addnewTab(self):
        """
        新开网页
        """
        newWebView = WebView(self)
        index = self.count() # 标签页的数量
        self.webviewsList.append(newWebView) # 添加网页浏览控件到列表
        title = f"新标签页 {index + 1}" # 原始标题
        self.addTab(newWebView, title) # 新增一个窗体用于加载网页的
        self.setCurrentIndex(index)
        self.page = newWebView.page() # 网页浏览的页面
        self.page.profile().downloadRequested.connect(self.downloadRequested) # 下载文件信号触发
        self.page.titleChanged.connect(self.webTitle) # 标题变化信号触发
        self.page.iconChanged.connect(self.webIcon) # 图标变化信号触发
        self.page.urlChanged.connect(self.webUrlChange) # URL变化信号触发
        self.page.linkHovered.connect(self.showURL) # 光标移动到链接上信号触发
        self.page.loadProgress.connect(self.emitLoadProgress) # 载入网页进度信号触发
        return newWebView
    
    def emitLoadProgress(self, value):
        """
        发射当前载入进度
        value：当前载入进度
        """
        self.loadProgressSignal.emit(value)

    def downloadRequested(self, item):
        """
        获取下载请求的 URL，并启动下载对话框
        item：下载对象
        """
        downLoadItem = item
        if downLoadItem and downLoadItem.state() == QWebEngineDownloadRequest.DownloadState.DownloadRequested:
            # 进入下载状态就会打开下载对话框
            downloadDialog = DownLoadDialog(downLoadItem, self)
            downloadDialog.downloadStart.connect(self.downloading)
            downloadDialog.exec()

    def downloading(self, item, path, downLoadName):
        """
        预备下载了
        """ 
        self.now1 = datetime.now()  # 开始计时
        self.downLoadItem = item
        self.downLoadItem.setDownloadDirectory(path) # 设置下载目录
        self.downLoadItem.setDownloadFileName(downLoadName) # 设置下载文件名
        self.downLoadItem.accept() # 开始下载
        self.downLoadItem.totalBytesChanged.connect(self.updateProgress) # 下载文件总大小
        self.downLoadItem.receivedBytesChanged.connect(self.updateProgress) # 下载文件接收大小
        self.downLoadItem.stateChanged.connect(self.updateProgress) # 下载文件的状态变化
        self.execProgressDialog()

    def execProgressDialog(self):
        """
        启动下载进程对话框
        """
        self.progress = QProgressDialog(self)
        self.progress.setWindowTitle("正在下载文件")  
        self.progress.setCancelButtonText("取消")
        self.progress.setMinimumDuration(100) # 预估最少时间大于0.1秒才显示对话框
        self.progress.setWindowModality(Qt.WindowModality.WindowModal) # 对话框模态
        self.progress.setRange(0, 100)
        self.progress.canceled.connect(self.canceledDownLoad) # 单击“取消”按钮触发

    def canceledDownLoad(self):
        """
        取消下载
        """
        self.downLoadItem.cancel()

    def UnitConversion(self, size):
        """
        单位转换
        """
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024*1024:
            return f"{size/1024:.2f} KB"
        elif size < 1024*1024*1024:
            return f"{size/pow(1024, 2):.2f} MB"
        else:
            return f"{size/pow(1024, 3):.2f} GB"

    def updateProgress(self):
        """
        更新进度对话框
        """
        duration = (datetime.now() - self.now1).seconds # 持续时间（秒）
        if duration == 0:
            duration = 1
        totalBytes = self.downLoadItem.totalBytes() # 总的大小
        receivedBytes = self.downLoadItem.receivedBytes() # 已经下载的大小
        bytesPerSecond = receivedBytes / duration # 平均下载速度
        downLoadState = self.downLoadItem.state() # 下载状态
        if downLoadState == QWebEngineDownloadRequest.DownloadState.DownloadInProgress:
            # 下载
            if totalBytes >= 0:
                self.progress.setValue(100 * receivedBytes / totalBytes)
                downloadInfo = f"接收：{self.UnitConversion(receivedBytes)}，总大小：{self.UnitConversion(totalBytes)}，平均下载速度：{self.UnitConversion(bytesPerSecond)}/S"
                self.progress.setLabelText(downloadInfo)
            else:
                self.progress.setValue(0)
                downloadInfo = f"接收：{self.UnitConversion(receivedBytes)}，总大小未知，平均下载速度：{self.UnitConversion(bytesPerSecond)}/S"
                self.progress.setLabelText(downloadInfo)
        elif downLoadState == QWebEngineDownloadRequest.DownloadState.DownloadCompleted:
            # 下载完毕
            QMessageBox.information(self, "提示", "下载完毕！")
        elif downLoadState == QWebEngineDownloadRequest.DownloadState.DownloadInterrupted:
            # 下载被终止，如：网络问题
            self.progress.setValue(0)
            downloadInfo = f"下载失败！\n接收：{self.UnitConversion(receivedBytes)}，总大小：{self.UnitConversion(totalBytes)}，平均下载速度：{self.UnitConversion(bytesPerSecond)}/S\n{self.downLoadItem.interruptReasonString()}"
            self.progress.setLabelText(downloadInfo)

    def tabChange(self, index):
        '''
        当前浏览页面发生任何变化时，地址栏中的url始终和当前浏览页面的url保持一致。
        index：QTabWidget的索引
        '''
        URL = self.tabURL(index).toString()
        self.currentViewUrlSignal.emit(URL)

    def webTitle(self, title):
        '''
        取部分标题
        title：标题
        '''
        index = self.currentIndex()
        if len(title) > 16:
            title = title[0:17]
        self.setTabText(index, title)

    def webIcon(self, icon):
        '''
        标签页上显示网址图标
        icon：网站图标
        '''
        index = self.currentIndex()
        self.setTabIcon(index, icon)
    
    def webUrlChange(self, URL):
        '''
        将浏览的URL发射到主窗体
        '''
        self.urlChangeSignal.emit(URL.toString()) # 变化的URL发射给主窗体

    def showURL(self, URL):
        '''
        向主窗体发送URL
        '''
        self.hoveredSignal.emit(URL)

    def load(self, URL):
        """
        载入URL
        """
        index = self.currentIndex()
        if index >= 0 and URL.isValid():
            self.webviewsList[index].setUrl(URL)

    def tabURL(self, index):
        """
        返回标签页对应网页的URL
        index：标签页的索引
        """
        if index >= 0:
            return self.webviewsList[index].url()
        else:
            return QUrl()

    def back(self):
        """
        后退
        """
        index = self.currentIndex()
        if index >= 0:
            self.webviewsList[index].back()

    def forward(self):
        """
        前进
        """
        index = self.currentIndex()
        if index >= 0:
            self.webviewsList[index].forward()

    def reload(self):
        """
        刷新
        """
        index = self.currentIndex()
        if index >= 0:
            self.webviewsList[index].reload()

    def stop(self):
        """
        停止
        """
        index = self.currentIndex()
        if index >= 0:
            self.webviewsList[index].stop()

    def zoomIn(self):
        """
        页面放大
        """
        index = self.currentIndex()
        if index >= 0:
            zoomf = self.webviewsList[index].getZoom()
            zoomf += 0.25
            self.webviewsList[index].setZoom(zoomf)
            if zoomf >= 5.0:
                zoomf =5.0
            self.webviewsList[index].setZoomFactor(zoomf)
            self.zoomStatusSignal.emit(zoomf)

    def zoomOut(self):
        """
        页面缩小
        """
        index = self.currentIndex()
        if index >= 0:
            zoomf = self.webviewsList[index].getZoom()
            zoomf -= 0.25
            self.webviewsList[index].setZoom(zoomf)
            if zoomf <= 0.25:
                zoomf = 0.25
            self.webviewsList[index].setZoomFactor(zoomf)
            self.zoomStatusSignal.emit(zoomf)

    def zoomReset(self):
        """
        页面恢复
        """
        index = self.currentIndex()
        if index >= 0:
            self.webviewsList[index].setZoom(1.0)
            self.webviewsList[index].setZoomFactor(1.0)
            self.zoomStatusSignal.emit(1.0)

    def getZoomFactor(self):
        """
        返回当前浏览标签的缩放因子
        """
        index = self.currentIndex()
        if index >= 0:
            return self.webviewsList[index].getZoom()

    def contextMenuTab(self, point):
        """
        标签页的右键菜单
        """
        index = self.tabBar().tabAt(point)
        if index < 0:
            return
        tab_count = len(self.webviewsList)
        context_menu = QMenu()
        copyTab = context_menu.addAction("复制标签")
        closeTab = context_menu.addAction("关闭标签")
        closeOtherTabs = context_menu.addAction("关闭其他标签")
        closeOtherTabs.setEnabled(tab_count > 1)
        closeRightTabs = context_menu.addAction("关闭右侧标签")
        closeRightTabs.setEnabled(index < tab_count - 1)
        closeLeftTabs = context_menu.addAction("关闭左侧标签")
        closeLeftTabs.setEnabled(index > 0)        
        chosen_action = context_menu.exec(self.tabBar().mapToGlobal(point))
        if chosen_action == copyTab: # 复制标签并载入原来标签的网页
            chosenTaburl = self.tabURL(index)
            self.addnewTab().load(chosenTaburl)
        elif chosen_action == closeTab: # 关闭标签
            self.closeTab(index)
        elif chosen_action == closeOtherTabs: # 关闭其他标签
            for otherIndex in range(tab_count - 1, -1, -1):
                if otherIndex != index:
                    self.closeTab(otherIndex)
        elif chosen_action == closeRightTabs: # 关闭右侧标签
            for rightIndex in range(tab_count - 1, index, -1):
                self.closeTab(rightIndex)
        elif chosen_action == closeLeftTabs: # 关闭左侧标签
            for leftIndex in range(0, index):
                self.closeTab(leftIndex)

    def closeTab(self, index):
        """
        关闭标签
        index：索引
        """
        if index >= 0 and self.count() > 1:
            webengineview = self.webviewsList[index]
            self.webviewsList.remove(webengineview)
            self.removeTab(index)