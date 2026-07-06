import logging
import keyboard
import mouse

from core.events import EventBus


class HotkeyService:
    mouse_keys = {'middle': 'middle', 'mouse4': 'x', 'mouse5': 'x2'}

    def __init__(self, bus: EventBus):
        self._bus = bus

        self.__mic_hotkey_obj = None
        
        # Для мыши в режиме рации нам нужно хранить два хука (на нажатие и отпускание)
        self.__walkie_hotkey_obj = None
        self.__walkie_mouse_press_obj = None
        self.__walkie_mouse_release_obj = None

        self.__is_mouse_toggle = False
        self.__is_mouse_walkie = False

        self._bus.shared.cmd_bind_hotkeys.connect(self.switch_hotkey_handler)

    def _parse_hotkey(self, hotkey: str):
        parts = hotkey.split('+')
        return parts[-1], parts[:-1]

    # --- Toggle Mode ---
    def __register_toggle_hotkey(self, hotkey: str):
        if not hotkey or hotkey == 'unmapped':
            self.__mic_hotkey_obj = None
            self._bus.shared.answ_bind_hotkeys.emit(False, None)
            return

        trigger, modifiers = self._parse_hotkey(hotkey)

        try:
            if trigger in self.mouse_keys:
                # МЫШЬ
                lib_btn = self.mouse_keys[trigger]
                self.__mic_hotkey_obj = mouse.on_button(
                    callback=lambda: self._bus.shared.int_toggle_mic.emit(), 
                    buttons=(lib_btn,),
                    types=(mouse.DOWN,)
                )
                self.__is_mouse_toggle = True
            else:
                # КЛАВИАТУРА
                self.__mic_hotkey_obj = keyboard.add_hotkey(
                    hotkey=hotkey,
                    callback=lambda: self._bus.shared.int_toggle_mic.emit(),
                )
                self.__is_mouse_toggle = False
                
            self._bus.shared.answ_bind_hotkeys.emit(False, hotkey) # Успех
            
        except ValueError as e:
            logging.error(f"Неизвестный хоткей '{hotkey}': {e}")
            self._bus.shared.answ_bind_hotkeys.emit(False, None) # Ошибка

    def __unregister_toggle_hotkey(self):
        if self.__mic_hotkey_obj:
            if self.__is_mouse_toggle:
                try: mouse.unhook(self.__mic_hotkey_obj)
                except Exception: pass
            else:
                try: keyboard.remove_hotkey(self.__mic_hotkey_obj)
                except Exception: pass
            self.__mic_hotkey_obj = None

    # --- Walkie-Talkie Mode ---
    def __register_walkie_hotkey(self, hotkey: str):
        if not hotkey or hotkey == 'unmapped':
            self.__walkie_hotkey_obj = None
            self._bus.shared.answ_bind_hotkeys.emit(True, None)
            return

        trigger, modifiers = self._parse_hotkey(hotkey)

        try:
            if trigger in self.mouse_keys:
                # МЫШЬ (Т.к. модификаторы запрещены, on_button работает идеально)
                lib_btn = self.mouse_keys[trigger]
                
                self.__walkie_mouse_press_obj = mouse.on_button(
                    callback=lambda: self._bus.shared.int_walkie_press.emit(),
                    buttons=(lib_btn,), types=(mouse.DOWN,)
                )
                self.__walkie_mouse_release_obj = mouse.on_button(
                    callback=lambda: self._bus.shared.int_walkie_release.emit(),
                    buttons=(lib_btn,), types=(mouse.UP,)
                )
                self.__is_mouse_walkie = True
            else:
                # КЛАВИАТУРА
                self.__walkie_hotkey_obj = keyboard.hook_key(
                    key=trigger, # Используем только триггер
                    keydown_callback=lambda: self._bus.shared.int_walkie_press.emit(),
                    keyup_callback=lambda: self._bus.shared.int_walkie_release.emit(),
                )
                self.__is_mouse_walkie = False
            
            self._bus.shared.answ_bind_hotkeys.emit(True, hotkey) # Успех
            
        except ValueError as e:
            logging.error(f"Неизвестный хоткей '{hotkey}': {e}")
            self._bus.shared.answ_bind_hotkeys.emit(True, None) # Ошибка

    def __unregister_walkie_hotkey(self):
        if self.__is_mouse_walkie:
            try:
                if self.__walkie_mouse_press_obj: mouse.unhook(self.__walkie_mouse_press_obj)
                if self.__walkie_mouse_release_obj: mouse.unhook(self.__walkie_mouse_release_obj)
            except Exception: pass
            self.__walkie_mouse_press_obj = None
            self.__walkie_mouse_release_obj = None
        else:
            if self.__walkie_hotkey_obj:
                try: keyboard.unhook(self.__walkie_hotkey_obj)
                except Exception: pass
                self.__walkie_hotkey_obj = None

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