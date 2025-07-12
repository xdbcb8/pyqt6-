#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   video_player.py
@Time    :   2025/04/08 22:14:32
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QSizePolicy
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, pyqtSignal, Qt
from config import movieList, branchDict, choiceDict, current_dir, get_current_datetime, fullname, defullname, db

class VideoPlayer(QWidget):
    """
    视频播放组件
    """
    choiceDSignal = pyqtSignal(list) # 构建玩家选择对话框的信号
    favorabilityValue = pyqtSignal(str) # 构建好感度信号
    gameoverSignal = pyqtSignal() # 游戏结束

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_video = '' # 当前播放的视频名称（完整路径）
        self.current_day = 1 # 初始化当前天数
        self.current_index = 0 # 初始化索引
        self.skip_days = []  # 存储需要跳过的剧情开始数字
        self.position = 0 # 视频播放的位置
        self.initUi()
        self.loadDate()
    
    def loadDate(self):
        '''
        从数据库查询要跳过的剧情
        '''
        skipdays = db.query_skipday() # 查询需要跳过的剧情
        if skipdays:
            for day in skipdays:
                self.skip_days.append(day[0])

    def initUi(self):
        # 创建媒体播放器对象
        self.media_player = QMediaPlayer()
        # 创建视频小部件对象
        self.video_widget = QVideoWidget()
        self.video_widget.setAspectRatioMode(Qt.AspectRatioMode.IgnoreAspectRatio)
        # 将视频输出设置为视频小部件
        self.media_player.setVideoOutput(self.video_widget)
        # 创建音频输出对象，用于处理媒体播放器的音频输出
        self.audio_output = QAudioOutput()
        # 将创建的音频输出对象设置给媒体播放器，以便播放音频
        self.audio_output.setVolume(100) # 声音设置成100%
        self.media_player.setAudioOutput(self.audio_output)

        self.media_player.errorOccurred.connect(self.handle_error) # 连接错误信号到槽函数
        self.media_player.mediaStatusChanged.connect(self.handle_media_status) # 连接媒体状态改变信号到槽函数
        self.media_player.positionChanged.connect(self.handle_position_changed) # 连接播放位置改变信号到槽函数
        self.media_player.playbackStateChanged.connect(self.handle_pause) # 连接暂停信号到槽函数

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0) # 设置布局的边距为0
        # 设置视频填充整个窗口
        self.video_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.video_widget)
        # 设置当前窗口的布局为创建的垂直布局
        self.setLayout(layout)

    def handle_position_changed(self, position):
        """
        处理播放位置改变事件
        """
        self.position = position # 快到结尾时暂停
        if self.position + 200 >= self.duration:
            self.media_player.pause()
        ### 以下主要是用于触发显示好感度窗体
        if self.position >= 32000 and self.position <= 32045 and defullname(self.current_video) == '04.1.1.mp4':
            self.favorabilityValue.emit('04.1.1.mp4')
        if self.position >= 28000 and self.position <= 28047 and defullname(self.current_video) == '04.2.1.mp4':
            self.favorabilityValue.emit('04.2.1.mp4')
        if self.position >= 60000 and self.position <= 60045 and defullname(self.current_video) == '05.1.1T.mp4':
            self.favorabilityValue.emit('05.1.1T.mp4')
        if self.position >= 64000 and self.position <= 64045 and defullname(self.current_video) == '06.1.1.mp4':
            self.favorabilityValue.emit('06.1.1.mp4')
        if self.position >= 40000 and self.position <= 40045 and defullname(self.current_video) == '06.1.1T.mp4':
            self.favorabilityValue.emit('06.1.1T.mp4')
        if self.position >= 46000 and self.position <= 46045 and defullname(self.current_video) == '11.1.1.mp4':
            self.favorabilityValue.emit('11.1.1.mp4')
        if self.position >= 61000 and self.position <= 61045 and defullname(self.current_video) == '12.1.1.mp4':
            self.favorabilityValue.emit('12.1.1.mp4')
        
    def handle_media_status(self, status):
        """
        处理媒体状态改变事件
        """
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.duration = self.media_player.duration()  # 获取视频总时长

    def handle_pause(self, state):
        '''
        处理暂停事件，意味着准备播放下一个视频了
        '''
        if state == QMediaPlayer.PlaybackState.PausedState:
            if self.position + 200 >= self.duration:
                if self.current_video in [fullname('achievementLu.mp4', 2), fullname('achievementSh.mp4', 2), fullname('achievementSu.mp4', 2)]:
                    self.play_scene(fullname('bgm.mp4', 0))
                    self.gameoverSignal.emit()
                if self.current_video != current_dir + "/res/bgm/bgm.mp4":
                    cvideo = defullname(self.current_video) # 当前视频的文件名（非全部路径）
                    db.update_datetime(cvideo, get_current_datetime()) # 更新一下播放完该视频的时间
                    self.get_next_video(defullname(self.current_video)) # 播放下一个视频
                if defullname(self.current_video) in ['14.2.1.mp4', '14.2.2.mp4', '14.2.3.mp4', '14.2.4.mp4']: # 表明整个游戏处于结尾了
                    favorabilitySu = db.query_favorability('苏小萌')
                    favorabilityShen = db.query_favorability('沈若曦')
                    favorabilityLu = db.query_favorability('陆雨晴')
                    count = sum(1 for num in [favorabilitySu, favorabilityShen, favorabilityLu] if num >= 100)
                    if count == 3:
                        # 三个都大于100
                        QMessageBox.information(self, "恭喜", "三女对你都感兴趣，具体与谁交往，以后再说吧！")
                        self.play_scene(fullname('bgm.mp4', 0))
                        self.gameoverSignal.emit()
                    elif count == 2:
                        # 有两个大于100，需进一步判断具体是哪两个
                        if favorabilitySu >= 100 and favorabilityShen >= 100:
                            QMessageBox.information(self, "恭喜", "苏小萌和沈若曦都对你都感兴趣，具体与谁交往，以后再说吧！")
                        elif favorabilitySu >= 100 and favorabilityLu >= 100:
                            QMessageBox.information(self, "恭喜", "苏小萌和陆雨晴都对你都感兴趣，具体与谁交往，以后再说吧！")
                        else: 
                            QMessageBox.information(self, "恭喜", "沈若曦和陆雨晴都对你都感兴趣，具体与谁交往，以后再说吧！")
                        self.play_scene(fullname('bgm.mp4', 0))
                        self.gameoverSignal.emit()
                    elif count == 1:
                        if favorabilitySu >= 100:
                            self.play_scene(fullname('achievementSu.mp4', 2))
                            QMessageBox.information(self, "恭喜", "恭喜你和苏小萌牵手成功！")
                        elif favorabilityShen >= 100:
                            self.play_scene(fullname('achievementSh.mp4', 2))
                            QMessageBox.information(self, "恭喜", "恭喜你和沈若曦牵手成功！")
                        elif favorabilityLu >= 100:
                            self.play_scene(fullname('achievementLu.mp4', 2))
                            QMessageBox.information(self, "恭喜", "恭喜你和陆雨晴牵手成功！")
                    else:
                        QMessageBox.information(self, "遗憾", "很遗憾，你与三位女主失之交臂，继续努力吧！")
                        self.play_scene(fullname('bgm.mp4', 0))
                        self.gameoverSignal.emit()

    def handle_error(self):
        """
        处理播放错误
        """
        error = self.media_player.error()
        error_string = self.media_player.errorString()
        QMessageBox.critical(self, "播放错误", f"发生错误: {error_string} (代码: {error})")

    def play_scene(self, scene_name):
        """
        播放指定视频
        """
        self.current_video = scene_name # 保存当前播放的视频名称
        if not os.path.exists(self.current_video):
            QMessageBox.critical(self, "错误", f"文件 {self.current_video} 不存在！")
            return
        
        if not self.media_player.videoOutput():
            raise RuntimeError("视频输出未初始化！")
        
        # 设置媒体播放器的播放源为指定的本地文件，本地文件路径由 self.current_video 变量提供
        self.media_player.setSource(QUrl.fromLocalFile(self.current_video))
        self.media_player.play()
    
    def pause(self):
        """暂停播放"""
        self.media_player.pause()
    
    def resume(self):
        """继续播放"""
        self.media_player.play()

    def stop(self):
        """停止播放"""
        self.media_player.stop()

    def get_day(self, video_name):
        '''
        解析视频文件名获取关键词，以便明确具体的后续剧情
        '''
        return int(video_name[0:2])

    def getNvideo(self, optionInfo):
        '''
        根据选项信息获取下一个视频
        '''
        self.next_video = choiceDict[optionInfo]
        if optionInfo == '拒绝参加':
            self.skip_days = [4]  # 跳过社团活动剧情
        elif optionInfo == '委婉拒绝':
            self.skip_days = [9]  # 跳过与苏小萌一家聚餐剧情
        elif optionInfo == '拒绝爬山':
            self.skip_days = [11, 12]  # 跳过爬山后续剧情
        self.playvideo(fullname(self.next_video, 1))

    def get_next_video(self, video):
        '''
        处理用户选择并返回下一个视频
        '''
        # 如果当前视频在branchDict中，获取用户选择
        if video in branchDict:
            options = branchDict[video]
            self.choiceDSignal.emit(options)
            return
        # 如果当前视频不在branchDict中，从movieList中找下一个
        if video in movieList:
            self.current_index = movieList.index(video)
            # 找到下一个不在skip_days中的视频
            for i in range(self.current_index + 1, len(movieList)):
                day = self.get_day(movieList[i])
                if day not in self.skip_days:
                    self.current_index = i
                    self.current_day = day
                    self.playvideo(fullname(movieList[i], 1))
                    return
        
        # 如果不在movieList中，尝试找到下一个天数的视频
        if video == '01.1.2F.mp4':
            self.skip_days = [4]  # 跳过社团活动剧情
        elif video == '07.2.1F.mp4':
            self.skip_days = [9]  # 跳过与苏小萌一家聚餐剧情
        elif video == '10.1.1F.mp4':
            self.skip_days = [11, 12]  # 跳过爬山后续剧情

        self.current_day = self.get_day(video)
        for i, video in enumerate(movieList):
            day = self.get_day(video)
            if day > self.current_day and day not in self.skip_days:
                self.current_index = i
                self.current_day = day
                self.playvideo(fullname(video, 1))
                return
        
    def playvideo(self, videoName):
        '''
        播放视频
        '''
        # 获取用户输入的起始视频
        start_video = defullname(videoName) # 只取视频文件名
        # 确定当前索引
        if start_video in movieList:
            self.current_index = movieList.index(start_video)

        self.current_day = self.get_day(start_video)
        
        self.current_video = videoName

        self.play_scene(self.current_video) # 播放当前视频