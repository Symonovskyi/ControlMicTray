#!/bin/python3

# This is a slimmed down version of the pycaw module.
# https://github.com/AndreMiras/pycaw/blob/develop/pycaw/pycaw.py

import sys, comtypes, ctypes
from enum import Enum
from ctypes import HRESULT, POINTER, Structure, Union, \
    c_uint32, c_longlong, c_float
from ctypes.wintypes import BOOL, VARIANT_BOOL, WORD, DWORD, \
    UINT, LONG, ULARGE_INTEGER, LPWSTR, LPCWSTR
from comtypes import IUnknown, GUID, COMMETHOD
from comtypes.automation import VARTYPE, VT_BOOL, VT_LPWSTR, VT_UI4, VT_CLSID



###
# All this stuff is to interface with the Win32 API
###
IID_Empty = GUID(
    '{00000000-0000-0000-0000-000000000000}')

CLSID_MMDeviceEnumerator = GUID(
    '{BCDE0395-E52F-467C-8E3D-C4579291692E}')


UINT32 = c_uint32
REFERENCE_TIME = c_longlong


class PROPVARIANT_UNION(Union):
        _fields_ = [
            ('lVal', LONG),
            ('uhVal', ULARGE_INTEGER),
            ('boolVal', VARIANT_BOOL),
            ('pwszVal', LPWSTR),
            ('puuid', GUID),
        ]


class PROPVARIANT(Structure):
    _fields_ = [
        ('vt', VARTYPE),
        ('reserved1', WORD),
        ('reserved2', WORD),
        ('reserved3', WORD),
        ('union', PROPVARIANT_UNION),
    ]

    def GetValue(self):
        vt = self.vt
        if vt == VT_BOOL:
            return self.union.boolVal != 0
        elif vt == VT_LPWSTR:
            # return Marshal.PtrToStringUni(union.pwszVal)
            return self.union.pwszVal
        elif vt == VT_UI4:
            return self.union.lVal
        elif vt == VT_CLSID:
            # TODO
            # return (Guid)Marshal.PtrToStructure(union.puuid, typeof(Guid))
            return
        else:
            return "%s:?" % (vt)


class WAVEFORMATEX(Structure):
    _fields_ = [
        ('wFormatTag', WORD),
        ('nChannels', WORD),
        ('nSamplesPerSec', WORD),
        ('nAvgBytesPerSec', WORD),
        ('nBlockAlign', WORD),
        ('wBitsPerSample', WORD),
        ('cbSize', WORD),
    ]


class ERole(Enum):
    eConsole = 0
    eMultimedia = 1
    eCommunications = 2
    ERole_enum_count = 3


class EDataFlow(Enum):
    eRender = 0
    eCapture = 1
    eAll = 2
    EDataFlow_enum_count = 3


class DEVICE_STATE(Enum):
    ACTIVE = 0x00000001
    DISABLED = 0x00000002
    NOTPRESENT = 0x00000004
    UNPLUGGED = 0x00000008
    MASK_ALL = 0x0000000F


class AudioDeviceState(Enum):
    Active = 0x1
    Disabled = 0x2
    NotPresent = 0x4
    Unplugged = 0x8


class STGM(Enum):
    STGM_READ = 0x00000000


class AUDCLNT_SHAREMODE(Enum):
    AUDCLNT_SHAREMODE_SHARED = 0x00000001
    AUDCLNT_SHAREMODE_EXCLUSIVE = 0x00000002

