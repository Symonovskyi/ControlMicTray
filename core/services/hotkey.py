from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSystemTrayIcon

import keyboard
import mouse

from core.events import EventBus


class HotkeyService:
    """
    Service for application hotkeys.
    
    Supports two modes:
    - Normal mode: single hotkey toggle for microphone
    - Walkie-talkie mode: press-and-hold hotkey for microphone
    """

    mouse_keys = {
        Qt.MouseButton.MiddleButton: 'middle',
        Qt.MouseButton.XButton1: 'x',
        Qt.MouseButton.XButton2: 'x2'
    }

    def __init__(self, bus: EventBus):
        self.__mic_hotkey_obj = None
        self.__walkie_hotkey_obj = None

        self._bus = bus

        self.__mic_hotkey_obj = None
        self.__walkie_hotkey_obj = None

        # Флаги для понимания, из какой библиотеки удалять хук
        self.__is_mouse_toggle = False
        self.__is_mouse_walkie = False

        self._bus.shared.cmd_bind_hotkeys.connect(self.switch_hotkey_handler)

    def _parse_hotkey(self, hotkey: str):
        """Разделяет строку на модификаторы и главный триггер."""
        parts = hotkey.split('+')
        trigger = parts[-1]
        modifiers = parts[:-1]
        return trigger, modifiers

    # --- Toggle Mode ---
    def __register_toggle_hotkey(self, hotkey: str):
        if hotkey == '' or hotkey == 'unmapped':
            self.__mic_hotkey_obj = None
            self._bus.shared.answ_bind_hotkeys.emit(False, None)
            return

        trigger, modifiers = self._parse_hotkey(hotkey)

        if trigger in self.mouse_keys:
            hotkey = self.mouse_keys[trigger]
            
            # def mouse_toggle_cb():
            #     # Проверка $O(1) модификаторов в памяти
            #     if all(keyboard.is_pressed(mod) for mod in modifiers):
            #         self._bus.shared.int_toggle_mic.emit()

            self.__mic_hotkey_obj = mouse.on_button(
                callback=lambda: self._bus.shared.int_hotkey_toggle_mic.emit(
                    QSystemTrayIcon.ActivationReason.Trigger
                ), 
                buttons=(hotkey,),
                types=(mouse.DOWN,)
            )
            self.__is_mouse_toggle = True
        else:
            # Для клавиатуры библиотека сама умеет парсить модификаторы из строки
            self.__mic_hotkey_obj = keyboard.add_hotkey(
                hotkey=hotkey,
                callback=lambda: self._bus.shared.int_hotkey_toggle_mic.emit(
                    QSystemTrayIcon.ActivationReason.Trigger
                ),
            )
            self.__is_mouse_toggle = False

        self._bus.shared.answ_bind_hotkeys.emit(False, hotkey) # Mode: toggle (False)

    def __unregister_toggle_hotkey(self):
        if self.__mic_hotkey_obj:
            if self.__is_mouse_toggle:
                try:
                    mouse.unhook(self.__mic_hotkey_obj)
                except Exception:
                    pass
            else:
                try:
                    keyboard.remove_hotkey(self.__mic_hotkey_obj)
                except Exception:
                    pass
            self.__mic_hotkey_obj = None

    # --- Walkie-Talkie Mode ---
    def __register_walkie_hotkey(self, hotkey: str):
        if hotkey == '' or hotkey == 'unmapped':
            self.__walkie_hotkey_obj = None
            self._bus.shared.answ_bind_hotkeys.emit(True, None)
            return

        trigger, modifiers = self._parse_hotkey(hotkey)

        if trigger in self.mouse_keys:
            hotkey = self.mouse_keys[trigger]
            
            # def mouse_walkie_cb(event):
            #     # Фильтруем только события нашей кнопки (игнорируем движения мыши)
            #     if getattr(event, 'button', None) == lib_btn:
            #         if event.event_type == 'down':
            #             if all(keyboard.is_pressed(mod) for mod in modifiers):
            #                 self._bus.shared.int_walkie_press.emit()
            #         elif event.event_type == 'up':
            #             self._bus.shared.int_walkie_release.emit()

            # self.__walkie_hotkey_obj = mouse.hook(mouse_walkie_cb)

            self.__walkie_hotkey_obj_press = mouse.on_button(
                callback=lambda e: self._bus.shared.int_walkie_press.emit(),
                buttons=(hotkey,), types=(mouse.DOWN,)
            )

            self.__walkie_hotkey_obj_release = mouse.on_button(
                callback=lambda e: self._bus.shared.int_walkie_release.emit(),
                buttons=(hotkey,), types=(mouse.UP,)
            )

            self.__is_mouse_walkie = True
            
        else:
            # def kb_walkie_cb(event):
            #     if event.event_type == keyboard.KEY_DOWN:
            #         if all(keyboard.is_pressed(mod) for mod in modifiers):
            #             self._bus.shared.int_walkie_press.emit()
            #     elif event.event_type == keyboard.KEY_UP:
            #         self._bus.shared.int_walkie_release.emit()

            self.__walkie_hotkey_obj = keyboard.hook_key(
                key=hotkey,
                keydown_callback=lambda: self._bus.shared.int_walkie_press.emit(),
                keyup_callback=lambda: self._bus.shared.int_walkie_release.emit(),
            )
            self.__is_mouse_walkie = False
        
        self._bus.shared.answ_bind_hotkeys.emit(False, hotkey) # Mode: toggle (False)

    def __unregister_walkie_hotkey(self):
        if self.__is_mouse_walkie:
            try:
                mouse.unhook(self.__walkie_hotkey_obj_press)
                mouse.unhook(self.__walkie_hotkey_obj_release)
            except Exception:
                pass
        else:
            try:
                keyboard.unhook(self.__walkie_hotkey_obj)
            except Exception:
                pass
            self.__walkie_hotkey_obj = None
            self.__walkie_hotkey_obj_press = None
            self.__walkie_hotkey_obj_release = None


    def switch_hotkey_handler(self, walkie_enabled: bool, hotkey: str):
        if not hotkey or hotkey in ('', 'Del', 'Backspace', 'unmapped'):
            hotkey = 'unmapped'

        if walkie_enabled:
            self.__unregister_toggle_hotkey()
            self.__register_walkie_hotkey(hotkey)
        else:
            self.__unregister_walkie_hotkey()
            self.__register_toggle_hotkey(hotkey)

    def cleanup(self):
        self.__unregister_toggle_hotkey()
        self.__unregister_walkie_hotkey()
