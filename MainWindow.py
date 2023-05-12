from PySide6.QtWidgets import QMainWindow, QDockWidget, QVBoxLayout, QWidget, QUndoView, QPushButton, QHBoxLayout, QLabel, QMessageBox, QListWidget, QListWidgetItem, QSplitter, QFrame, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QUndoStack, QKeySequence, QUndoCommand, QAction
from Browser import Browser
from Viewer import Viewer
from List import List

from tools import getFiles, getDirs, filterImages, moveFile, createDirectory

from DataModels.Dir import Dir
from DataModels.File import File
from Commands.MoveFile import MoveFileCommand

from os.path import join


class MainWindow(QMainWindow):
    def __init__(self, title="MainWindow"):
        super().__init__()
        self.resize(800, 600)

        self.createMenu()

        self.undoStack = QUndoStack()
        self.undoAction = self.undoStack.createUndoAction(self)
        self.undoAction.setShortcut(QKeySequence.Undo)

        self.addAction(self.undoAction)

        self.undo_view = QUndoView(self.undoStack)
        self.undo_view.setEmptyLabel("No Undo/Redo operations")
        self.undo_view.setWindowTitle("Undo/Redo Stack")
        self.undo_view.setMinimumWidth(200)
        self.undo_view.setMaximumWidth(300)
        dock_widget = QDockWidget("Undo View")
        dock_widget.setWidget(self.undo_view)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

        self.viewer = Viewer()
        self.browser = Browser()
        self.browser.browse.connect(self.onDirectoryPicked)

        self.list = List()
        self.list.categorySelected.connect(self.onCategorySelect)
        self.list.newCategoryCreated.connect(self.onNewCategoryCreation)

        self.detailsFrame = QFrame()
        self.detailsLayout = QVBoxLayout()
        self.detailsFrame.setLayout(self.detailsLayout)

        self.details = QTextEdit()
        self.details.setReadOnly(True)
        col = self.palette().placeholderText().color()
        self.details.setTextColor(col)

        self.splitterH = QSplitter(Qt.Horizontal)
        self.splitterH.addWidget(self.list)
        self.splitterH.addWidget(self.viewer)
        self.splitterH.setStretchFactor(0, 0)
        self.splitterH.setStretchFactor(1, 1)

        self.splitterV = QSplitter(Qt.Vertical)
        self.splitterV.addWidget(self.splitterH)
        self.splitterV.addWidget(self.details)
        self.splitterV.setStretchFactor(0, 1)
        self.splitterV.setStretchFactor(1, 0)

        self.setCentralWidget(self.splitterV)

        self.files = []
        self._index = -1

    def onCategorySelect(self, directory: Dir):
        try:
            self.undoStack.push(MoveFileCommand(
                self.path, self.file, directory))
            self.files.pop(self._index)
            self.index = self.index
        except Exception as e:
            print(e)
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
    def file(self) -> File:
        if self._index < 0 or self._index >= len(self.files):
            return None

        file = self.files[self.index]
        return file

    @property
    def index(self) -> int:
        return self._index

    def updateStatusBar(self):
        self.statusBar().showMessage(
            f"{self._index+1}/{len(self.files)} {self.path}", 0)

    @index.setter
    def index(self, value: int) -> int:

        if len(self.files) <= 0:
            self._index = -1
            self.viewer.clear()
            self.details.clear()

            self.updateStatusBar()
            return self._index

        self._index = (value % len(self.files))
        self.updateStatusBar()

        self.viewer.setImage(self.file)
        self.details.setText(
            f"File: {self.file.name}\nPath: {self.file.path}\nDate: {self.file.time}\nDimensions: {self.file.width}x{self.file.height}")

        return self._index

    def onDirectoryPicked(self, path: str):
        self.path = path
        self.files = filterImages(getFiles(path))
        self.list.setList(getDirs(path))
        self.index = 0
        self.updateStatusBar()

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
