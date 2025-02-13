# coding=utf-8
import sys
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsSimpleTextItem
from PyQt6.QtCore import QPointF

app = QApplication(sys.argv)

scene = QGraphicsScene()
scene.setSceneRect(0, 0, 400, 400)
# scene.setSceneRect(-200, -200, 400, 400)
# scene.setSceneRect(-400, -400, 400, 400)

textItem = QGraphicsSimpleTextItem()
textItem.setText("我爱PyQt")
textItem.setPos(scene.sceneRect().left(), scene.sceneRect().top())

scene.addItem(textItem)
view = QGraphicsView(scene)
# view.resize(300, 300)
# view.resize(400, 400)
view.resize(1000, 1000)
view.show()

print(f"视图坐标(0, 0)-->场景坐标{(view.mapToScene(0, 0).x(), view.mapToScene(0, 0).y())}")
print(f"场景坐标(0.0, 0.0)-->视图坐标{(view.mapFromScene(0, 0).x(), view.mapFromScene(0, 0).y())}")
topLeftPoint = QPointF(scene.sceneRect().topLeft())
print(f"场景左上角{(topLeftPoint.x(), topLeftPoint.y())}-->视图坐标{(view.mapFromScene(topLeftPoint.x(), topLeftPoint.y()).x(),view.mapFromScene(topLeftPoint.x(), topLeftPoint.y()).y())}")
sys.exit(app.exec())