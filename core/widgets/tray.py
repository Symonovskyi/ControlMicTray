import logging
import sys

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QActionGroup, QAction

from core.styles import TrayIconStyles, BaseStyle
from core.events import EventBus

logger = logging.getLogger(__name__)


class TrayIcon(QSystemTrayIcon):

    def __init__(self, bus: EventBus):
        super().__init__()

        self.menu = QMenu()
        self._bus = bus

        # Styles
        self.tray_styles = TrayIconStyles(self)

        # For hadnling walkie mode features
        self.is_walkie = None
        self.is_muted = None

        # Setup UI and connect signals
        self.__initialize_main_menu()
        self.__setup_connections()

    def __initialize_main_menu(self):
        """Initialize menu items and connect signals."""
        # Microphone toggle
        self.toggle_mic = self.menu.addAction('Вкл.\\Выкл. микрофон')
        # Walkie-talkie mode toggle
        self.walkie_mic = self.menu.addAction('Вкл.\\Выкл. режим рации')

        self.menu.addSeparator()

        # Devices menu
        self.devices_menu = QMenu("Микрофоны", parent=self.menu)
        self.menu.addMenu(self.devices_menu)
        self.device_action_group = QActionGroup(self)
        self.device_action_group.setExclusive(True) # Только один может быть выбран

        # Settings
        self.settings_action = self.menu.addAction('Настройки')
        # About
        self.about_action = self.menu.addAction('О программе...')
        # Exit
        self.exit_action = self.menu.addAction('Выход')

        # Set menu and tooltip
        self.setContextMenu(self.menu)
        self.setToolTip('ControlMicTray')

    def __setup_connections(self):
        # Connect single click on tray icon
        self.activated.connect(self._on_tray_icon_click)

        self.toggle_mic.triggered.connect(self._toggler)
        self.toggle_mic.setCheckable(True)
        self.walkie_mic.triggered.connect(self._mode_switcher)
        self.walkie_mic.setCheckable(True)

        self._bus.shared.int_hotkey_toggle_mic.connect(self._on_tray_icon_click)

        self.settings_action.triggered.connect(
            lambda e: self._bus.shared.int_open_settings.emit()
        )
        self.about_action.triggered.connect(
            lambda e: self._bus.shared.int_open_about.emit()
        )
        self.exit_action.triggered.connect(sys.exit)

        # Подключаем сигнал группы (срабатывает при клике на ЛЮБОЙ экшен внутри нее)
        self.device_action_group.triggered.connect(self._on_device_selected)

        # Подписки на App Events от Оркестратора
        self._bus.shared.app_devices_list_updated.connect(self._rebuild_devices_menu)
        self._bus.shared.app_default_mic_updated.connect(self._sync_mic_with_os)

        self._bus.theme.tray_icon_change.connect(self._on_mic_changes)
        self._bus.theme.app_theme_changed.connect(self._on_theme_changed)
        self._bus.storage.app_initial_state_loaded.connect(self._on_initial_state_loaded)

    def _rebuild_devices_menu(self, devices: dict[str, str]):
        self.devices_menu.clear()

         # Очищаем группу от старых экшенов (предотвращает утечки памяти)
        for old_action in self.device_action_group.actions():
            self.device_action_group.removeAction(old_action)

        for dev_id, dev_name in devices.items():
            action = QAction(dev_name, self.devices_menu)
            action.setCheckable(True) # Включаем встроенные галочки Qt
            action.setData(dev_id)    # Сохраняем ID устройства внутри экшена
        
            self.device_action_group.addAction(action)
            self.devices_menu.addAction(action)

        # Updating icons
        self.tray_styles.update_tray_icons(self.is_muted, self.is_walkie)

    def _on_device_selected(self, action: QAction):
        """Слот срабатывает, когда пользователь кликает на любой микрофон"""
        # Галочка УЖЕ переставилась фреймворком (Оптимистичный UI)
        device_id = action.data()
        
        # Отправляем интент Оркестратору на реальную смену в ОС
        self._bus.shared.int_change_default_mic.emit(device_id)

    def _sync_mic_with_os(self, verified_device_id: str):
        """
        Вызывается Оркестратором.
        Применяется для подтверждения смены от ОС или для ОТКАТА (Rollback),
        если ОС отказалась менять микрофон.
        """
        for action in self.device_action_group.actions():
            if action.data() == verified_device_id:
                # Если галочка и так стоит - ничего не делаем
                if action.isChecked():
                    break

                # ВАЖНО: Блокируем сигналы группы! 
                # Иначе программный setChecked(True) вызовет triggered и породит бесконечный цикл.
                self.device_action_group.blockSignals(True)
                action.setChecked(True)
                self.device_action_group.blockSignals(False)
                break

    def _on_tray_icon_click(self, reason):
        """Handle single click on tray icon (only in normal mode)."""
        if reason == self.ActivationReason.Trigger and not self.is_walkie:
            muted = self.toggle_mic.isChecked()
            self.toggle_mic.setChecked(not muted)

            self._bus.shared.int_toggle_mic.emit(not muted)

    def _toggler(self):
        muted = self.toggle_mic.isChecked()
        self._bus.shared.int_toggle_mic.emit(muted)

    def _mode_switcher(self):
        """Switch between normal and walkie-talkie modes."""
        self._bus.shared.int_change_mode.emit(self.walkie_mic.isChecked())

    def _on_initial_state_loaded(self, data: dict):
        """Установка начального состояния при загрузке из БД."""
        self.is_walkie = data.get("walkie_status", False)
        self.is_muted = data.get("mic_status", False)

        # Обновляем чекбокс walkie в меню
        self._on_mic_changes(self.is_muted, self.is_walkie)

    def _on_theme_changed(self, palette: BaseStyle):
        self.tray_styles.set_styles(palette)
        self._on_mic_changes(self.is_muted, self.is_walkie)

    def _on_mic_changes(self, muted: bool, mode: bool):
        self.is_walkie = mode
        self.is_muted = muted
        self.tray_styles.update_tray_icons(not muted, mode)
