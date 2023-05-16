from PySide6.QtGui import QUndoCommand

from DataModels.Dir import Dir
from DataModels.File import File

from tempfile import gettempdir, mkdtemp

from tools import moveFile


class DeleteFileCommand(QUndoCommand):
    def __init__(self, root: Dir, file: File):
        super().__init__()

        self.temp = Dir(mkdtemp(prefix="PyImageSorter", suffix="_temp"))

        self.root = root
        self.file = file

        self.setText(f"remove {file.name}")

    def undo(self):
        moveFile(self.file, self.root)

        self.root.files.insert(self.index, self.file)

    def redo(self):
        moveFile(self.file, self.temp)

        self.index = self.root.files.index(self.file)

        self.root.files.remove(self.file)
