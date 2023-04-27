from os.path import basename


class File:
    def __init__(self, path):
        self.path = path

        self.name = basename(path)
