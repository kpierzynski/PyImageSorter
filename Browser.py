from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog, QLabel
from PySide6.QtCore import Signal
import os


class Browser(QWidget):
    browse = Signal(str)

    def __init__(self):
        super().__init__()

        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.browseClick)

        self.pathLabel = QLabel()
        self.pathLabel.setText("Select directory first")

        self.mainLayout = QHBoxLayout()

        self.mainLayout.addWidget(self.browseButton, 1)
        self.mainLayout.addWidget(self.pathLabel, 9)
        self.setLayout(self.mainLayout)

    def setPath(self, path):
        self.pathLabel.setText(path)

    def browsePath(self):
        self.browseClick()

    def browseClick(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", os.getcwd())

        if not directory:
            return

        self.setPath(directory)
        self.browse.emit(directory)
