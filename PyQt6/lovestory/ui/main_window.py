#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main_window.py
@Time    :   2025/04/08 22:13:48
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .video_player import VideoPlayer
from .dialogs.context_menu import ContextMenu
from .dialogs.message_menu import MessageMenu
from .showFavorability import showFavorabilityWindow
from .relationship import FavoriteWidget
from .myhistory import HistoryViewer
from config import fullname, current_dir, favorabilityDict, db, branchDict

# 主窗口
class MainWindow(QMainWindow):
    """
    游戏主窗口
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_game() # 启动游戏
        
    def init_ui(self):
        """
        初始化用户界面
        """
        windows = QWidget(self)
        icon = QIcon(current_dir + "/res/icons/heart.png")
        self.setWindowIcon(icon)
        self.setWindowTitle("完蛋了！我也被美女包围了")

        # self.resize(720, 480) # 将视频播放窗口设置成固定大小，全屏会严重影响视频播放质量
        self.resize(1280, 770) # 将视频播放窗口设置成固定大小，全屏会严重影响视频播放质量

        # 计算并设置窗口居中位置
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # 无边框窗口
        
        self.video_player = VideoPlayer(windows) # 视频播放器
        self.context_menu = ContextMenu(windows) # 创建游戏菜单
        self.message_menu = MessageMenu(windows) # 创建玩家选项菜单
        self.favorability_window = showFavorabilityWindow() # 创建好感度窗口
        self.favorability_window.hide() # 好感度窗体默认隐藏
        self.context_menu.show() # 显示游戏菜单

        main_geo = self.geometry() # 获取主窗口位置和大小
        fav_geo = self.favorability_window.geometry() # 获取好感度窗口大小
        x = main_geo.x() + main_geo.width() - fav_geo.width() - 20 # 计算好感度窗口右上角坐标
        y = main_geo.y()
        self.favorability_window.move(x, y)
        
        vlayout = QVBoxLayout(windows)
        vlayout.addWidget(self.video_player, stretch=1)
        vlayout.addWidget(self.context_menu)
        vlayout.addWidget(self.message_menu)
        vlayout.setContentsMargins(0,0,0,0)
        vlayout.setSpacing(0)
        vlayout.setAlignment(self.context_menu, Qt.AlignmentFlag.AlignBottom)
        windows.setLayout(vlayout)

        self.setCentralWidget(windows)

    def getfavorabilityValue(self, videoName):
        '''
        根据视频名称获取好感度信息
        '''
        if favorabilityDict.get(videoName):
            name, value = favorabilityDict.get(videoName)[0], favorabilityDict.get(videoName)[1]
            self.updateFavorability(name, value)

    def updateFavorability(self, name, favorability):
        '''
        启动好感度小窗口，并更新好感度
        '''
        if name == 'all': # 同时增加3女的好感度
            for nameItem in ['苏小萌', '沈若曦', '陆雨晴']:
                db.update_favorability(nameItem, 10) # 同时更新三女好感度
            self.favorability_window.show_gif('3女主', 10)
        else:
            self.favorability_window.show_gif(name, favorability)
            db.update_favorability(name, favorability) # 更新女主好感度

    def start_game(self):
        """
        启动游戏初始设置
        """
        bgm_movie = fullname('bgm.mp4', 0)
        self.video_player.play_scene(bgm_movie)
        self.video_player.choiceDSignal.connect(self.create_message_menu)
        self.video_player.favorabilityValue.connect(self.getfavorabilityValue)
        self.video_player.gameoverSignal.connect(self.gameover)
        self.context_menu.menuSignal.connect(self.on_menu_signal)
        self.message_menu.choiceInfoSignal.connect(self.on_message_signal)
        self.message_menu.updateFavorabilitySignal.connect(self.updateFavorability)

    def on_menu_signal(self, menuinfo):
        """
        处理上下文菜单信号
        """
        if menuinfo == "newgame":
            historyList = db.query_non_empty_datetime()
            if historyList:
                reply = QMessageBox.question(self, "提示", "存在游戏记录，新的游戏会删除所有游戏记录，确定？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.No:
                    return
                else:
                    self.video_player.skip_days.clear() # 清空跳过的剧情
                    newgameVideo = fullname('01.1.1.mp4', 1)
                    self.video_player.playvideo(newgameVideo)
                    self.context_menu.hide()
                    db.clear_favorability() # 好感度清除
                    db.clear_history() # 我的历程清除
            else:
                newgameVideo = fullname('01.1.1.mp4', 1)
                self.video_player.playvideo(newgameVideo)
                self.context_menu.hide()
        elif menuinfo == "continuegame":
            latestvideo = db.query_latest_datetime()
            if latestvideo:
                if latestvideo[0][0][0:5] == '14.2.': # 表明游戏已经结束了
                    QMessageBox.information(self, "提示", "游戏已经结束，无法继续游戏，开始新的游戏吧！")
                else:
                    if branchDict.get(latestvideo[0][0]):
                        self.video_player.playvideo(fullname(latestvideo[0][0], 1))
                    else:
                        self.video_player.get_next_video(latestvideo[0][0])
                    self.context_menu.hide()
        elif menuinfo == "myhistory": # 显示我的历程
            self.history = HistoryViewer()
            self.history.show()
        elif menuinfo == "viewfavor": # 查看女主好感度
            self.view = FavoriteWidget()
            self.view.show()
        elif menuinfo == "exitgame":
            self.close()

    def create_message_menu(self, optionsList):
        '''
        创建消息菜单
        '''
        self.message_menu.setinfomation(optionsList)
        self.message_menu.show()
        if not self.context_menu.isHidden():
            self.context_menu.hide()

    def on_message_signal(self, choiceInfo):
        '''
        处理玩家选项
        '''
        self.video_player.getNvideo(choiceInfo)

    def closeEvent(self, event):
        """
        关闭窗口事件
        """
        reply = QMessageBox.question(self, "退出游戏", "是否退出游戏？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.video_player.stop()
            if hasattr(self, 'favorability_window'):
                self.favorability_window.close() # 关闭显示好感度窗口
            if hasattr(self, 'view'): # 关闭查看好感度窗口
                self.view.close()
            if self.video_player.skip_days: # 要是存在跳过的剧情，会存入数据库中
                for day in self.video_player.skip_days:
                    db.insertSkipday(day)
            db.close()    
            self.close()
        else:
            event.ignore()

    def gameover(self):
        '''
        菜单栏显示
        '''
        self.context_menu.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            # 处理ESC按键事件
            if self.message_menu.isHidden():
                if self.context_menu.isHidden():
                    self.context_menu.show()
                    if self.video_player.current_video != current_dir + "/res/bgm/bgm.mp4":
                        self.video_player.pause()
                else:
                    self.context_menu.hide()
                    if self.video_player.current_video != current_dir + "/res/bgm/bgm.mp4":
                        self.video_player.resume()