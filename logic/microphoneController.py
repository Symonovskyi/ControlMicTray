# Built-in modules and own classes.
from ctypes import POINTER, cast
import logging

# "pip install" modules.
from keyboard import is_pressed
from comtypes import CLSCTX_ALL, COMObject
from pycaw.pycaw import (AudioUtilities, IAudioEndpointVolume,
    IAudioEndpointVolumeCallback)
from PyQt6.QtCore import QObject, pyqtSignal, Qt


# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MicrophoneController(AudioUtilities):
    '''
    This controller uses "pycaw" module to operate with microphone states.
    Initalizate connection to default microphone in system if any available.

    Attributes:
        - __mic (comtypes.POINTER(IAudioEndpointVolume)):
        system microphone instance.
    '''
    def __init__(self):
        try:
            self.__mic = cast(self.GetMicrophone().Activate(\
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None),\
                        POINTER(IAudioEndpointVolume))
        except Exception as e:
            logger.error(f"Failed to initialize microphone: {e}")
            raise

    def mute_mic(self):
        '''
        Mutes system microphone.
        '''
        try:
            self.__mic.SetMute(True, None)
        except Exception as e:
            logger.error(f"Failed to mute microphone: {e}")

    def unmute_mic(self):
        '''
        Unmutes system microphone.
        '''
        try:
            self.__mic.SetMute(False, None)
        except Exception as e:
            logger.error(f"Failed to unmute microphone: {e}")

    def register_control_change_notify(self, callback):
        '''
        Registers callback for changing icons status on mic change status.
        '''
        try:
            self.__mic.RegisterControlChangeNotify(callback)
        except Exception as e:
            logger.error(f"Failed to register callback: {e}")

    @property
    def get_mic_status(self) -> bool:
        '''
        Returns True if mic is muted, False otherwise.
        '''
        try:
            return bool(self.__mic.GetMute())
        except Exception as e:
            logger.error(f"Failed to get mic status: {e}")
            return True  # Безопасное значение по умолчанию (микрофон выключен)


class AudioSignals(QObject):
    volume_changed = pyqtSignal()
    mute_mic = pyqtSignal()


class CustomMicrophoneEndpointVolumeCallback(COMObject):
    '''
    Implements custom callback for microphone state changes.

    Parameters:
        - inst (QSystemTrayIcon): used for making a reference between classes,
        such as this and TrayIcon class.

    Attributes:
        - _com_interfaces_ (list): contains reference to
        IAudioEndpointVolumeCallback functionality from C language.
    '''
    _com_interfaces_ = [IAudioEndpointVolumeCallback]

    def __init__(self, tray_instance, db_intance):
        super().__init__()
        self.db = db_intance
        self.signals = AudioSignals()
        # Используем QueuedConnection для безопасного вызова из другого потока
        self.signals.volume_changed.connect(
            tray_instance.settings_win.settings_UI.NightTheme.clicked.emit,
            type=Qt.ConnectionType.QueuedConnection
        )
        self.signals.mute_mic.connect(
            tray_instance.mic.mute_mic,
            type=Qt.ConnectionType.QueuedConnection
        )

    def OnNotify(self, pNotify):
        '''
        Implements a callback itself.
        Instantly mutes mic if not pressing unmuting button, and app is in
        walkie-talkie mode.
        Calls change_icons_according_to_mic_status() from main TrayIcon class
        to change menu elements switchers and tray icon color when microphone
        state changes from "muted" to "unmuted" and conversely otherwise.
        '''
        try:
            # Получаем значения из БД безопасно (теперь потокобезопасно)
            walkie_status = self.db.walkie_status
            hotkey_walkie = self.db.hotkey_walkie

            # Проверяем режим рации и горячую клавишу
            if walkie_status and hotkey_walkie:
                try:
                    if not is_pressed(hotkey_walkie):
                        self.signals.mute_mic.emit()
                except Exception as e:
                    logger.error(f"Failed to check hotkey state: {e}")

            # Уведомляем об изменении громкости
            self.signals.volume_changed.emit()

        except Exception as e:
            logger.error(f"Critical error in OnNotify callback: {e}")

        return 0  # S_OK - важно вернуть код успеха
