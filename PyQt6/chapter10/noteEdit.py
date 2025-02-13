#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   noteEdit.py
@Time    :   2023/07/18 15:51:52
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''
# 第10章第2节QPlainTextEdit

import sys
import codecs
import os
from PyQt6.QtWidgets import (QMainWindow, QApplication, QPlainTextEdit, QMessageBox, QFileDialog, 
                             QFontDialog, QWidget, QTextEdit)
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QGuiApplication, QColor, QTextFormat, QPainter
from PyQt6.QtCore import Qt, QDir, QRect

current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录

class LineNumberWidget(QWidget):
    '''
    使文本输入框能有行号：带换行符算一个段落
    '''
    def __init__(self, editor=None):
        super().__init__(editor)
        self.editor = editor # editor指代QPlainTextEdit

    def paintEvent(self, event):
        self.editor.LineNumberWidgetPaintEvent(event)

class CodeEditor(QPlainTextEdit):

    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.LineNumberWidget = LineNumberWidget(self)
        self.blockCountChanged.connect(self.updateLineNumberWidgetWidth) # 段落数变化时调用
        self.updateRequest.connect(self.updateLineNumberWidget) # 文本文档需要更新指定的矩形时调用
        self.cursorPositionChanged.connect(self.highlightCurrentLine) # 光标位置变化时调用
        self.updateLineNumberWidgetWidth()
        self.highlightCurrentLine() # 初始化时调用一次让行出现高亮

    def LineNumberWidgetWidth(self):
        """
        显示行号控件的宽度
        """
        digits = 1
        paragraphs = self.blockCount() # 段落数
        while paragraphs >= 10:
            paragraphs /= 10 # 段落数为10的倍数，导致行号所在控件的宽度会发生变化
            digits += 1
        if digits <= 4: # 9999行以内控件宽度不变
            space = 3 + self.fontMetrics().horizontalAdvance('0000')
        else: # 否则根据当前字体的宽度来设定显示行号控件的宽度
            space = 3 + self.fontMetrics().horizontalAdvance('0') * digits 
        return space

    def updateLineNumberWidgetWidth(self):
        # 更新滚动区域周围的边距(int left, int top, int right, int bottom)
        self.setViewportMargins(self.LineNumberWidgetWidth(), 0, 0, 0)

    def updateLineNumberWidget(self, rect, dy):
        """
        文档变化时，整个视口区域需要发生改变
        rect：发生改变的矩形
        dy：视口滚动的像素量
        """
        if dy:
            self.LineNumberWidget.scroll(0, dy) # 向下滚动dy
        else:
            self.LineNumberWidget.update(0, rect.y(), self.LineNumberWidget.width(), rect.height())
            # 重新绘制行号所在控件的矩形

        if rect.contains(self.viewport().rect()):
            # 判断编辑器视口的矩形是否在rect这个矩形内
            self.updateLineNumberWidgetWidth()

    def resizeEvent(self, event):
        '''
        接收在事件参数中传递的控件尺寸调整事件
        '''
        cr = self.contentsRect() # 返回控件边距内的区域
        self.LineNumberWidget.setGeometry(QRect(cr.left(), cr.top(), self.LineNumberWidgetWidth(), cr.height())) # 设置行号所在控件的尺寸
        super().resizeEvent(event) # 重写resizeEvent事件的托底用

    def highlightCurrentLine(self):
        """
        让行高亮
        """
        extraSelections = QTextEdit.ExtraSelection()
        
        # QTextEdit.ExtraSelection 是 Qt 中的一种结构，用于描述在文本编辑器中显示的额外选择。 
        # 它由以下属性组成：
        # cursor：QTextCursor类对象，表示文本区域的光标位置。
        # format：QTextCharFormat类对象，表示应用于文本区域的样式。您可以设置字体、颜色、背景等属性。
        # selectionStart：表示文本区域的起始位置。
        # selectionEnd：表示文本区域的结束位置。

        if not self.isReadOnly():
            lineColor = QColor(Qt.GlobalColor.gray).lighter(150) # 灰色
            extraSelections.format.setBackground(lineColor)
            extraSelections.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            # 当在选择的characterFormat的对象format上设置时，将显示文本的整个宽度。
            # 如果 Selection 属性设置为 True，则选择将显示为单行，并且文本的整个宽度内容将被选择。
            # 如果 Selection 属性设置为 False，则选择将显示为块
            extraSelections.cursor = self.textCursor()
            extraSelections.cursor.clearSelection() # 清除选择
        self.setExtraSelections([extraSelections]) # 设置ExtraSelections

    def LineNumberWidgetPaintEvent(self, event):
        """
        绘制行号所在的控件
        """
        painter = QPainter(self.LineNumberWidget)
        painter.fillRect(event.rect(), Qt.GlobalColor.lightGray) # 构建一个绘画设备，并用淡灰色填充给定的矩形

        block = self.firstVisibleBlock() # 返回第一个段落
        blockNumber = block.blockNumber() # 返回段落的编号
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        # 使用blockBoundingGeometry()方法，以内容坐标返回文本块的边界矩形，
        # 并使用contentOffset()转义得到矩形以获得视口上的视觉坐标。这里得到top。
        bottom = top + round(self.blockBoundingRect(block).height()) # top+行高=底

        while block.isValid() and top <= event.rect().bottom():
            number = str(blockNumber + 1) # 行号
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(0, top, self.LineNumberWidget.width(), self.fontMetrics().height(),
                            Qt.AlignmentFlag.AlignCenter, number) # 绘制行号
            block = block.next() # 下个文本块
            top = bottom # 原来的底变成顶
            bottom = top + round(self.blockBoundingRect(block).height()) # 现在的底又更新了
            blockNumber += 1
            
