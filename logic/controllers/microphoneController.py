# Built-in modules and own classes.
from ctypes import POINTER, cast
from logic.controllers.interfaces.ipolicyconfig import IPolicyConfig, CLSID_PolicyConfigClient

# "pip install" modules.
from keyboard import is_pressed
from comtypes import CLSCTX_ALL, CLSCTX_INPROC_SERVER, COMObject, CoCreateInstance
from pycaw.pycaw import (AudioUtilities, IAudioEndpointVolume,
    IAudioEndpointVolumeCallback, IMMDeviceEnumerator)
from pycaw.utils import EDataFlow, DEVICE_STATE, CLSID_MMDeviceEnumerator, ERole



class MicrophoneController(AudioUtilities):
    '''
    This controller uses "pycaw" module to operate with microphone states.
    Initalizate connection to default microphone in system if any available.

    Attributes:
        - __mic (comtypes.POINTER(IAudioEndpointVolume)):
        system microphone instance.
    '''
    def __init__(self):
        self.__device_enumerator = CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator,
            CLSCTX_INPROC_SERVER)

        self.__default_mic = self.__device_enumerator.GetDefaultAudioEndpoint(
            EDataFlow.eCapture.value, ERole.eCommunications.value)
        self.__active_mic = cast(self.__default_mic.Activate(\
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None),\
                    POINTER(IAudioEndpointVolume))

    def get_all_sys_microphones(self):
        '''
        Returns dictionary of all system microphones.

        Returns:
            - dict: contains all system microphones.
              Ex.: {device_name (str): device((comtypes.POINTER(IAudioEndpointVolume))}.
        '''
        collection = self.__device_enumerator.EnumAudioEndpoints(
            EDataFlow.eCapture.value, DEVICE_STATE.ACTIVE.value
        )

        devices = {}
        count = collection.GetCount()
        # Add exception handling here.
        for i in range(count):
            dev = collection.Item(i)
            if dev is not None:
                device = AudioUtilities.CreateDevice(dev)
                devices.update({device.FriendlyName: device})

        return devices

    def get_microphone_by_name(self, name):
        '''
        Returns system microphone by its name.

        Parameters:
            - name (str): microphone name.

        Returns:
            - comtypes.POINTER(IAudioEndpointVolume): system microphone instance.
        '''
        microphones = self.get_all_sys_microphones()
        return microphones.get(name)

    def set_microphone_by_default(self, mic_name):
        '''
        Sets system microphone by its name as default.

        Parameters:
            - mic_name (str): microphone name.
        '''
        try:
            mic = self.get_microphone_by_name(mic_name)
            policy_config = CoCreateInstance(
                CLSID_PolicyConfigClient,
                IPolicyConfig,
                CLSCTX_ALL
            )
            policy_config.SetDefaultEndpoint(mic.id, ERole.eMultimedia.value)
            # policy_config.SetDefaultEndpoint(mic.id, EDataFlow.eCapture.value)
            policy_config.Release()

            self.__default_mic = self.__device_enumerator.GetDefaultAudioEndpoint(
                EDataFlow.eCapture.value, ERole.eMultimedia.value)
            self.__active_mic = cast(self.__default_mic.Activate(\
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None),\
                        POINTER(IAudioEndpointVolume))
        except:
            raise

    def is_mic_active(self, dev) -> bool:
        '''
        Returns True if microphone is active, False otherwise.

        Parameters:
            ...

        Returns:
            - bool: True if microphone is active, False otherwise.
        '''
        self.__default_mic = self.GetMicrophone()
        device = AudioUtilities.CreateDevice(dev).FriendlyName
        active_device = AudioUtilities.CreateDevice(self.__default_mic).FriendlyName
        return bool(device == active_device)

    def mute_mic(self):
        '''
        Mutes system microphone.
        '''
        self.__active_mic.SetMute(True, None)

    def unmute_mic(self):
        '''
        Unmutes system microphone.
        '''
        self.__active_mic.SetMute(False, None)

    def register_control_change_notify(self, callback):
        '''
        Registers callback for changing icons status on mic change status.
        '''
        self.__active_mic.RegisterControlChangeNotify(callback)

    @property
    def get_mic_status(self) -> bool:
        '''
        Returns True if mic is muted, False otherwise.
        '''
        return bool(self.__active_mic.GetMute())


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
