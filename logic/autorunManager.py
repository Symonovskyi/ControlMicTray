import os
import sys
from pathlib import Path
from subprocess import call as cmd_exec

from absolutePath import loadRealFile


class AutorunManager:
    def __init__(self, exe_path: str | Path = None):
        """
        Initializes the AutorunManager.
        :param exe_path: Path to the original .exe file.
        """
        if exe_path is None:
            self.exe_path = Path(str(os.path.dirname(sys.argv[0]))) / "ControlMicTray.exe"
        else:
            self.exe_path = Path(loadRealFile(exe_path)).resolve()
        self.working_dir = self.exe_path.parent

    def get_startup_folder(self) -> Path:
        """Determines the current user's Autorun (Startup) folder on Windows."""
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise OSError("Cannot find APPDATA environment variable. Is this a Windows OS?")
        
        startup_path = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        
        if not startup_path.exists():
            raise FileNotFoundError(f"Startup folder not found at: {startup_path}")
            
        return startup_path

    def get_shortcut_path(self) -> Path:
        """Constructs and returns the expected Path to the .lnk file."""
        startup_folder = self.get_startup_folder()
        return startup_folder / f"{self.exe_path.stem}.lnk"

    def shortcut_exists(self) -> bool:
        """
        Determines if the shortcut already exists in the Autorun folder.
        :return: True if the .lnk file exists, False otherwise.
        """
        return self.get_shortcut_path().exists()

    def create_autorun_shortcut(self) -> None:
        """Creates a .lnk file in the Windows Startup folder pointing to the .exe file."""
        shortcut_path = self.get_shortcut_path()
        
        # We use the system TEMP folder to store the transient VBScript
        temp_dir = Path(os.environ.get("TEMP", self.working_dir))
        vbs_path = temp_dir / "create_shortcut_temp.vbs"
        
        vbs_script = (
            'Set ws = WScript.CreateObject("WScript.Shell")\n'
            f'Set link = ws.CreateShortcut("{shortcut_path}")\n'
            f'link.TargetPath = "{self.exe_path}"\n'
            f'link.WorkingDirectory = "{self.exe_path.parent}"\n'
            'link.Save\n'
        )
        
        if not self.shortcut_exists():
            vbs_path.write_text(vbs_script, encoding="utf-8")
            cmd_exec(f'cscript //nologo "{vbs_path}"')

            try:
                os.remove(vbs_path)
            except OSError:
                pass

    def remove_autorun_shortcut(self) -> bool:
        """
        Deletes the shortcut from the Autorun folder if it exists.
        :return: True if the shortcut was successfully deleted, False if it did not exist.
        """
        shortcut_path = self.get_shortcut_path()
        
        if shortcut_path.exists():
            try:
                os.remove(shortcut_path)
                return True
            except OSError as e:
                raise OSError(f"Failed to delete shortcut at {shortcut_path}: {e}")
                
        return False

# --- Usage Example ---
if __name__ == "__main__":
    exe_location = Path(str(os.path.dirname(sys.argv[0]))) / "app.exe"
    manager = AutorunManager(exe_path=exe_location)
    
    # 1. Check existence
    if manager.shortcut_exists():
        print("Shortcut already exists.")
    else:
        # 2. Create shortcut
        manager.create_autorun_shortcut()
        print(f"Shortcut created. Exists now: {manager.shortcut_exists()}")
    
    # 3. Remove shortcut
    was_removed = manager.remove_autorun_shortcut()
    if was_removed:
        print(f"Shortcut removed successfully. Exists now: {manager.shortcut_exists()}")