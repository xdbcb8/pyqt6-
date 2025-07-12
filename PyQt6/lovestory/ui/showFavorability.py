#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File     :   gif_animation_window.py
@Time     :   2025/06/28 10:10:12
@Author   :   yangff
@Version  :   1.0
@微信公众号 : 学点编程吧
'''

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QMovie, QIcon
from config import current_dir


class showFavorabilityWindow(QWidget):
    """
    显示某个女主好感度的小窗体
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self): 
        self.setWindowTitle("好感度")
        self.resize(270, 260)
        self.setWindowIcon(QIcon(current_dir + "/res/icons/heart.png"))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint) # 设置窗口无边框且始终置顶
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setStyleSheet('background:transparent;')  # 设置样式表确保背景透明
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 创建gif显示控件
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.gif_label)
        
        # 创建文本显示控件
        self.text_label = QLabel(self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet('font-size: 16px; font-weight: bold; color: white;')
        layout.addWidget(self.text_label)
        
        # 设置定时器，3秒后隐藏窗体
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_fade_out)

        # 设置渐入动画
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        # 设置渐出动画
        self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_animation.setDuration(500)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.Type.InQuad)
        self.fade_out_animation.finished.connect(self.hide)

        self.setLayout(layout)
        
    def start_fade_out(self):
        """
        启动渐出动画
        """
        self.fade_out_animation.start()

    def show_gif(self, name, value):
        """
        显示gif动画和文本信息
        """
        # 加载gif动画
        if name == "沈若曦":
            gif_path = current_dir + "/res/icons/shen.gif"
        elif name == "陆雨晴":
            gif_path = current_dir + "/res/icons/lu.gif"
        elif name == "苏小萌":
            gif_path = current_dir + "/res/icons/su.gif"
        elif name == "3女主":
            gif_path = current_dir + "/res/icons/all.gif"

        try:
            movie = QMovie(gif_path)
            self.gif_label.setMovie(movie)
            movie.start()
            if not movie.isValid():
                print(f"无法加载GIF文件: {gif_path}")
        except Exception as e:
            print(f"加载GIF文件时出错: {e}")
        
        # 设置文本信息
        if value > 0:
            self.text_label.setText(f'{name}：好感度 +{value}')
        else:
            self.text_label.setText(f'{name}：好感度 {value}')
        
        self.setWindowOpacity(0)
        self.show()
        self.fade_in_animation.start()

        # 显示窗体并启动定时器
        self.timer.start(3000)