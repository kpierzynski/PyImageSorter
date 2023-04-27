from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Signal

from DataModels.Dir import Dir


class ListElement(QWidget):
    def __init__(self, sourceDir: Dir):
        super().__init__()

        self.mainLayout = QHBoxLayout()

        self.nameLabel = QLabel(sourceDir.name)

        self.mainLayout.addWidget(self.nameLabel)

        self.setLayout(self.mainLayout)

    def __str__(self) -> str:
        return f'ListElement: {self.nameLabel.text()}'
