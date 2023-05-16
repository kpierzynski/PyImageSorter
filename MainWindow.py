from PySide6.QtWidgets import QMainWindow, QToolBar, QFileDialog, QDockWidget, QVBoxLayout, QWidget, QUndoView, QPushButton, QHBoxLayout, QLabel, QMessageBox, QListWidget, QListWidgetItem, QSplitter, QFrame, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QUndoStack, QKeySequence, QUndoCommand, QAction, QScreen, QGuiApplication

from Viewer import Viewer
from List import List
from Toolbar import Toolbar

from tools import getFiles, getDirs, moveFile, createDirectory

from DataModels.Dir import Dir
from DataModels.File import File
from Commands.MoveFile import MoveFileCommand
from Commands.DeleteFile import DeleteFileCommand

from os.path import join
from os import getcwd


class MainWindow(QMainWindow):
    def __init__(self, title="MainWindow"):
        super().__init__()

        self.undoStack = QUndoStack()
        self.undoAction = self.undoStack.createUndoAction(self)
        self.undoAction.setIcon(QIcon.fromTheme('undo'))
        self.undoAction.triggered.connect(self.update)
        self.undoAction.setShortcut(QKeySequence.Undo)

        self.addAction(self.undoAction)

        self.directory = None
        self._index = -1

        self.initUI()
        self.initMenu()

    def initUI(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        self.setWindowTitle("PyImageSorter")
        self.resize(int(screen_geometry.width() * 0.8),
                    int(screen_geometry.height() * 0.8))

        self.setGeometry(
            (screen_geometry.width() * (1-0.8)/2),
            (screen_geometry.height() * (1-0.8)/2),
            self.width(),
            self.height()
        )

        self.toolbar = Toolbar(self)
        self.toolbar.delete.triggered.connect(self.handleFileRemove)
        self.toolbar.next.triggered.connect(self.nextIndex)
        self.toolbar.prev.triggered.connect(self.prevIndex)
        self.toolbar.addAction(self.undoAction)

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

    def handleFileRemove(self):
        try:
            self.undoStack.push(
                DeleteFileCommand(self.directory, self.file)
            )

            if self.index == self.directory.filesCount:
                self.index -= 1

            self.update()

        except Exception as e:
            print(e)
            QMessageBox(QMessageBox.Critical, 'Error occur',
                        f'Cannot remove image').exec()

    def handleDirectoryPick(self, directory: Dir):
        try:
            self.undoStack.push(
                MoveFileCommand(self.directory, self.file, directory)
            )

            if self.index == self.directory.filesCount:
                self.index -= 1

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
        if self.directory.filesCount <= 0:
            self.toolbar.lock()
        else:
            self.toolbar.unlock()

        if self.index < 0 and self.directory.filesCount > 0:
            self.index += 1

        self.updateStatusBar()
        self.updateDetails()

        if self.file:
            self.viewer.setImage(self.file)
        else:
            self.viewer.clear()

    def updateStatusBar(self):
        self.statusBar().showMessage(
            f"{self._index+1}/{self.directory.filesCount} {self.directory.path}", 0)

    def updateDetails(self):
        if not self.file:
            message = f"Select a file"
        else:
            message = f"File: {self.file.name}\nPath: {self.file.path}\nDate: {self.file.time}\nDimensions: {self.file.width}x{self.file.height}"

        self.details.setText(message)

    # do i need this?
    def updateList(self):
        pass

    @property
    def file(self) -> File:
        if not self.directory:
            return None

        if self.index < 0 or self.index >= self.directory.filesCount:
            return None

        return self.directory.files[self.index]

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        if not self.directory:
            return

        if self.directory.filesCount <= 0:
            self._index = -1
        else:
            self._index = (value % self.directory.filesCount)

        self.update()

    def nextIndex(self):
        self.index += 1

    def prevIndex(self):
        self.index -= 1

    def onHelp(self):
        QMessageBox(QMessageBox.Information, "Help",
                    "Created by kpierzynski\n\nVisit https://github.com/kpierzynski/PyImageSorter for further help.", parent=self).exec()

    def onExit(self):
        self.close()
