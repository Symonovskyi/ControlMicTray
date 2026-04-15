# src/adapters/audio/windows/api/constants.py

from ctypes import c_longlong
from enum import Enum
from comtypes import GUID

from src.adapters.audio.windows.api.structures import PROPERTYKEY


DEVPKEY_Device_FriendlyName = PROPERTYKEY()
DEVPKEY_Device_FriendlyName.fmtid = GUID("{a45c254e-df1c-4efd-8020-67d146a850e0}")
DEVPKEY_Device_FriendlyName.pid = 14

REFERENCE_TIME = c_longlong


class ERole(Enum):
    eConsole = 0
    eMultimedia = 1
    eCommunications = 2


class EDataFlow(Enum):
    eRender = 0
    eCapture = 1
    eAll = 2


class EAudioDeviceState(Enum):
    Active = 1
    Disabled = 2
    NotPresent = 4
    Unplugged = 8


class STGM(Enum):
    STGM_READ = 0
    STGM_WRITE = 1
    STGM_READWRITE = 2

class EEndpointHardwareSupport(Enum):
    EndpointHardwareSupportVolume = 1
    EndpointHardwareSupportMute = 2
    EndpointHardwareSupportMeter = 3
