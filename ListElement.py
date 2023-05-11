from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QListWidgetItem
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

from DataModels.Dir import Dir


class ListElement(QListWidgetItem):
    def __init__(self, sourceDir: Dir):
        super().__init__(QIcon.fromTheme("folder"), sourceDir.name)
        self.dir = sourceDir
