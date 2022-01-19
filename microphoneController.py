
from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL, CLSCTX_INPROC_SERVER, CoCreateInstance, GUID
from pycaw.pycaw import AudioUtilities as aUtils, IAudioEndpointVolume,\
    IMMDeviceEnumerator, EDataFlow, ERole


IID_Empty = GUID(
    '{00000000-0000-0000-0000-000000000000}')

CLSID_MMDeviceEnumerator = GUID(
    '{BCDE0395-E52F-467C-8E3D-C4579291692E}')


class MicrophoneController(aUtils):
    '''
    Class that uses "pycaw" module to operate with microphone.

    Methods:
    - MuteMic() - mutes the mic.
    - UnMuteMic() - unmutes the mic.

    Properties:
    - GetDevicesCount - holds microphones count that are active in system.
    - GetMicMuteState - holds the actual state of mic: muted or not.
    - GetMic - holds the actual microphone instance.
    '''
    def __init__(self):
        mic_device = self.GetMicrophone()
        interface = mic_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,\
            None)
        self.mic = cast(interface, POINTER(IAudioEndpointVolume))

    @staticmethod
    def GetMicrophone():
        """
        get the microphone (1st capture + multimedia) device
        """
        deviceEnumerator = CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator, CLSCTX_INPROC_SERVER)
        microphone = deviceEnumerator.GetDefaultAudioEndpoint(
                    EDataFlow.eCapture.value, ERole.eMultimedia.value)
        return microphone

    #TODO: get the real count of microphones only.
    @property
    def GetDevicesCount(self):
        return len(aUtils.GetAllDevices())

    @property
    def GetMicMuteState(self):
        return self.mic.GetMute()

    @property
    def GetMic(self):
        return self.mic

    def MuteMic(self):
        self.mic.SetMute(True, None)

    def UnMuteMic(self):
        self.mic.SetMute(False, None)