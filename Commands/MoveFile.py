from PySide6.QtGui import QUndoCommand

from DataModels.Dir import Dir
from DataModels.File import File

from tools import getFiles, getDirs, filterImages, moveFile, createDirectory


class MoveFileCommand(QUndoCommand):
    def __init__(self, path: str, file: File, directory: Dir):
        super().__init__()

        self.path = path
        self.file = file
        self.directory = directory

        self.setText(f"{file.name} and {directory.path}")

    # undo move file
    def undo(self):
        print("undoing")
        moveFile(self.file, Dir(self.path))

    # move file logic
    def redo(self):
        moveFile(self.file, self.directory)
