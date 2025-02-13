#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   webview.py
@Time    :   2023/11/29 10:38:24
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

# 第21章简单浏览器--浏览页面

from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView

class WebView(QWebEngineView):
    '''
    新的页面
    '''
    def __init__(self, tabWidget):
        '''
        一些初始设置
        '''
        super().__init__()
        self.tabWidget = tabWidget
        self.zoom = 1.0 # 缩放因子
        setting = self.page().profile().settings() # 浏览器设置
        setting.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True) # 可以支持Flash，默认关闭
        setting.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
        # 指定WebEngine是否会尝试预取DNS条目以加快浏览速度，默认为关闭。

    def getZoom(self):
        """
        返回缩放因子 
        """
        return self.zoom
    
    def setZoom(self, p):
        """
        设置缩放因子
        """
        self.zoom = p
    
    def createWindow(self, WebWindowType):
        '''
        新页面
        '''
        if (WebWindowType == QWebEnginePage.WebWindowType.WebBrowserTab or
            WebWindowType == QWebEnginePage.WebWindowType.WebBrowserBackgroundTab):
                return self.tabWidget.addnewTab()
                # 返回新增加的QWebEngineView对象