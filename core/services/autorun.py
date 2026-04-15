import os
import sys
from pathlib import Path
from subprocess import call as cmd_exec

from core.services.storage import StorageService
from core.events import EventBus


class AutorunService:
    def __init__(self, bus: EventBus, db: StorageService):
        """Initializes the AutorunManager."""
        self.__exe_path = Path(str(os.path.dirname(sys.argv[0]))) / "ControlMicTray.exe"
        self.__working_dir = self.__exe_path.parent

        self._bus = bus
        self._db = db

        # connecting signals (commands) to slots
        self._bus.system.int_toggle_autorun.connect(self.toggle_autorun_handler)

    def __get_startup_folder(self) -> Path:
        """Determines the current user's Autorun (Startup) folder on Windows."""
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise OSError("Cannot find APPDATA environment variable. Is this a Windows OS?")
        
        startup_path = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        
        if not startup_path.exists():
            raise FileNotFoundError(f"Startup folder not found at: {startup_path}")
            
        return startup_path

    def __get_shortcut_path(self) -> Path:
        """Constructs and returns the expected Path to the .lnk file."""
        startup_folder = self.__get_startup_folder()
        return startup_folder / f"{self.__exe_path.stem}.lnk"

    def _create_autorun_shortcut(self) -> None:
        """Creates a .lnk file in the Windows Startup folder pointing to the .exe file."""
        shortcut_path = self.__get_shortcut_path()
        
        # We use the system TEMP folder to store the transient VBScript
        temp_dir = Path(os.environ.get("TEMP", self.__working_dir))
        vbs_path = temp_dir / "create_shortcut_temp.vbs"
        
        vbs_script = (
            'Set ws = WScript.CreateObject("WScript.Shell")\n'
            f'Set link = ws.CreateShortcut("{shortcut_path}")\n'
            f'link.TargetPath = "{self.__exe_path}"\n'
            f'link.WorkingDirectory = "{self.__exe_path.parent}"\n'
            'link.Save\n'
        )

        if not shortcut_path.exists():
            vbs_path.write_text(vbs_script, encoding="utf-8")
            cmd_exec(f'cscript //nologo "{vbs_path}"')

            try:
                os.remove(vbs_path)
            except OSError:
                pass

    def _remove_autorun_shortcut(self) -> bool:
        """
        Deletes the shortcut from the Autorun folder if it exists.
        :return: True if the shortcut was successfully deleted, False if it did not exist.
        """
        shortcut_path = self.__get_shortcut_path()
        
        if shortcut_path.exists():
            try:
                os.remove(shortcut_path)
                return True
            except OSError as e:
                raise OSError(f"Failed to delete shortcut at {shortcut_path}: {e}")
                
        return False

    # Slot
    def toggle_autorun_handler(self, state: bool):
        self._db.enable_program = int(state)
        if state:
            self._create_autorun_shortcut()
        else:
            self._remove_autorun_shortcut()
        
        self._bus.system.app_autorun_state_changed.emit(state)
