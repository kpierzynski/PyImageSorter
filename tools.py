from os.path import join, isfile, isdir, basename, exists
from os import listdir, rename, makedirs, remove

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

    return dir


def moveFile(file: File, directory: Dir) -> None:
    filename = basename(file.path)
    targetpath = join(directory.path, filename)

    if isfile(targetpath):
        raise Exception(f"Target file exists. Cannot move {filename} file.")
        return

    rename(file.path, targetpath)

    file.path = targetpath


def createDirectory(path: str) -> Dir | None:
    if exists(path):
        raise Exception(f"Directory {path} exists!")
        return

    makedirs(path)
    return Dir(path)


def removeFile(file: File) -> None:
    if not exists(file.path) or not isfile(file.path):
        raise Exception(
            f"Given path {file.path} does not exist or it is not a file.")
        return

    remove(file.path)
