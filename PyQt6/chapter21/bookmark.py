#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   bookmark.py
@Time    :   2023/12/06 19:25:11
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

# 第21章简单浏览器--书签

import codecs
import os
import json
from PyQt6.QtCore import QStandardPaths
from PyQt6.QtGui import QAction, QIcon

def dirSetting():
    """
    URL收藏以及Web图标保存的路径
    """
    location = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ConfigLocation)
    directory = f"{location}/webBrowser"
    if not os.path.exists(directory): # 如果没有webBrowser目录，就建立一个
        os.makedirs(directory)
    return f"{location}/webBrowser"

def writeBookmarks(bookmarksList):
    """
    URL收藏写入json文件
    bookmarksList：收藏的URL列表
    """
    directory = dirSetting()
    with codecs.open(f"{directory}/bookmarks.json", 'w', "utf-8") as f:
        json.dump(bookmarksList, f, indent=4)

def readBookmarks():
    """
    从json文件中读取URL收藏
    """
    
    directory = dirSetting()
    if os.path.exists(f"{directory}/bookmarks.json"):
        with codecs.open(f"{directory}/bookmarks.json", 'r', "utf-8") as f:
            bookmarksList = json.load(f)
            return bookmarksList
    bookmarksList = [] # 不存在bookmarks.json，说明收藏URL的列表为空
    return bookmarksList

def loadAction2Bar(toolbar):
    """
    将已经收藏的URL添加到浏览器的工具栏上
    toolbar：工具栏对象
    """
    bookmarksList = readBookmarks()
    if bookmarksList:
        for actionList in bookmarksList:
            title = actionList[0] # 标题
            URL = actionList[1]
            iconPath = actionList[2] # 图标路径
            action = QAction(toolbar)
            action.setText(title)
            action.setToolTip(title)
            action.setIcon(QIcon(iconPath))
            action.setData(URL)
            toolbar.addAction(action)

def add2Bar(webURL, title, icon, toolbar):
    """
    将新的URL添加到工具栏上
    webURL：URL，QURL对象
    title：标题
    icon：图标
    toolbar：工具栏对象
    """
    URL = webURL.toString()
    action = QAction(toolbar)
    action.setText(title)
    action.setToolTip(title)
    action.setData(URL)
    if not icon.isNull(): # 如果图标不为空
        action.setIcon(icon)
        iconSizes = icon.availableSizes() # 返回指定模式和状态的可用图标大小列表
        largestSize = iconSizes[len(iconSizes) - 1] # 选定最大的图标大小
        directory = dirSetting()
        icon_file_name = f"{directory}/icon{title[:5]}.png"
        icon.pixmap(largestSize).save(icon_file_name, "png") # 保存图标
        actionList = [title, URL, icon_file_name]
    else:
        actionList = [title, URL, None]
    toolbar.addAction(action)
    bookmarksList = readBookmarks()
    bookmarksList.append(actionList)
    writeBookmarks(bookmarksList)