class NoteEdit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        界面的搭建
        """
        self.resize(800, 600)
        self.statusBar().showMessage("准备就绪") # 状态栏
        self.noteEdit = CodeEditor(self) # 创建自定义QPlainTextEdit对象
        self.document = self.noteEdit.document() # 文档内容
        self.setCentralWidget(self.noteEdit)
        QDir.addSearchPath("icon", f"{current_dir}\images")
        self.setCurrentText("") # 一开始没有文本内容

        # ###########开始创建菜单#############
        # ############菜单--文件##############
        fileMenu = self.menuBar().addMenu("文件(&F)")
        fileToolBar = self.addToolBar("FileOP")
        # 新建
        newFileIcon = QIcon("icon:new.png")
        newAct = QAction(newFileIcon, "新建(&N)", self)
        newAct.setShortcuts(QKeySequence.StandardKey.New)
        newAct.setStatusTip("新建文件")
        fileMenu.addAction(newAct)
        fileToolBar.addAction(newAct)
        # 打开
        openFileIcon = QIcon("icon:open.png")
        openAct = QAction(openFileIcon, "打开(&O)...", self)
        openAct.setShortcuts(QKeySequence.StandardKey.Open)
        openAct.setStatusTip("打开已经存在的文件")
        fileMenu.addAction(openAct)
        fileToolBar.addAction(openAct)

        fileMenu.addSeparator()
        # 保存
        saveIcon = QIcon("icon:save.png")
        saveAct = QAction(saveIcon, "保存(&S)", self)
        saveAct.setShortcuts(QKeySequence.StandardKey.Save)
        saveAct.setStatusTip("保存该文件")
        fileMenu.addAction(saveAct)
        fileToolBar.addAction(saveAct)
        # 另存为
        saveAsIcon = QIcon("icon:saveas.png")
        saveAsAct = fileMenu.addAction(saveAsIcon, "另存为(&A)...", self.saveAs)
        saveAsAct.setShortcut("Ctrl+Shift+S")
        saveAsAct.setStatusTip("将该文档另存一份")

        fileMenu.addSeparator()
        # 退出
        exitIcon = QIcon("icon:exit.png")
        exitAct = fileMenu.addAction(exitIcon, "退出(&x)", self.close)
        exitAct.setShortcuts(QKeySequence.StandardKey.Quit)
        exitAct.setStatusTip("退出程序")

        # #####菜单--编辑############
        editMenu = self.menuBar().addMenu("编辑(&E)")
        editToolBar = self.addToolBar("Edit")
        # 撤销
        undoIcon = QIcon("icon:undo.png")
        undoAct = QAction(undoIcon, "撤销(&U)", self)
        undoAct.setShortcuts(QKeySequence.StandardKey.Undo)
        undoAct.setStatusTip("撤销刚刚写的内容")
        editMenu.addAction(undoAct)

        editMenu.addSeparator()
        # 剪贴
        cutIcon = QIcon("icon:cut.png")
        cutAct = QAction(cutIcon, "剪贴(&t)", self)
        cutAct.setShortcuts(QKeySequence.StandardKey.Cut)
        cutAct.setStatusTip("将所选内容剪贴到粘贴板")
        editMenu.addAction(cutAct)
        editToolBar.addAction(cutAct)
        # 复制
        copyIcon = QIcon("icon:copy.png")
        copyAct = QAction(copyIcon, "复制(&C)", self)
        copyAct.setShortcuts(QKeySequence.StandardKey.Copy)
        copyAct.setStatusTip("将所选内容复制到粘贴板")
        editMenu.addAction(copyAct)
        editToolBar.addAction(copyAct)
        # 粘贴
        pasteIcon = QIcon("icon:paste.png")
        pasteAct = QAction(pasteIcon, "粘贴(&P)", self)
        pasteAct.setShortcuts(QKeySequence.StandardKey.Paste)
        pasteAct.setStatusTip("粘贴粘贴板上的内容")
        editMenu.addAction(pasteAct)
        editToolBar.addAction(pasteAct)

        # #####菜单--格式############
        formatMenu = self.menuBar().addMenu("格式(&O)")
        # 自动换行
        lineWrappedAct = QAction("自动换行(&W)", self)
        lineWrappedAct.setCheckable(True)
        lineWrappedAct.setChecked(True)
        lineWrappedAct.setShortcut("ALt+W")
        lineWrappedAct.setStatusTip("设置自动换行")
        formatMenu.addAction(lineWrappedAct)
        # 字体
        fontAct = QAction("字体(&F)...", self)
        fontAct.setShortcut("ALt+F")
        fontAct.setStatusTip("设置文档字体")
        formatMenu.addAction(fontAct)
        # #####菜单--查看############
        zoomMenu = self.menuBar().addMenu("查看(&V)")
        zoomBar = self.addToolBar("zoom")

        # 放大
        zoomInIcon = QIcon("icon:zoomin.png")
        zoomInAct = QAction(zoomInIcon, "放大(&I)", self)
        zoomInAct.setShortcuts(QKeySequence.StandardKey.ZoomIn)
        zoomMenu.addAction(zoomInAct)
        zoomInAct.setStatusTip("放大")
        zoomBar.addAction(zoomInAct)
        # 缩小
        zoomOutIcon = QIcon("icon:zoomout.png")
        zoomOutAct = QAction(zoomOutIcon, "缩小(&O)", self)
        zoomOutAct.setShortcuts(QKeySequence.StandardKey.ZoomOut)
        zoomMenu.addAction(zoomOutAct)
        zoomOutAct.setStatusTip("缩小")
        zoomBar.addAction(zoomOutAct)

        # #####菜单--关于############
        aboutMenu = self.menuBar().addMenu("关于(&B)")
        aboutAct = aboutMenu.addAction("关于(&B)本程序")
        aboutAct.setStatusTip("显示程序的一些基本信息")

        aboutQtAct = aboutMenu.addAction("关于(&Q)t")
        aboutQtAct.setStatusTip("显示Qt信息")
        # 一开始剪贴和复制菜单不可用
        cutAct.setEnabled(False)
        copyAct.setEnabled(False)

        # ####菜单项与槽连接############
        self.noteEdit.copyAvailable.connect(cutAct.setEnabled) # 文本被选择后启用剪贴按钮
        self.noteEdit.copyAvailable.connect(copyAct.setEnabled) # 文本被选择后启用复制按钮
        newAct.triggered.connect(self.newFile) # 新建文件
        openAct.triggered.connect(self.open) # 打开文件
        saveAct.triggered.connect(self.save) # 保存文件
        undoAct.triggered.connect(self.noteEdit.undo) # 撤销上一步
        cutAct.triggered.connect(self.noteEdit.cut) # 剪贴
        copyAct.triggered.connect(self.noteEdit.copy) # 复制
        pasteAct.triggered.connect(self.noteEdit.paste) # 粘贴
        lineWrappedAct.triggered.connect(self.setLineWrapped) # 换行
        fontAct.triggered.connect(self.setFont) # 字体
        zoomInAct.triggered.connect(self.noteEdit.zoomIn) # 放大
        zoomOutAct.triggered.connect(self.noteEdit.zoomOut) # 缩小
        aboutAct.triggered.connect(self.showAbout)
        aboutQtAct.triggered.connect(self.showAboutQt)

        self.show()

        self.document.contentsChanged.connect(self.documentWasModified) # 当文档更改时

    def documentWasModified(self):
        # 设置当前窗体为是否修改的状态，一般带*号表示已有修改
        self.setWindowModified(self.document.isModified())

    def newFile(self):
        """
        新建文件
        """
        if self.isSave():
            self.noteEdit.clear() # 清除文字
            self.setCurrentText("")

    def open(self):
        """
        打开文件
        """
        if self.isSave():
            fileName = QFileDialog.getOpenFileName(self, "打开文件", "./", "文本文档 (*.txt);;Python文件 (*.py)")
            if fileName[0]:
                self.loadFile(fileName[0])

    def loadFile(self, fileName):
        """
        载入文件
        提示：这里在学习了多线程后，建议用多线程方式，否则读一本小说会卡死你
        """
        try:
            with codecs.open(fileName, "r", "utf-8", errors="ignore") as file:
                content = file.read() # 读取文件
                QGuiApplication.setOverrideCursor(Qt.CursorShape.WaitCursor) # 让光标呈现忙碌的状态
                self.noteEdit.setPlainText(content) # 设置内容
                self.noteEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth) # 默认是设置换行的
                QGuiApplication.restoreOverrideCursor() # 恢复光标
                self.setCurrentText(fileName)
                self.statusBar().showMessage("文件载入成功", 2000) # 状态栏消息保持2000ms
        except FileNotFoundError as e:
            QMessageBox.warning(self, "警告", f"找不到相关文件！原因：{e}")
        except IOError as e:
            QMessageBox.warning(self, "警告", f"打不开相关文件！原因：{e}")
    
    def setCurrentText(self, fileName):
        """
        设置当前读取文档的文件名
        fileName：当前读取的文档文件名
        """
        self.currentFile = fileName
        self.document.setModified(False) # 设置文档未修改
        self.setWindowModified(False) # 设置窗体为未修改的状态

        shownName = self.currentFile
        if not self.currentFile:
            shownName = "无标题.txt"
        self.setWindowFilePath(shownName) # 设置窗体显示文件名

    def saveAs(self):
        """
        另存为
        """
        saveDdialog = QFileDialog.getSaveFileName(self, "保存文件", "./", "文本文档 (*.txt);;Python文件 (*.py)")
        if saveDdialog[0]:
            return self.saveFile(saveDdialog[0])

    def save(self):
        """
        保存
        """
        if not self.currentFile: # 要是当前文件为空，新文档都是为空，调用另存为
            return self.saveAs()
        else: # 否则直接保存当前文件
            return self.saveFile(self.currentFile)

    def saveFile(self, fileName):
        """
        保存文件
        """
        QGuiApplication.setOverrideCursor(Qt.CursorShape.WaitCursor) # 设置光标忙碌
        try:
            with codecs.open(fileName, 'w', 'utf-8') as file:
                content = self.noteEdit.toPlainText()
                file.write(content)
            self.setCurrentText(fileName)
            self.statusBar().showMessage("文件保存成功", 2000)
        except IOError as e:
            QMessageBox.warning(self, "警告", f"文件保存出错，原因：{e}")
        QGuiApplication.restoreOverrideCursor() # 光标恢复

    def isSave(self):
        """
        判断当前内容保存吗
        """
        if not self.document.isModified(): # 当前内容没有修改时
            return True
        # 如果修改了，就创建一个对话框，问问你接下来的操作。
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("请看这里！")
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setText("文件已修改")
        msgBox.setInformativeText("需要保存吗？")
        Save = msgBox.addButton("保存(&S)", QMessageBox.ButtonRole.AcceptRole)
        msgBox.addButton("取消", QMessageBox.ButtonRole.RejectRole)
        msgBox.addButton("不保存(&N)", QMessageBox.ButtonRole.DestructiveRole)
        msgBox.setDefaultButton(Save) # 默认按钮为保存
        reply = msgBox.exec()
        if reply == 0: # 单击了保存
            return self.save()
        elif reply == 1: # 单击取消
            return False
        elif reply == 2: # 单击了不保存
            return True
        
    def setLineWrapped(self, checked):
        """
        设置自动换行
        checked：表示已勾选自动换行
        """
        if not checked: # 不换行
            self.noteEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        else: # 换行
            self.noteEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

    def setFont(self):
        """
        设置字体
        """
        font, isok = QFontDialog.getFont()
        if isok:
            self.noteEdit.setFont(font)

    def showAbout(self):
        """
        关于本程序
        """
        QMessageBox.about(self, "提示", "这是关于QPlainTextEdit的示例程序\n\n微信公众号：学点编程吧")
    
    def showAboutQt(self):
        """
        关于Qt
        """
        QMessageBox.aboutQt(self, "关于Qt")

    def closeEvent(self, event):
        """
        重写关闭事件
        """
        if self.isSave():
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    noteEdit = NoteEdit()
    sys.exit(app.exec())