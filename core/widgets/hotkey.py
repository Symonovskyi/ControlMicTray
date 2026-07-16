from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QKeySequence


QT_MOUSE_MAP = {
    Qt.MouseButton.MiddleButton: 'middle',
    Qt.MouseButton.XButton1: 'mouse4',
    Qt.MouseButton.XButton2: 'mouse5'
}

QT_KEY_MAP = {
    Qt.Key.Key_Control: "ctrl", Qt.Key.Key_Shift: "shift",
    Qt.Key.Key_Alt: "alt", Qt.Key.Key_Meta: "windows",
    Qt.Key.Key_Return: "enter", Qt.Key.Key_Enter: "enter",
    Qt.Key.Key_Escape: "esc", Qt.Key.Key_ScrollLock: "scroll_lock",
    Qt.Key.Key_Print: "print screen", Qt.Key.Key_SysReq: "print screen",
    Qt.Key.Key_Insert: "insert", Qt.Key.Key_Delete: "del",
    Qt.Key.Key_Backspace: "backspace", Qt.Key.Key_PageUp: "page up",
    Qt.Key.Key_PageDown: "page down", Qt.Key.Key_CapsLock: "caps lock",
    Qt.Key.Key_NumLock: "num lock", Qt.Key.Key_Up: "up",
    Qt.Key.Key_Down: "down", Qt.Key.Key_Left: "left",
    Qt.Key.Key_Right: "right", Qt.Key.Key_Space: "space",
    Qt.Key.Key_Clear: "clear", Qt.Key.Key_End: "end",
    Qt.Key.Key_Home: "home", Qt.Key.Key_Minus: "-", Qt.Key.Key_Plus: "+"
}


class HotkeyButton(QPushButton):
    hotkey_updated = pyqtSignal(str)

    def __init__(self, mode_name: str, tooltip: str, parent=None):
        super().__init__("Кликните для назначения...", parent)
        self.setObjectName(f"HotkeyBtn{mode_name}")
        self.setToolTip(tooltip)
        self.setCheckable(True)
        
        self._current_hotkey = "unmapped"
        self._held_modifiers = set()
        self._held_main_key = None

        self.toggled.connect(self._on_toggled)

    def set_hotkey(self, hotkey: str):
        self._current_hotkey = hotkey if hotkey else self._current_hotkey
        self.setText(self._current_hotkey)

    def _on_toggled(self, checked: bool):
        if checked:
            self.setText("Нажмите клавишу мыши\клавиатуры...")
            self._held_modifiers.clear()
            self._held_main_key = None
            self.grabKeyboard() 
        else:
            self.releaseKeyboard()
            self.setText(self._current_hotkey.upper())

    # --- mouse processing ---
    def mousePressEvent(self, e: QMouseEvent):

        try:
            btn = e.button()
            if not self.isChecked():
                super().mousePressEvent(e)
            
            if btn == Qt.MouseButton.LeftButton or btn == Qt.MouseButton.RightButton:
                self._finalize_hotkey("unmapped")
                return

            if btn in QT_MOUSE_MAP.keys():
                # ЗАЩИТА ОТ СМЕШИВАНИЯ: Если зажаты модификаторы клавиатуры - сброс
                self._held_modifiers = set()
                self._held_main_key = None
                mapped_btn = QT_MOUSE_MAP[btn]
                self._finalize_hotkey(mapped_btn)
        except Exception as e:
            print(e)

    # --- keyboard processing ---
    def keyPressEvent(self, e: QKeyEvent):
        if not self.isChecked() or e.isAutoRepeat():
            super().keyPressEvent(e)

        key = e.key()
        
        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_Escape):
            self._finalize_hotkey("unmapped")
            return

        # ЗАЩИТА ОТ РАСКЛАДКИ (Cyrillic -> English)
        if key in QT_KEY_MAP:
            mapped_key = QT_KEY_MAP[key]
        else:
            # QKeySequence всегда возвращает английскую букву для базовых клавиш!
            mapped_key = QKeySequence(key).toString().lower()
            if not mapped_key: 
                mapped_key = e.text().lower() # Фолбэк на крайний случай
        
        if key in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            self._held_modifiers.add(mapped_key)
        else:
            self._held_main_key = mapped_key

        temp_str = self._build_hotkey_string(self._held_main_key or "...")
        self.setText(temp_str.upper())

    def keyReleaseEvent(self, e: QKeyEvent):
        if not self.isChecked() or e.isAutoRepeat():
            super().keyReleaseEvent(e)

        if not self._held_main_key:
            self._finalize_hotkey("unmapped")
            return
        else:
            final_str = self._build_hotkey_string(self._held_main_key)
            self._finalize_hotkey(final_str)

    # --- misc methods ---
    def _build_hotkey_string(self, main_key: str) -> str:
        parts = list(self._held_modifiers)
        parts.sort(key=lambda x: {"ctrl": 1, "shift": 2, "alt": 3, "windows": 4}.get(x, 99))
        if main_key and main_key != "...":
            parts.append(main_key)
        return "+".join(parts)

    def _finalize_hotkey(self, hotkey_str: str):
        if hotkey_str == "" or hotkey_str == "...":
            hotkey_str = "unmapped"
        self._current_hotkey = hotkey_str
        self.setChecked(False) 
        self.hotkey_updated.emit(self._current_hotkey)