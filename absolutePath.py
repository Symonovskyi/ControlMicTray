from sys import argv, executable
from os import path
from pathlib import Path

def get_base_path():
    """Get the base path, handling both normal Python and Nuitka onefile mode."""
    if hasattr(argv, 'frozen') or getattr(argv, 'frozen', False):
        # Nuitka onefile mode
        return Path(argv[0]).parent
    return Path(__file__).parent

def loadFile(file_name: str) -> str:
    return path.join(path.dirname(__file__), file_name)

def loadRealFile(file_name: str, level_down: bool = False) -> str:
    base_path = Path(argv[0]).parent if argv[0] else Path(executable).parent
    if level_down:
        return str(base_path.parent)
    else:
        return str(base_path / file_name)

def realWorkingDirectory(level_down: bool = False) -> str:
    base_path = Path(argv[0]).parent if argv[0] else Path(executable).parent
    if level_down:
        return str(base_path.parent)
    else:
        return str(base_path)