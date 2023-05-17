from os.path import basename, join, isdir, isfile
from os import listdir

from .File import File


class Dir:
    def __init__(self, path, progress_signal=None, thread=None):
        self.path = path
        self.name = basename(path)

        self.directories = []
        self.files = []

        items = listdir(path)

        total = len(items)
        if progress_signal:
            progress_signal.emit(0.0)

        for i, item in enumerate(items):
            if thread and thread.isInterruptionRequested():
                break

            itempath = join(path, item)

            if isdir(itempath):
                self.directories.append(Dir(itempath))
            elif isfile(itempath):
                f = File(itempath)
                if f.isImage:
                    self.files.append(f)

            if progress_signal:
                progress_signal.emit(i/total)

        if progress_signal:
            progress_signal.emit(1.0)

    @property
    def filesCount(self) -> int:
        return len(self.files)

    @property
    def directoriesCount(self) -> int:
        return len(self.directories)

    def __str__(self) -> str:
        return self.path
