from PySide6.QtWidgets import QMainWindow, QFileDialog, QDockWidget, QVBoxLayout, QWidget, QUndoView, QPushButton, QHBoxLayout, QLabel, QMessageBox, QListWidget, QListWidgetItem, QSplitter, QFrame, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QUndoStack, QKeySequence, QUndoCommand, QAction

from Viewer import Viewer
from List import List

from tools import getFiles, getDirs, filterImages, moveFile, createDirectory

from DataModels.Dir import Dir
from DataModels.File import File
from Commands.MoveFile import MoveFileCommand

from os.path import join
from os import getcwd


class MainWindow(QMainWindow):
    def __init__(self, title="MainWindow"):
        super().__init__()

        self.undoStack = QUndoStack()
        self.undoAction = self.undoStack.createUndoAction(self)
        self.undoAction.triggered.connect(self.update)
        self.undoAction.setShortcut(QKeySequence.Undo)

        self.addAction(self.undoAction)

        self._index = -1

        self.initUI()
        self.initMenu()

    def initUI(self):
        self.resize(800, 600)

        self.undo_view = QUndoView(self.undoStack)
        self.undo_view.setEmptyLabel("No Undo/Redo operations")
        self.undo_view.setWindowTitle("Undo/Redo Stack")
        self.undo_view.setMinimumWidth(200)
        self.undo_view.setMaximumWidth(300)
        dock_widget = QDockWidget("Undo View")
        dock_widget.setWidget(self.undo_view)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

        self.viewer = Viewer()

        self.list = List()
        self.list.directoryPicked.connect(self.handleDirectoryPick)
        self.list.newCategoryCreated.connect(self.handleNewDirectory)

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

    def initMenu(self):
        menu = self.menuBar()

        fileMenu = menu.addMenu("File")
        menu.addAction("Help", self.onHelp)

        fileMenu.addAction("Open Directory", self.handleBrowse)
        fileMenu.addAction("Exit", self.onExit)

    def handleBrowse(self):
        directorypath = QFileDialog.getExistingDirectory(
            self, "Select Directory", getcwd())

        if not directorypath:
            return

        self.directory = Dir(directorypath)
        self.list.setList(self.directory.directories)
        self.index = 0

    def handleDirectoryPick(self, directory: Dir):
        try:
            self.undoStack.push(
                MoveFileCommand(self.directory, self.file, directory)
            )

            self.update()

        except Exception as e:
            print(e)
            QMessageBox(QMessageBox.Critical, 'Error occur',
                        f'Cannot move image to "{directory.name}", there is already file named "{self.file.name}"').exec()

    def handleNewDirectory(self, name: str):
        if not self.directory:
            return

        try:
            self.directory.directories.append(
                createDirectory(join(self.directory.path, name)))
            self.list.setList(self.directory.directories)
        except Exception as e:
            print(e)
            QMessageBox(QMessageBox.Critical, 'Error occur',
                        f'Cannot create "{categoryName}" category, it exists!').exec()

    def update(self):
        self.updateStatusBar()
        self.updateDetails()

        self.viewer.setImage(self.file)

    def updateStatusBar(self):
        self.statusBar().showMessage(
            f"{self._index+1}/{self.directory.filesCount} {self.directory.path}", 0)

    def updateDetails(self):
        self.details.setText(
            f"File: {self.file.name}\nPath: {self.file.path}\nDate: {self.file.time}\nDimensions: {self.file.width}x{self.file.height}")

    # do i need this?
    def updateList(self):
        pass

    @property
    def file(self) -> File:
        if not self.directory:
            return

        if self.index < 0 and self.index >= self.directory.filesCount:
            return

        return self.directory.files[self.index]

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        if not self.directory:
            return

        self._index = (value % self.directory.filesCount)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.index -= 1
        elif event.key() == Qt.Key_D:
            self.index += 1

    def onDirectoryPicked(self, path: str):
        pass

    def onHelp(self):
        QMessageBox(QMessageBox.Critical, "Help",
                    "Created by kpierzynski", parent=self).exec()

    def onExit(self):
        self.close()
