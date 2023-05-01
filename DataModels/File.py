from os.path import basename, getctime
import datetime

from PIL import Image


class File:
    def __init__(self, path):
        self.path = path

        self.name = basename(path)

        if self._isImage():
            self.isImage = True

            with Image.open(self.path) as img:
                self.width, self.height = img.size
                time = getctime(self.path)
                time = datetime.datetime.fromtimestamp(
                    time).strftime('%Y-%m-%d %H:%M:%S')

                self.time = time

            print(self.width, self.height, self.time)

    def _isImage(self) -> bool:
        try:
            with Image.open(self.path) as img:
                img.verify()
            return True
        except:
            return False