class IAudioEndpointVolume(IUnknown):
    _iid_ = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
    _methods_ = (
        # HRESULT RegisterControlChangeNotify(
        # [in] IAudioEndpointVolumeCallback *pNotify);
        COMMETHOD([], HRESULT, 'NotImpl1'),
        # HRESULT UnregisterControlChangeNotify(
        # [in] IAudioEndpointVolumeCallback *pNotify);
        COMMETHOD([], HRESULT, 'NotImpl2'),
        # HRESULT GetChannelCount([out] UINT *pnChannelCount);
        COMMETHOD([], HRESULT, 'GetChannelCount',
                  (['out'], POINTER(UINT), 'pnChannelCount')),
        # HRESULT SetMasterVolumeLevel(
        # [in] float fLevelDB, [in] LPCGUID pguidEventContext);
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], POINTER(GUID), 'pguidEventContext')),
        # HRESULT SetMasterVolumeLevelScalar(
        # [in] float fLevel, [in] LPCGUID pguidEventContext);
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
                  (['in'], c_float, 'fLevel'),
                  (['in'], POINTER(GUID), 'pguidEventContext')),
        # HRESULT GetMasterVolumeLevel([out] float *pfLevelDB);
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevel',
                  (['out'], POINTER(c_float), 'pfLevelDB')),
        # HRESULT GetMasterVolumeLevelScalar([out] float *pfLevel);
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
                  (['out'], POINTER(c_float), 'pfLevelDB')),
        # HRESULT SetChannelVolumeLevel(
        # [in] UINT nChannel,
        # [in] float fLevelDB,
        # [in] LPCGUID pguidEventContext);
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
                  (['in'], UINT, 'nChannel'),
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], POINTER(GUID), 'pguidEventContext')),
        # HRESULT SetChannelVolumeLevelScalar(
        # [in] UINT nChannel,
        # [in] float fLevel,
        # [in] LPCGUID pguidEventContext);
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
                  (['in'], DWORD, 'nChannel'),
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], POINTER(GUID), 'pguidEventContext')),
        # HRESULT GetChannelVolumeLevel(
        # [in]  UINT nChannel,
        # [out] float *pfLevelDB);
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
                  (['in'], UINT, 'nChannel'),
                  (['out'], POINTER(c_float), 'pfLevelDB')),
        # HRESULT GetChannelVolumeLevelScalar(
        # [in]  UINT nChannel,
        # [out] float *pfLevel);
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
                  (['in'], DWORD, 'nChannel'),
                  (['out'], POINTER(c_float), 'pfLevelDB')),
        # HRESULT SetMute([in] BOOL bMute, [in] LPCGUID pguidEventContext);
        COMMETHOD([], HRESULT, 'SetMute',
                  (['in'], BOOL, 'bMute'),
                  (['in'], POINTER(GUID), 'pguidEventContext')),
        # HRESULT GetMute([out] BOOL *pbMute);
        COMMETHOD([], HRESULT, 'GetMute',
                  (['out'], POINTER(BOOL), 'pbMute')),
        # HRESULT GetVolumeStepInfo(
        # [out] UINT *pnStep,
        # [out] UINT *pnStepCount);
        COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
                  (['out'], POINTER(DWORD), 'pnStep'),
                  (['out'], POINTER(DWORD), 'pnStepCount')),
        # HRESULT VolumeStepUp([in] LPCGUID pguidEventContext);
        COMMETHOD([], HRESULT, 'VolumeStepUp',
                  (['in'], POINTER(GUID), 'pguidEventContext')),
        # HRESULT VolumeStepDown([in] LPCGUID pguidEventContext);
        COMMETHOD([], HRESULT, 'VolumeStepDown',
                  (['in'], POINTER(GUID), 'pguidEventContext')),
        # HRESULT QueryHardwareSupport([out] DWORD *pdwHardwareSupportMask);
        COMMETHOD([], HRESULT, 'QueryHardwareSupport',
                  (['out'], POINTER(DWORD), 'pdwHardwareSupportMask')),
        # HRESULT GetVolumeRange(
        # [out] float *pfLevelMinDB,
        # [out] float *pfLevelMaxDB,
        # [out] float *pfVolumeIncrementDB);
        COMMETHOD([], HRESULT, 'GetVolumeRange',
                  (['out'], POINTER(c_float), 'pfMin'),
                  (['out'], POINTER(c_float), 'pfMax'),
                  (['out'], POINTER(c_float), 'pfIncr')))

class PROPERTYKEY(Structure):
    _fields_ = [
        ('fmtid', GUID),
        ('pid', DWORD),
    ]

    def __str__(self):
        return "%s %s" % (self.fmtid, self.pid)


class IPropertyStore(IUnknown):
    _iid_ = GUID('{886d8eeb-8cf2-4446-8d02-cdba1dbdcf99}')
    _methods_ = (
        # HRESULT GetCount([out] DWORD *cProps);
        COMMETHOD([], HRESULT, 'GetCount',
                  (['out'], POINTER(DWORD), 'cProps')),
        # HRESULT GetAt(
        # [in] DWORD iProp,
        # [out] PROPERTYKEY *pkey);
        COMMETHOD([], HRESULT, 'GetAt',
                  (['in'], DWORD, 'iProp'),
                  (['out'], POINTER(PROPERTYKEY), 'pkey')),
        # HRESULT GetValue(
        # [in] REFPROPERTYKEY key,
        # [out] PROPVARIANT *pv);
        COMMETHOD([], HRESULT, 'GetValue',
                  (['in'], POINTER(PROPERTYKEY), 'key'),
                  (['out'], POINTER(PROPVARIANT), 'pv')),
        # HRESULT SetValue([out] LPWSTR *ppstrId);
        COMMETHOD([], HRESULT, 'SetValue',
                  (['out'], POINTER(LPWSTR), 'ppstrId')),
        # HRESULT Commit();
        COMMETHOD([], HRESULT, 'Commit'))

class IMMDevice(IUnknown):
    _iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
    _methods_ = (
        # HRESULT Activate(
        # [in] REFIID iid,
        # [in] DWORD dwClsCtx,
        # [in] PROPVARIANT *pActivationParams,
        # [out] void **ppInterface);
        COMMETHOD([], HRESULT, 'Activate',
                  (['in'], POINTER(GUID), 'iid'),
                  (['in'], DWORD, 'dwClsCtx'),
                  (['in'], POINTER(DWORD), 'pActivationParams'),
                  (['out'],
                   POINTER(POINTER(IUnknown)), 'ppInterface')),
        # HRESULT OpenPropertyStore(
        # [in] DWORD stgmAccess,
        # [out] IPropertyStore **ppProperties);
        COMMETHOD([], HRESULT, 'OpenPropertyStore',
                  (['in'], DWORD, 'stgmAccess'),
                  (['out'],
                  POINTER(POINTER(IPropertyStore)), 'ppProperties')),
        # HRESULT GetId([out] LPWSTR *ppstrId);
        COMMETHOD([], HRESULT, 'GetId',
                  (['out'], POINTER(LPWSTR), 'ppstrId')),
        # HRESULT GetState([out] DWORD *pdwState);
        COMMETHOD([], HRESULT, 'GetState',
        (['out'], POINTER(DWORD), 'pdwState')))

