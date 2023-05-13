from PySide6.QtGui import QUndoCommand

from DataModels.Dir import Dir
from DataModels.File import File

from tools import getFiles, getDirs, filterImages, moveFile, createDirectory


class MoveFileCommand(QUndoCommand):
    def __init__(self, root: Dir, file: File, directory: Dir):
        super().__init__()

        self.root = root
        self.file = file
        self.directory = directory

        self.setText(f"{file.name} and {directory.path}")

    # undo move file
    def undo(self):
        moveFile(self.file, self.root)
        self.directory.files.remove(self.file)

        self.root.files.insert(self.index, self.file)

    # move file logic
    def redo(self):
        moveFile(self.file, self.directory)

        self.index = self.root.files.index(self.file)

        self.root.files.remove(self.file)
        self.directory.files.append(self.file)
