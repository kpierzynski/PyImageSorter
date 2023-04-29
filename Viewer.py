from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPixmap, QPainter, Qt


class Viewer(QWidget):
    def __init__(self, path=""):
        super().__init__()
        self.path = path

        self.view = QGraphicsView(self)
        self.view.setAlignment(Qt.AlignCenter)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.view)

        self.setImagePath(self.path)

    def setImagePath(self, path):
        if not path:
            print("No corrent path was given.")
            return

        self.path = path
        self.pixmap = QPixmap(self.path)
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)

        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
