from sys import argv
from os import path
from pathlib import Path

def loadFile(file_name: str) -> str:
    return path.join(path.dirname(__file__), file_name)

def loadRealFile(file_name: str, level_down: bool = False) -> str:
    if level_down:
        return str(Path(path.join(path.dirname(argv[0]), file_name)).parent)
    else:
        return path.join(path.dirname(argv[0]), file_name)

def realWorkingDirectory(level_down: bool = False) -> str:
    if level_down:
        return str(Path(path.dirname(argv[0])).parent)
    else:
        return str(path.dirname(argv[0]))