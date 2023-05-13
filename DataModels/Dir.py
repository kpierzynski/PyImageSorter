from os.path import basename, join, isdir, isfile
from os import listdir

from .File import File


class Dir:
    def __init__(self, path):
        self.path = path
        self.name = basename(path)

        self.directories = []
        self.files = []

        items = listdir(path)
        for item in items:
            itempath = join(path, item)

            if isdir(itempath):
                self.directories.append(Dir(itempath))
            elif isfile(itempath):
                f = File(itempath)
                if f.isImage:
                    self.files.append(f)

    @property
    def filesCount(self) -> int:
        return len(self.files)

    @property
    def directoriesCount(self) -> int:
        return len(self.directories)

    def __str__(self) -> str:
        return self.path
