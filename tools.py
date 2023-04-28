from os.path import join, isfile, isdir, basename
from os import listdir, rename

from PIL import Image

from DataModels.File import File
from DataModels.Dir import Dir


def getFiles(path: str) -> list[File]:
    files = []

    for file in listdir(path):
        filePath = join(path, file)

        if isfile(filePath):
            files.append(File(filePath))

    return files


def getDirs(path: str) -> list[Dir]:
    dirs = []

    for _dir in listdir(path):
        dirPath = join(path, _dir)

        if isdir(dirPath):
            dirs.append(Dir(dirPath))

    return dirs


def filterImages(files: list[File]) -> list[File]:
    def is_image(filePath):
        try:
            img = Image.open(filePath)
            img.verify()
            return True
        except:
            return False

    return [x for x in files if is_image(x.path)]


def _moveFile(filePath: str, targetDir: str) -> None:
    fileName = basename(filePath)
    targetPath = join(targetDir, fileName)

    if isfile(targetPath):
        raise Exception(f"Target file exists. Cannot move {fileName} file.")
    else:
        rename(filePath, targetPath)


def moveFile(file: File, direct: Dir) -> None:
    _moveFile(file.path, direct.path)
