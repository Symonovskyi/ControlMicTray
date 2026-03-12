# Built-in modules and own classes.
import logging
from database.databaseController import DatabaseController

# 'pip install' modules.
from PyQt6.QtCore import QObject, pyqtSignal
from keyboard import add_hotkey as kb_add_hotkey, remove_hotkey as kb_remove_hotkey

logger = logging.getLogger(__name__)


class HotkeysManager(QObject):
    '''
    Implements hotkey manager functionality.

    Attributes:
        - db (DatabaseController): for getting hotkeys shortcuts from database.
        - normal_mode_hotkey_signal (pyqtSignal): Qt custom signal for normal
        mode hotkey.
        - walkie_mode_on_hotkey_signal (pyqtSignal): Qt custom signal for
        walkie-talkie mode hotkey. Used when user using walkie mode and
        holds hotkey so mic gets unmuted.
        - walkie_mode_off_hotkey_signal (pyqtSignal): Qt custom signal for
        walkie-talkie mode hotkey. Used when user using walkie mode and
        releases hotkey so mic gets muted.
        - normal_hotkey_attr (None | keyboard.KeyboardEvent): handles reference
        to normal hotkey keyboard event.
        - walkie_hotkey_on_attr (None | keyboard.KeyboardEvent): handles
        reference to "walkie hotkey on" keyboard event.
        - walkie_hotkey_off_attr (None | keyboard.KeyboardEvent): handles
        reference to "walkie hotkey off" keyboard event.
    '''

    normal_mode_hotkey_signal = pyqtSignal()
    walkie_mode_on_hotkey_signal = pyqtSignal()
    walkie_mode_off_hotkey_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Создаём экземпляр БД для каждого экземпляра класса
        self.db = DatabaseController()
        
        self.normal_hotkey_attr = None
        self.walkie_hotkey_on_attr = None
        self.walkie_hotkey_off_attr = None

    def register_normal_mode_hotkey(self):
        '''
        Registers hotkey for normal app mode using shortcuts from db.
        '''
        try:
            hotkey = self.db.hotkey_mic
            if hotkey and hotkey != 'unmapped':
                self.normal_hotkey_attr = kb_add_hotkey(
                    hotkey,
                    self.normal_mode_hotkey_signal.emit
                )
                logger.debug(f"Registered normal mode hotkey: {hotkey}")
        except Exception as e:
            logger.error(f"Failed to register normal mode hotkey: {e}")
            self.normal_hotkey_attr = None

    def register_walkie_mode_hotkey(self):
        '''
        Registers hotkey for walkie-talkie app mode using shortcuts from db.
        '''
        try:
            hotkey = self.db.hotkey_walkie
            if hotkey and hotkey != 'unmapped':
                self.walkie_hotkey_on_attr = kb_add_hotkey(
                    hotkey.upper(),
                    self.walkie_mode_on_hotkey_signal.emit,
                    trigger_on_release=False
                )
                self.walkie_hotkey_off_attr = kb_add_hotkey(
                    hotkey.lower(),
                    self.walkie_mode_off_hotkey_signal.emit,
                    trigger_on_release=True
                )
                logger.debug(f"Registered walkie mode hotkey: {hotkey}")
        except Exception as e:
            logger.error(f"Failed to register walkie mode hotkey: {e}")
            self.walkie_hotkey_on_attr = None
            self.walkie_hotkey_off_attr = None

    def _safe_remove_hotkey(self, hotkey_attr, hotkey_name=""):
        """Безопасное удаление горячей клавиши с логированием."""
        if hotkey_attr is not None:
            try:
                kb_remove_hotkey(hotkey_attr)
                logger.debug(f"Removed hotkey: {hotkey_name}")
            except Exception as e:
                logger.warning(f"Failed to remove hotkey {hotkey_name}: {e}")
            except OSError as e:
                # Игнорируем ошибки, если горячая клавиша уже удалена
                logger.debug(f"Hotkey {hotkey_name} was already removed or unavailable: {e}")

    def re_register_normal_mode_hotkey(self):
        '''
        Removes actual registered hotkey for nomral app mode and registers
        new hotkey, using shortcut from db.
        '''
        self._safe_remove_hotkey(self.normal_hotkey_attr, "normal_mode")
        self.normal_hotkey_attr = None
        self.register_normal_mode_hotkey()

    def re_register_walkie_mode_hotkey(self):
        '''
        Removes actual registered hotkeys for walkie-talkie app mode and
        registers new hotkeys, using shortcuts from db.
        '''
        self._safe_remove_hotkey(self.walkie_hotkey_off_attr, "walkie_off")
        self._safe_remove_hotkey(self.walkie_hotkey_on_attr, "walkie_on")
        self.walkie_hotkey_on_attr = None
        self.walkie_hotkey_off_attr = None
        self.register_walkie_mode_hotkey()

    def switch_hotkey_mode(self):
        '''
        Removes non-actual mode hotkey(s) and registers hotkey(s) for
        switched app mode.
        '''
        try:
            if self.db.walkie_status:
                # Переключение в режим рации
                self._safe_remove_hotkey(self.normal_hotkey_attr, "normal_mode")
                self.normal_hotkey_attr = None
                self.register_walkie_mode_hotkey()
            else:
                # Переключение в обычный режим
                self._safe_remove_hotkey(self.walkie_hotkey_off_attr, "walkie_off")
                self._safe_remove_hotkey(self.walkie_hotkey_on_attr, "walkie_on")
                self.walkie_hotkey_on_attr = None
                self.walkie_hotkey_off_attr = None
                self.register_normal_mode_hotkey()
        except Exception as e:
            logger.error(f"Failed to switch hotkey mode: {e}")

    def unregister_normal_mode_hotkey(self):
        try:
            self._safe_remove_hotkey(self.normal_hotkey_attr, "normal_mode")
            self.normal_hotkey_attr = None
        except Exception as e:
            logger.error(f"Failed to unregister normal mode hotkey: {e}")
        finally:
            self.db.hotkey_mic = 'unmapped'

    def unregister_walkie_mode_hotkey(self):
        try:
            self._safe_remove_hotkey(self.walkie_hotkey_on_attr, "walkie_on")
            self._safe_remove_hotkey(self.walkie_hotkey_off_attr, "walkie_off")
        except Exception as e:
            logger.error(f"Failed to unregister walkie mode hotkey: {e}")
        finally:
            self.walkie_hotkey_on_attr = None
            self.walkie_hotkey_off_attr = None
            self.db.hotkey_walkie = 'unmapped'
