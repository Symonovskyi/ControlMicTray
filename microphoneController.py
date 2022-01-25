# Built-in modules and own classes.
from ctypes import POINTER, cast
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# "pip install" modules.
from comtypes import CLSCTX_ALL


class MicrophoneController(AudioUtilities):
    '''
    Class that uses "pycaw" module to operate with microphone.

    Methods:
    - MuteMic() - mutes the mic.
    - UnMuteMic() - unmutes the mic.

    Properties:
    - getMic - holds the actual microphone instance.
    - getDevicesCount - holds microphones count that are active in system.
    - getMicMuteState - holds the actual state of mic: muted or not.
    '''
    def __init__(self):
        interface = self.GetMicrophone().Activate(IAudioEndpointVolume._iid_,\
            CLSCTX_ALL, None)
        self.mic = cast(interface, POINTER(IAudioEndpointVolume))

    def MuteMic(self):
        self.mic.SetMute(True, None)

    def UnMuteMic(self):
        self.mic.SetMute(False, None)

    @property
    def getMic(self):
        return self.mic

    @property
    def getDevicesCount(self):
        #TODO: get the real count of microphones only.
        return len(self.GetAllDevices())

    @property
    def getMicMuteState(self):
        return self.mic.GetMute()