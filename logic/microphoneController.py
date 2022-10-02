# Built-in modules and own classes.
from ctypes import POINTER, cast
from pycaw.pycaw import (AudioUtilities, IAudioEndpointVolume,
                         IAudioEndpointVolumeCallback)

# "pip install" modules.
from comtypes import CLSCTX_ALL, COMObject


class MicrophoneController(AudioUtilities):
    '''
    Class that uses "pycaw" module to operate with microphone.

    Methods:
    - mute_mic() - mutes the mic.
    - unmute_mic() - unmutes the mic.

    Properties:
    - get_devices_count - holds microphones count that are active in system.
    - get_mic_muted_state - holds the actual state of mic: muted or not.
    '''

    def __init__(self):
        interface = self.GetMicrophone(
            ).Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.mic = cast(interface, POINTER(IAudioEndpointVolume))

    def mute_mic(self):
        self.mic.SetMute(True, None)

    def unmute_mic(self):
        self.mic.SetMute(False, None)

    def register_control_change_notify(self, callback):
        self.mic.RegisterControlChangeNotify(callback)

    @property
    def get_devices_count(self):
        # TODO: get the real count of microphones only.
        ...

    @property
    def get_mic_status(self):
        return self.mic.GetMute()


class CustomAudioEndpointVolumeCallback(COMObject):
    _com_interfaces_ = [IAudioEndpointVolumeCallback]

    def __init__(self, qinstance):
        self.inst = qinstance

    def OnNotify(self, pNotify):
        self.inst.change_icons_according_to_status()
