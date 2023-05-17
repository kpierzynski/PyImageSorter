from PySide6.QtWidgets import QProgressDialog
from PySide6.QtCore import Qt, Signal

from DirectoryLoader import DirectoryLoader
from DataModels.Dir import Dir


class Progress(QProgressDialog):
    finished = Signal(Dir)

    def __init__(self, directorypath, parent=None):
        super().__init__("Loading images...", "Cancel", 0, 100,
                         flags=Qt.WindowTitleHint | Qt.CustomizeWindowHint, parent=parent)

        self.directory = None

        self.setWindowTitle("Processing")
        self.setModal(True)
        self.setAutoClose(True)

        self.loader = DirectoryLoader(directorypath)

        self.canceled.connect(self._handleLoaderStopRequest)
        self.loader.progress.connect(self._handleValueUpdate)
        self.loader.done.connect(self._handleDirectoryResult)
        self.loader.finished.connect(self._handleDialogDone)

    def _handleValueUpdate(self, value):
        self.setValue(value * 100)

    def _handleLoaderStopRequest(self):
        self.loader.requestInterruption()

    def _handleDirectoryResult(self, directory):
        self.directory = directory

    def _handleDialogDone(self):
        if self.directory:
            self.finished.emit(self.directory)

    def start(self):
        self.show()
        self.loader.start()
