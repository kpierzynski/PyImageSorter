from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog, QLabel, QListWidget, QListWidgetItem
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem

from ListElement import ListElement

from DataModels.Dir import Dir


class List(QWidget):
    def __init__(self, listItems=[]):
        super().__init__()

        self.list = listItems

        self.mainLayout = QHBoxLayout()
        self.listView: QListWidget = QListWidget()
        self.listView.doubleClicked.connect(self.handleDoubleClick)

        self.setList(listItems)

        self.mainLayout.addWidget(self.listView)
        self.setLayout(self.mainLayout)

    def setList(self, listItems: list[Dir]):
        self.list = listItems

        for entry in self.list:
            widget = ListElement(entry)

            item = QListWidgetItem(self.listView)
            item.setSizeHint(widget.sizeHint())

            self.listView.addItem(item)
            self.listView.setItemWidget(item, widget)

    def handleDoubleClick(self, index):
        item = self.listView.itemFromIndex(index)
        widget = self.listView.itemWidget(item)

        print(widget)
