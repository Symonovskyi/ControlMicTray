from os import path, environ

def loadFile(file_name: str) -> str:
    return path.join(environ.get("_MEIPASS2", path.abspath(".")), file_name)
