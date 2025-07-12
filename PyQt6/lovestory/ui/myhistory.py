from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTableView, QLabel, QHeaderView
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from config import current_dir, db

class HistoryViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_data()
        self.setStyleSheet(self.get_qss())

    def get_image_column_index(self):
        """返回图片数据所在的列索引"""
        return 3

    def init_ui(self):
        self.resize(1280, 770) 
        self.setWindowTitle('我的历程')
        self.setWindowIcon(QIcon(current_dir + '/res/icons/heart.png'))

        # 主布局
        layout = QHBoxLayout()

        # 表格视图
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.clicked.connect(self.show_image)
        self.table_view.setAlternatingRowColors(True)
        layout.addWidget(self.table_view, stretch=2)

        # 图片显示区域
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label, stretch=1)

        self.setLayout(layout)

    def load_data(self):
        # 执行查询

        # 创建模型并设置数据
        model = RowNumberModel()
        self.table_view.setModel(model)

        results = db.query_non_empty_datetime()

        if results:
            for row_idx, row in enumerate(results):
                model.insertRow(row_idx)
                for col_idx, value in enumerate(row):
                    if col_idx == 3:
                        item = QStandardItem()
                        item.setData(value)
                    else:
                        item = QStandardItem(str(value))
                    model.setItem(row_idx, col_idx, item)

        # 隐藏第1和第4列
        self.table_view.setColumnHidden(0, True) # 第0列隐藏（影片）
        self.table_view.setColumnHidden(3, True) # 图片列隐藏，因为返回的二进制字节码太多了，会崩溃的
        # 设置列宽
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

    def get_query(self):
        return 'query_non_empty_datetime()'

    def show_image(self, index):
        model = self.table_view.model()
        image_item = model.item(index.row(), self.get_image_column_index())
        if image_item:
            image_data = image_item.data()
            if image_data:
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.width(), self.image_label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))

    def get_qss(self):
        return """
        QWidget {
            background-color: #f5f5f5;
        }
        QTableView {
            background-color: #ffffff;
            color: #333333;
            gridline-color: #e0e0e0;
            border: 1px solid #d0d0d0;
            alternate-background-color: #f9f9f9;
        }
        QTableView::item {
            padding: 5px;
        }
        QTableView::item:hover {
            background-color: #e3f2fd;
        }
        QTableView::item:selected {
            background-color: #4a90e2;
            color: white;
        }
        QTableView::item:alternate {
            background-color: #f9f9f9;
        }
        QHeaderView::section {
            background-color: #e0e0e0;
            padding: 5px;
            border: 1px solid #d0d0d0;
        }
        QLabel {
            background-color: #ffffff;
            border: 1px solid #d0d0d0;
        }
        """

class RowNumberModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(4)  # 设置列数为4

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return '影片'
            elif section == 1:
                return '描述'
            elif section == 2:
                return '日期时间'
            elif section == 3:
                return '图片'
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        return super().data(index, role)