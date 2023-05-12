from os.path import join, isfile, isdir, basename, exists
from os import listdir, rename, makedirs

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
    return [x for x in files if x.isImage]


def moveFile(file: File, directory: Dir) -> None:
    filename = basename(file.path)
    targetpath = join(directory.path, filename)

    if isfile(targetpath):
        raise Exception(f"Target file exists. Cannot move {filename} file.")
        return

    rename(file.path, targetpath)

    file.path = targetpath
    directory.filesCount += 1


def createDirectory(path: str) -> Dir | None:
    if exists(path):
        raise Exception(f"Directory {path} exists!")
        return

    makedirs(path)
    return Dir(path)
