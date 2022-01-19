
from ctypes import POINTER, cast
from pycaw.constants import CLSID_MMDeviceEnumerator
from pycaw.pycaw import AudioUtilities as aUtils, IAudioEndpointVolume,\
    IMMDeviceEnumerator, EDataFlow, ERole

from comtypes import CLSCTX_ALL, CLSCTX_INPROC_SERVER, CoCreateInstance


class MicrophoneController(aUtils):
    '''
    Class that uses "pycaw" module to operate with microphone.

    Methods:
    - getMicDevice() - staticmethod - allows to get microphone in 
    inactivated state.
    - MuteMic() - mutes the mic.
    - UnMuteMic() - unmutes the mic.

    Properties:
    - getMic - holds the actual activated microphone instance.
    - getDevicesCount - holds microphones count that are active in system.
    - getMicMuteState - holds the actual state of mic: muted or not.
    '''
    def __init__(self):
        interface = self.getMicDevice().Activate(IAudioEndpointVolume._iid_,\
            CLSCTX_ALL, None)
        self.mic = cast(interface, POINTER(IAudioEndpointVolume))

    @staticmethod
    def getMicDevice():
        deviceEnumerator = CoCreateInstance(
            CLSID_MMDeviceEnumerator, IMMDeviceEnumerator, CLSCTX_INPROC_SERVER)
        microphone = deviceEnumerator.GetDefaultAudioEndpoint(
            EDataFlow.eCapture.value, ERole.eMultimedia.value)
        return microphone

    def MuteMic(self):
        self.mic.SetMute(True, None)

    def UnMuteMic(self):
        self.mic.SetMute(False, None)

    @property
    def getMic(self):
        return self.mic

    #TODO: get the real count of microphones only.
    @property
    def getDevicesCount(self):
        return len(self.GetAllDevices())

    @property
    def getMicMuteState(self):
        return self.mic.GetMute()