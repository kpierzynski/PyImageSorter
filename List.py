from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QListWidget, QListWidgetItem, QMessageBox, QInputDialog
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon

from ListElement import ListElement

from DataModels.Dir import Dir


class List(QWidget):
    categorySelected = Signal(Dir)
    newCategoryCreated = Signal(str)

    def __init__(self, listItems: list[Dir] = []):
        super().__init__()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.listView = QListWidget()
        self.listView.itemDoubleClicked.connect(self.onSelected)

        self.newCategoryBtn = QPushButton("New category")
        self.newCategoryBtn.setIcon(QIcon.fromTheme("folder-new"))
        self.newCategoryBtn.clicked.connect(self.onNewCategory)
        self.newCategoryBtn.setDisabled(True)

        self.mainLayout.addWidget(self.listView)
        self.mainLayout.addWidget(self.newCategoryBtn)
        self.setLayout(self.mainLayout)

        self.setList(listItems)

    def setList(self, listItems: list[Dir]):
        listItems.sort(key=lambda d: d.name.lower())

        self.list = listItems
        if len(self.list):
            self.newCategoryBtn.setDisabled(False)

        self.listView.clear()
        for entry in self.list:
            item = ListElement(entry)
            self.listView.addItem(item)

    def onSelected(self, item: ListElement):
        self.categorySelected.emit(item.dir)

    def onNewCategory(self):
        text, ok = QInputDialog.getText(
            self, "Create new category", "Input category name:")

        if ok and text:
            self.newCategoryCreated.emit(text)
