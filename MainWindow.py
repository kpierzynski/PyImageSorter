from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from Browser import Browser
from Viewer import Viewer
from List import List
from QEasyList import QEasyList

from tools import getFiles, getDirs, filterImages, moveFile

from DataModels.Dir import Dir


class MainWindow(QMainWindow):
    def __init__(self, title="MainWindow"):
        super().__init__()
        self.resize(800, 600)

        self.createMenu()

        self.browser = Browser()
        self.browser.browse.connect(self.directoryPicked)

        self.viewer = Viewer()

        self.list = List()
        self.list.categorySelected.connect(self.onCategorySelect)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.browser)

        self.container = QHBoxLayout()
        self.container.addWidget(self.viewer, 1)
        self.container.addWidget(self.list, 0)

        self.mainLayout.addLayout(self.container)

        self.widget = QWidget()
        self.widget.setLayout(self.mainLayout)

        self.setCentralWidget(self.widget)

        self._index = -1

    def onCategorySelect(self, directory: Dir):
        moveFile(self.file, directory)
        # file moved, but need to update self.files or/and self.index

    def dupa(self, widget):
        print(widget.text())

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, newIndex: int):
        self._index = (newIndex % len(self.files))
        self.file = self.files[self._index]

        self.viewer.setImagePath(self.file.path)
        self.statusBar().showMessage(f'{self.index} {self.file.name}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.index -= 1
        elif event.key() == Qt.Key_D:
            self.index += 1

    def directoryPicked(self, path: str):
        self.files = filterImages(getFiles(path))
        self.list.setList(getDirs(path))

        self.index = 0

    def selectDirectory(self):
        self.browser.browsePath()

    def exit(self):
        self.close()

    def createMenu(self):
        self.menu = [
            {
                "name": "File",
                "items": [
                    {
                        "name": "Open Directory",
                        "spacerAfter": True,
                        "action": self.selectDirectory
                    },
                    {
                        "name": "Exit",
                        "action": self.exit
                    }
                ]
            },
            {
                "name": "Help",
            }
        ]

        def createMenuTree(menu, tree):
            for item in tree:
                if 'items' in item:
                    item['object'] = menu.addMenu(item["name"])
                    createMenuTree(item['object'], item['items'])
                else:
                    item['object'] = menu.addAction(item['name'])

                    if "action" in item:
                        item['object'].triggered.connect(item['action'])

                if 'spacerAfter' in item:
                    if item['spacerAfter']:
                        menu.addSeparator()

        menuBar = self.menuBar()
        createMenuTree(menuBar, self.menu)
