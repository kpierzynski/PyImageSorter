from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Signal

from DataModels.Dir import Dir


class ListElement(QWidget):
    def __init__(self, sourceDir: Dir):
        super().__init__()
        self.dir = sourceDir

        self.mainLayout = QHBoxLayout()

        self.nameLabel = QLabel(f'{self.dir.name}')

        self.mainLayout.addWidget(self.nameLabel)

        self.setLayout(self.mainLayout)

    def getDir(self) -> Dir:
        return self.dir

    def __str__(self) -> str:
        return f'ListElement: {self.nameLabel.text()}'
