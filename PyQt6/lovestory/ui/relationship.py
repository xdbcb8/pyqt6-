#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   relationship.py
@Time    :   2025/04/08 22:14:59
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from config import current_dir, db

class RelationshipWidget(QWidget):
    """
    好感度显示组件
    """

    def __init__(self, character_ids, parent=None):
        super().__init__(parent)
        self.character_ids = character_ids
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout = QHBoxLayout()
        layout.setSpacing(20)

        self.character_widgets = {}

        for char_id in self.character_ids:
            # 创建角色容器
            char_widget = QWidget()
            char_layout = QVBoxLayout()
            char_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # 进度条
            progress_bar = QProgressBar()
            progress_bar.setOrientation(Qt.Orientation.Horizontal)
            progress_bar.setRange(0, 100)
            progress_bar.setValue(0)
            progress_bar.setTextVisible(True)  # 设置进度条显示文本
            progress_bar.setFormat("%p%")  # 设置进度条显示格式为百分比
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid white;
                    border-radius: 5px;
                    background-color: rgba(255, 255, 255, 0.3);
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #FFB6C1;
                    border-radius: 3px;
                }
            """)

            # 图片显示
            image_label = QLabel()
            char_layout.addWidget(progress_bar)
            char_layout.addWidget(image_label)
            char_widget.setLayout(char_layout)

            layout.addWidget(char_widget)
            self.character_widgets[char_id] = {
                'image': image_label,
                'progress': progress_bar
            }

        self.setLayout(layout)

    def update_relationship(self, char_id, value):
        """
        更新指定角色的好感度显示
        """
        if char_id not in self.character_widgets:
            return

        widget = self.character_widgets[char_id]
        widget['progress'].setValue(value)

        # 加载原图片
        gray_pixmap = QPixmap(current_dir + f"/res/characters/{char_id}_gray.png")
        color_pixmap = QPixmap(current_dir + f"/res/characters/{char_id}_color.png")

        # 获取原图片尺寸
        width = gray_pixmap.width()
        height = gray_pixmap.height()

        # 计算显示彩色部分的高度
        color_height = int(height * (value / 100))

        # 创建一个新的QPixmap来合成图片
        combined_pixmap = QPixmap(width, height)
        combined_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(combined_pixmap)
        painter.drawPixmap(0, 0, gray_pixmap)
        if color_height > 0:
            painter.setClipRect(0, height - color_height, width, color_height)
            painter.drawPixmap(0, 0, color_pixmap)
        painter.end()

        widget['image'].setPixmap(combined_pixmap)

class FavoriteWidget(QWidget):
    """
    好感度显示窗体
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.resize(1272, 806)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint) # 设置窗口始终置顶
        self.setWindowTitle('查看好感度')
        icon = QIcon(current_dir + "/res/icons/heart.png")
        self.setWindowIcon(icon)
        layout = QVBoxLayout(self)
        character_ids = ["0", "1", "2"]
        relationship_widget = RelationshipWidget(character_ids)
        layout.addWidget(relationship_widget)
        self.setLayout(layout)

        favorabilitySu = db.query_favorability('苏小萌')
        favorabilityShen = db.query_favorability('沈若曦')
        favorabilityLu = db.query_favorability('陆雨晴')

        relationship_widget.update_relationship("0", favorabilitySu)
        relationship_widget.update_relationship("1", favorabilityShen)
        relationship_widget.update_relationship("2", favorabilityLu)