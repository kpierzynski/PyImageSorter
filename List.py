from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QListWidget, QListWidgetItem, QMessageBox, QInputDialog
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem

from ListElement import ListElement
from QEasyList import QEasyList

from DataModels.Dir import Dir


class List(QWidget):
    categorySelected = Signal(Dir)
    newCategoryCreated = Signal(str)

    def __init__(self, listItems: list[Dir] = []):
        super().__init__()

        self.mainLayout = QVBoxLayout()
        self.listView = QEasyList()
        self.listView.selected.connect(self.onSelected)

        self.newCategoryBtn = QPushButton("New..")
        self.newCategoryBtn.clicked.connect(self.onNewCategory)
        self.newCategoryBtn.setDisabled(True)

        self.mainLayout.addWidget(self.newCategoryBtn)
        self.mainLayout.addWidget(self.listView)
        self.setLayout(self.mainLayout)

        self.setList(listItems)

    def setList(self, listItems: list[Dir]):
        listItems.sort(key=lambda d: d.name.lower())

        self.list = listItems
        if len(self.list):
            self.newCategoryBtn.setDisabled(False)

        self.listView.clearWidgets()
        for entry in self.list:
            widget = ListElement(entry)
            self.listView.addWidget(widget)

    def onSelected(self, widget: ListElement):
        self.categorySelected.emit(widget.getDir())

    def onNewCategory(self):
        text, ok = QInputDialog.getText(
            self, "Create new category", "Input category name:")

        if ok and text:
            self.newCategoryCreated.emit(text)
