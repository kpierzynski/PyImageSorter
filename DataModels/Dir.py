from os.path import basename
from os import walk


class Dir:
    def __init__(self, path):
        self.path = path
        self.name = basename(path)

        _, _, files = next(walk(path))
        self.filesCount = len(files)

    def __str__(self) -> str:
        return f'Directory: {self.name}, path: {self.path}'
