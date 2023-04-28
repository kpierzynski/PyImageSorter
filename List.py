from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog, QLabel, QListWidget, QListWidgetItem
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem

from ListElement import ListElement
from QEasyList import QEasyList

from DataModels.Dir import Dir


class List(QWidget):
    categorySelected = Signal(Dir)

    def __init__(self, listItems: list[Dir] = []):
        super().__init__()
        self.setList(listItems)

        self.mainLayout = QHBoxLayout()
        self.listView = QEasyList()
        self.listView.selected.connect(self.onSelected)

        self.mainLayout.addWidget(self.listView)
        self.setLayout(self.mainLayout)

    def setList(self, listItems: list[Dir]):
        self.list = listItems

        for entry in self.list:
            widget = ListElement(entry)
            self.listView.addWidget(widget)

    def onSelected(self, widget: ListElement):
        self.categorySelected.emit(widget.getDir())
