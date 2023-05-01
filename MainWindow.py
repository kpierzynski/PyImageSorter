from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt
from Browser import Browser
from Viewer import Viewer
from List import List
from QEasyList import QEasyList

from tools import getFiles, getDirs, filterImages, moveFile, createDirectory

from DataModels.Dir import Dir
from os.path import join


class MainWindow(QMainWindow):
    def __init__(self, title="MainWindow"):
        super().__init__()
        self.resize(800, 600)

        self.createMenu()

        self.browser = Browser()
        self.browser.browse.connect(self.onDirectoryPicked)

        self.viewer = Viewer()

        self.list = List()
        self.list.categorySelected.connect(self.onCategorySelect)
        self.list.newCategoryCreated.connect(self.onNewCategoryCreation)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.browser)

        self.container = QHBoxLayout()
        self.container.addWidget(self.viewer, 1)
        self.container.addWidget(self.list, 0)

        self.mainLayout.addLayout(self.container)

        self.widget = QWidget()
        self.widget.setLayout(self.mainLayout)

        self.setCentralWidget(self.widget)

        self.files = []
        self._index = -1

    def onCategorySelect(self, directory: Dir):
        try:
            moveFile(self.file, directory)
            self.files.pop(self._index)
            self.index = self.index
        except Exception as e:
            QMessageBox(QMessageBox.Critical, 'Error occur',
                        f'Cannot move image to "{directory.name}", there is already file named "{self.file.name}"').exec()

    def onNewCategoryCreation(self, categoryName: str) -> None:
        if not self.path:
            return

        try:
            createDirectory(join(self.path, categoryName))
            self.list.setList(getDirs(self.path))

        except Exception as e:
            print(e)
            QMessageBox(QMessageBox.Critical, 'Error occur',
                        f'Cannot create "{categoryName}" category, it exists!').exec()

    @property
    def file(self):
        if self._index < 0 or self._index >= len(self.files):
            return None
        return self.files[self.index]

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if len(self.files) <= 0:
            self._index = -1
            return

        self._index = (value % len(self.files))

        self.viewer.setImage(self.file)
        self.statusBar().showMessage(
            f"{self._index}/{len(self.files)}: {self.file.path}", 0)
        return self._index

    def onDirectoryPicked(self, path: str):
        self.path = path
        self.files = filterImages(getFiles(path))
        self.list.setList(getDirs(path))
        self.index = 0

    def onSelectDirectory(self):
        self.browser.browsePath()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.index -= 1
        elif event.key() == Qt.Key_D:
            self.index += 1

    def onHelp(self):
        QMessageBox(QMessageBox.Critical, "Help",
                    "Created by kpierzynski").exec()

    def onExit(self):
        self.close()

    def createMenu(self):
        self.menu = [
            {
                "name": "File",
                "items": [
                    {
                        "name": "Open Directory",
                        "spacerAfter": True,
                        "action": self.onSelectDirectory
                    },
                    {
                        "name": "Exit",
                        "action": self.onExit
                    }
                ]
            },
            {
                "name": "Help",
                "action": self.onHelp
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
