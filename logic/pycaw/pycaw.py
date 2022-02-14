"""
Python wrapper around the Core Audio Windows API.
"""
# import here all newly split up modules,
# to keep backwards compatibility

# flake8: noqa
# yes, the imports are unused

from logic.pycaw.api.audioclient import IAudioClient, ISimpleAudioVolume
from logic.pycaw.api.audioclient.depend import WAVEFORMATEX
from logic.pycaw.api.audiopolicy import (
    IAudioSessionControl, IAudioSessionControl2, IAudioSessionEnumerator,
    IAudioSessionEvents, IAudioSessionManager, IAudioSessionManager2)
from logic.pycaw.api.endpointvolume import (IAudioEndpointVolume,
                                      IAudioEndpointVolumeCallback,
                                      IAudioMeterInformation)
from logic.pycaw.api.endpointvolume.depend import (AUDIO_VOLUME_NOTIFICATION_DATA,
                                             PAUDIO_VOLUME_NOTIFICATION_DATA)
from logic.pycaw.api.mmdeviceapi import (IMMDevice, IMMDeviceCollection,
                                   IMMDeviceEnumerator)
from logic.pycaw.api.mmdeviceapi.depend import IPropertyStore
from logic.pycaw.api.mmdeviceapi.depend.structures import (PROPERTYKEY, PROPVARIANT,
                                                     PROPVARIANT_UNION)
from logic.pycaw.constants import (AUDCLNT_SHAREMODE, DEVICE_STATE, STGM,
                             AudioDeviceState, EDataFlow, ERole)
from logic.pycaw.utils import AudioDevice, AudioSession, AudioUtilities