class IMMDeviceCollection(IUnknown):
    _iid_ = GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
    _methods_ = (
        # HRESULT GetCount([out] UINT *pcDevices);
        COMMETHOD([], HRESULT, 'GetCount',
                  (['out'], POINTER(UINT), 'pcDevices')),
        # HRESULT Item([in] UINT nDevice, [out] IMMDevice **ppDevice);
        COMMETHOD([], HRESULT, 'Item',
                  (['in'], UINT, 'nDevice'),
        (['out'], POINTER(POINTER(IMMDevice)), 'ppDevice')))

class IMMDeviceEnumerator(IUnknown):
    _iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
    _methods_ = (
        # HRESULT EnumAudioEndpoints(
        # [in] EDataFlow dataFlow,
        # [in] DWORD dwStateMask,
        # [out] IMMDeviceCollection **ppDevices);
        COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
                  (['in'], DWORD, 'dataFlow'),
                  (['in'], DWORD, 'dwStateMask'),
                  (['out'],
                  POINTER(POINTER(IMMDeviceCollection)), 'ppDevices')),
        # HRESULT GetDefaultAudioEndpoint(
        # [in] EDataFlow dataFlow,
        # [in] ERole role,
        # [out] IMMDevice **ppDevice);
        COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
                  (['in'], DWORD, 'dataFlow'),
                  (['in'], DWORD, 'role'),
                  (['out'], POINTER(POINTER(IMMDevice)), 'ppDevices')),
        # HRESULT GetDevice(
        # [in] LPCWSTR pwstrId,
        # [out] IMMDevice **ppDevice);
        COMMETHOD([], HRESULT, 'GetDevice',
                  (['in'], LPCWSTR, 'pwstrId'),
                  (['out'],
                  POINTER(POINTER(IMMDevice)), 'ppDevice')),
        # HRESULT RegisterEndpointNotificationCallback(
        # [in] IMMNotificationClient *pClient);
        COMMETHOD([], HRESULT, 'NotImpl1'),
        # HRESULT UnregisterEndpointNotificationCallback(
        # [in] IMMNotificationClient *pClient);
        COMMETHOD([], HRESULT, 'NotImpl2'))



# Real Control Code

class AudioUtilities(object):

    # Constructor
    def __init__(self):
        # self.is_muted = False
        deviceEnumerator = comtypes.CoCreateInstance(CLSID_MMDeviceEnumerator, IMMDeviceEnumerator, comtypes.CLSCTX_INPROC_SERVER)
        self.audio_input_devices = deviceEnumerator.GetDefaultAudioEndpoint(EDataFlow.eCapture.value, DEVICE_STATE.ACTIVE.value)

    def GetMicrophoneState(self):
        interface = self.audio_input_devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
        volume_control_ptr = ctypes.cast(interface, POINTER(IAudioEndpointVolume))
        return volume_control_ptr.GetMute()

    def MuteMicrophone(self):
        try:
            interface = self.audio_input_devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
            volume_control_ptr = ctypes.cast(interface, POINTER(IAudioEndpointVolume))
            volume_control_ptr.SetMute(True, None)
        except Exception as e:
            raise "EXCEPTION [MuteMicrophone]: \n{}".format(e)
            
    def UnMuteMicrophone(self):
        try:
            interface = self.audio_input_devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
            volume_control_ptr = ctypes.cast(interface, POINTER(IAudioEndpointVolume))
            volume_control_ptr.SetMute(False, None)
        except Exception as e:
            raise "EXCEPTION [UnMuteMicrophone]: \n{}".format(e)
    
    @property
    def micsCount(self):
        return [self.audio_input_devices]

# Main Entry Point
# This example mutes the mic for three seconds, the unmutes the mic
# if __name__ == "__main__":
    
#     from time import sleep #DO NOT USE THIS FOR FINAL VERSION. SLEEP IS BLOCKING
#     # Create a Microphone controller object
#     test_audio_control = AudioUtilities()
#     # Mute the Microphone
#     test_audio_control.MuteMicrophone()
#     #sleep for 3 seconds for testing purposes
#     sleep(3)
#     test_audio_control.UnMuteMicrophone()
#     # Microphone Unmuted. Done with this example,
    
#     # Example using toggle function
#     print("\n\nToggle Test")
#     print("toggle on")
#     test_audio_control.toggle_mute()
#     sleep(3)
#     print("toggle off")
#     test_audio_control.toggle_mute()