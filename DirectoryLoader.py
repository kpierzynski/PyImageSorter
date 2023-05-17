from PySide6.QtCore import QThread, Signal

from DataModels.Dir import Dir


class DirectoryLoader(QThread):
    progress = Signal(float)
    done = Signal(Dir)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        directory = Dir(self.path, progress_signal=self.progress, thread=self)

        if not self.isInterruptionRequested():
            self.done.emit(directory)
