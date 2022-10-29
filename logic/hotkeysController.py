# Built-in modules and own classes.
from database.databaseController import DatabaseController

# 'pip install' modules.
from PyQt6.QtCore import QObject, pyqtSignal
from keyboard import add_hotkey as kb_add_hotkey, remove_hotkey as kb_remove_hotkey


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
    db = DatabaseController()

    normal_mode_hotkey_signal = pyqtSignal()
    walkie_mode_on_hotkey_signal = pyqtSignal()
    walkie_mode_off_hotkey_signal = pyqtSignal()

    normal_hotkey_attr = None
    walkie_hotkey_on_attr = None
    walkie_hotkey_off_attr = None

    def register_normal_mode_hotkey(self):
        '''
        Registers hotkey for normal app mode using shortcuts from db.
        '''
        if not self.db.hotkey_mic == 'unmapped':
            self.normal_hotkey_attr = kb_add_hotkey(self.db.hotkey_mic,\
                self.normal_mode_hotkey_signal.emit)

    def register_walkie_mode_hotkey(self):
        '''
        Registers hotkey for walkie-talkie app mode using shortcuts from db.
        '''
        if not self.db.hotkey_walkie == 'unmapped':
            self.walkie_hotkey_on_attr = kb_add_hotkey(
                self.db.hotkey_walkie.upper(),\
                    self.walkie_mode_on_hotkey_signal.emit,\
                        trigger_on_release=False)
            self.walkie_hotkey_off_attr = kb_add_hotkey(
                self.db.hotkey_walkie.lower(),\
                    self.walkie_mode_off_hotkey_signal.emit,\
                        trigger_on_release=True)

    def re_register_normal_mode_hotkey(self):
        '''
        Removes actual registered hotkey for nomral app mode and registers
        new hotkey, using shortcut from db.
        '''
        try:
            kb_remove_hotkey(self.normal_hotkey_attr)
        except: pass
        self.register_normal_mode_hotkey()

    def re_register_walkie_mode_hotkey(self):
        '''
        Removes actual registered hotkeys for walkie-talkie app mode and
        registers new hotkeys, using shortcuts from db.
        '''
        try:
            kb_remove_hotkey(self.walkie_hotkey_off_attr)
            kb_remove_hotkey(self.walkie_hotkey_on_attr)
        except: pass
        self.register_walkie_mode_hotkey()

    def switch_hotkey_mode(self):
        '''
        Removes non-actual mode hotkey(s) and registers hotkey(s) for
        switched app mode.
        '''
        if self.db.walkie_status:
            kb_remove_hotkey(self.normal_hotkey_attr)
            self.register_walkie_mode_hotkey()
        else:
            kb_remove_hotkey(self.walkie_hotkey_off_attr)
            kb_remove_hotkey(self.walkie_hotkey_on_attr)
            self.register_normal_mode_hotkey()

    def unregister_normal_mode_hotkey(self):
        try:
            kb_remove_hotkey(self.normal_hotkey_attr)
        except: pass
        self.db.hotkey_mic = 'unmapped'

    def unregister_walkie_mode_hotkey(self):
        try:
            kb_remove_hotkey(self.walkie_hotkey_on_attr)
            kb_remove_hotkey(self.walkie_hotkey_off_attr)
        except: pass
        self.db.hotkey_walkie = 'unmapped'