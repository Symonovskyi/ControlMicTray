# Built-in modules and own classes.
from ctypes import POINTER, cast

# "pip install" modules.
from keyboard import is_pressed
from comtypes import CLSCTX_ALL, COMObject
from pycaw.pycaw import (AudioUtilities, IAudioEndpointVolume,
    IAudioEndpointVolumeCallback)


class MicrophoneController(AudioUtilities):
    '''
    This controller uses "pycaw" module to operate with microphone states.
    Initalizate connection to default microphone in system if any available.

    Attributes:
        - __mic (comtypes.POINTER(IAudioEndpointVolume)):
        system microphone instance.
    '''
    def __init__(self):
        self.__mic = cast(self.GetMicrophone().Activate(\
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None),\
                    POINTER(IAudioEndpointVolume))

    def mute_mic(self):
        '''
        Mutes system microphone.
        '''
        self.__mic.SetMute(True, None)

    def unmute_mic(self):
        '''
        Unmutes system microphone.
        '''
        self.__mic.SetMute(False, None)

    def register_control_change_notify(self, callback):
        '''
        Registers callback for changing icons status on mic change status.
        '''
        self.__mic.RegisterControlChangeNotify(callback)

    @property
    def get_mic_status(self) -> bool:
        '''
        Returns True if mic is muted, False otherwise.
        '''
        return bool(self.__mic.GetMute())


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

    def __init__(self, tray_instance):
        self.inst = tray_instance

    def OnNotify(self, pNotify):
        '''
        Implements a callback itself.
        Instantly mutes mic if not pressing unmuting button, and app is in
        walkie-talkie mode.
        Calls change_icons_according_to_mic_status() from main TrayIcon class
        to change menu elements switchers and tray icon color when microphone
        state changes from "muted" to "unmuted" and conversely otherwise.
        '''
        if self.inst.db.walkie_status and not is_pressed(self.inst.db.hotkey_walkie):
            self.inst.mic.mute_mic()

        self.inst.change_icons_according_to_mic_status()
