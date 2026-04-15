from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent, QMouseEvent


QT_MOUSE_MAP = {
    Qt.MouseButton.MiddleButton: 'middle',
    Qt.MouseButton.XButton1: 'x',
    Qt.MouseButton.XButton2: 'x2'
}

QT_KEY_MAP = {
    Qt.Key.Key_Control: "ctrl",
    Qt.Key.Key_Shift: "shift",
    Qt.Key.Key_Alt: "alt",
    Qt.Key.Key_Meta: "windows",
    Qt.Key.Key_Return: "enter",
    Qt.Key.Key_Enter: "enter",
    Qt.Key.Key_Escape: "esc",
    Qt.Key.Key_ScrollLock: "scroll_lock",
    Qt.Key.Key_Print: "print screen",
    Qt.Key.Key_SysReq: "print screen",
    Qt.Key.Key_Insert: "insert",
    Qt.Key.Key_Delete: "del",
    Qt.Key.Key_Backspace: "backspace",
    Qt.Key.Key_PageUp: "page up",
    Qt.Key.Key_PageDown: "page down",
    Qt.Key.Key_CapsLock: "caps lock",
    Qt.Key.Key_NumLock: "num lock",
    Qt.Key.Key_Up: "up",
    Qt.Key.Key_Down: "down",
    Qt.Key.Key_Left: "left",
    Qt.Key.Key_Right: "right",
    Qt.Key.Key_Space: "space",
    Qt.Key.Key_Clear: "clear",
    Qt.Key.Key_End: "end",
    Qt.Key.Key_Home: "home",
    Qt.Key.Key_NumLock: "num_lock",
    Qt.Key.Key_Minus: "-",
    Qt.Key.Key_Plus: "+"
}


class HotkeyButton(QPushButton):
    hotkey_updated = pyqtSignal(str)

    def __init__(self, mode_name: str, tooltip: str, parent=None):
        super().__init__("Кликните для назначения...", parent)
        self.setObjectName(f"HotkeyBtn{mode_name}")
        self.setToolTip(tooltip)
        self.setCheckable(True) # checked signal as "grab" mode
        
        self._current_hotkey = "unmapped"
        self._held_modifiers = set()
        self._held_main_key = None

        self.toggled.connect(self._on_toggled)

    def set_hotkey(self, hotkey: str):
        self._current_hotkey = hotkey if hotkey else "unmapped"
        self.setText(self._current_hotkey.upper())

    # enabling "grab" mode
    def _on_toggled(self, checked: bool):
        if checked:
            self.setText("Нажмите клавишу...")
            self._held_modifiers.clear()
            self._held_main_key = None
            self.grabKeyboard()
        else:
            self.releaseKeyboard()
            self.setText(self._current_hotkey.upper())

    # --- mouse processing ---
    def mousePressEvent(self, e: QMouseEvent):
        if not self.isChecked():
            # Если мы не в режиме записи, обычный клик левой кнопкой включает запись
            if e.button() == Qt.MouseButton.LeftButton:
                super().mousePressEvent(e)
            return

        # Если в режиме записи нажата кнопка мыши
        btn = e.button()
        
        # ЛКМ и ПКМ обычно используются для отмены/очистки
        if btn == Qt.MouseButton.LeftButton or btn == Qt.MouseButton.RightButton:
            self._finalize_hotkey("unmapped")
            return

        if btn in QT_MOUSE_MAP:
            # 1. ЗАЩИТА: Если главная клавиша клавиатуры уже зажата - сбрасываем ввод
            if self._held_main_key is not None and self._held_main_key in list(QT_MOUSE_MAP.keys()):
                self._finalize_hotkey("unmapped")
                return

            mapped_btn = QT_MOUSE_MAP[btn]
            result = self._build_hotkey_string(mapped_btn)
            self._finalize_hotkey(result)

    # --- keyboard processing ---
    def keyPressEvent(self, e: QKeyEvent):
        if not self.isChecked():
            return super().keyPressEvent(e)

        if e.isAutoRepeat(): # Игнорируем спам события при долгом удержании
            return

        key = e.key()
        
        # Очистка хоткея (Backspace, Delete, Escape)
        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_Escape):
            self._finalize_hotkey("unmapped")
            return

        # Если это модификатор - добавляем в набор
        mapped_key = QT_KEY_MAP.get(Qt.Key(key), e.text().lower())
        
        if key in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            self._held_modifiers.add(mapped_key)
        else:
            self._held_main_key = mapped_key

        # Динамически обновляем текст на кнопке (например, показываем "ctrl + ...")
        temp_str = self._build_hotkey_string(self._held_main_key or "...")
        self.setText(temp_str.upper())

    def keyReleaseEvent(self, e: QKeyEvent):
        if not self.isChecked():
            return super().keyReleaseEvent(e)

        if e.isAutoRepeat():
            return

        # Если пользователь отпустил клавишу, но основная клавиша (буква/цифра/мышь)
        # так и не была нажата (в _held_modifiers есть данные, а в _held_main_key - пусто)
        if not self._held_main_key:
            self._finalize_hotkey("unmapped")
            return

        # Фиксация по отпусканию любой клавиши (если основная уже задана)
        final_str = self._build_hotkey_string(self._held_main_key)
        self._finalize_hotkey(final_str)


    # --- misc methods ---
    def _build_hotkey_string(self, main_key: str) -> str:
        """Собирает строку вида 'ctrl+shift+k'"""
        parts = list(self._held_modifiers)
        # Сортируем модификаторы для консистентности (alt+ctrl -> ctrl+alt)
        parts.sort(key=lambda x: {"ctrl": 1, "shift": 2, "alt": 3, "windows": 4}.get(x, 99))
        
        if main_key and main_key != "...":
            parts.append(main_key)
            
        return "+".join(parts)

    def _finalize_hotkey(self, hotkey_str: str):
        """Сохраняет бинд, отжимает кнопку и эмиттит сигнал в Оркестратор"""
        if hotkey_str == "" or hotkey_str == "...":
            hotkey_str = "unmapped"
            
        self._current_hotkey = hotkey_str
        self.setChecked(False) # Это автоматически вернет текст и выключит grabKeyboard
        self.hotkey_updated.emit(self._current_hotkey)
