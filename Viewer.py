from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QLabel
from PySide6.QtGui import QPixmap, QPainter, Qt

from DataModels import File


class Viewer(QWidget):
    def __init__(self, file: File = None):
        super().__init__()

        self.view = QGraphicsView(self)
        self.view.setAlignment(Qt.AlignCenter)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.view)

        if file:
            self.setImage(self.file)

    def clear(self):
        self.scene.clear()

    def setImage(self, file: File):
        if not file:
            print("No corrent path was given.")
            return

        self.file = file

        self.pixmap = QPixmap(self.file.path)
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)

        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
