# src/platform/winos/api/interfaces.py

from ctypes import HRESULT, POINTER, c_float
from ctypes.wintypes import BOOL, DWORD, LPCWSTR, LPWSTR, UINT
from comtypes import COMMETHOD, GUID, IUnknown

from src.adapters.audio.windows.api.structures import (
    PROPERTYKEY,
    PROPVARIANT,
    AUDIO_VOLUME_NOTIFICATION_DATA,
    WAVEFORMATEX,
    DEVICE_SHARED_MODE,
    IPolicyPropertyKey,
    IPolicyPropVariant,
)
from src.adapters.audio.windows.api.constants import REFERENCE_TIME


class IAudioEndpointVolumeCallback(IUnknown):
    """
    IAudioEndpointVolumeCallback interface provides notifications of changes
    in the volume level and muting state of an audio endpoint device.


    Methods:
    - OnNotify: The OnNotify method notifies the client that the volume level
    or muting state of the audio endpoint device has changed.


    Argumnets:
    - pNotify: Pointer to an AUDIO_VOLUME_NOTIFICATION_DATA structure that
    describes the volume level and muting state of the audio endpoint device.
    Example of usage:
    ```
    class AudioEndpointVolumeCallback(IAudioEndpointVolumeCallback):
        def OnNotify(self, pNotify):
            print('Volume:', pNotify.fMasterVolume)
            print('Muted:', pNotify.bMuted)
    ```


    Returns:
    - HRESULT: If the method succeeds, it returns S_OK.


    Docs:
    https://learn.microsoft.com/en-gb/windows/win32/api/endpointvolume/nn-endpointvolume-iaudioendpointvolumecallback
    """

    _iid_ = GUID("{b1136c83-b6b5-4add-98a5-a2df8eedf6fa}")
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            "OnNotify",
            (["in"], POINTER(AUDIO_VOLUME_NOTIFICATION_DATA), "pNotify"),
        ),
    )


class IAudioEndpointVolume(IUnknown):
    """
    The IAudioEndpointVolume interface represents the volume controls on the
    audio stream to or from an audio endpoint device.
    A client obtains a reference to the IAudioEndpointVolume
    interface of an endpoint device by calling the `IMMDevice::Activate`
    method with parameter `iid` set to `REFIID IID_IAudioEndpointVolume`.

    Example of initialization:
    ```
    audio_endpoint_volume = audio_device.Activate(
        IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None
    )
    ```
    Where `audio_device` is an instance of `IMMDevice` interface.



    Methods:
    - RegisterControlChangeNotify: The RegisterControlChangeNotify method
    registers a client's notification interface to receive notifications of
    changes in the volume level or muting state of the audio stream that flows
    through an audio endpoint device.
    Example of usage:
    ```
    class AudioEndpointVolumeCallback(IAudioEndpointVolumeCallback):
        def OnNotify(self, pNotify):
            print('Volume:', pNotify.fMasterVolume)
            print('Muted:', pNotify.bMuted)

    audio_endpoint_volume.RegisterControlChangeNotify(AudioEndpointVolumeCallback())
    ```


    - UnregisterControlChangeNotify: The UnregisterControlChangeNotify method
    deletes a client's notification interface from the list of clients that
    receive notifications of changes in the volume level or muting state of the
    audio stream that flows through an audio endpoint device.
    Example of usage:
    ```
    audio_endpoint_volume.UnregisterControlChangeNotify(AudioEndpointVolumeCallback())
    ```
    Where `AudioEndpointVolumeCallback` is an instance of
    `IAudioEndpointVolumeCallback` interface.


    - GetChannelCount: The GetChannelCount method gets the number of channels
    in the audio stream that enters or leaves the audio endpoint device.
    Example of usage:
    ```
    channel_count = audio_endpoint_volume.GetChannelCount()
    print(channel_count)
    ```
    Where `channel_count` is the number of channels in the audio stream.


    - SetMasterVolumeLevel: The SetMasterVolumeLevel method sets the master
    volume level of the audio stream that enters or leaves the audio endpoint
    device.
    Example of usage:
    ```
    audio_endpoint_volume.SetMasterVolumeLevel(-10.0, None)
    ```
    Where `-10.0` is the volume level in decibels.


    - SetMasterVolumeLevelScalar: The SetMasterVolumeLevelScalar method sets
    the master volume level, in decibels, of the audio stream that enters or
    leaves the audio endpoint device.
    Example of usage:
    ```
    audio_endpoint_volume.SetMasterVolumeLevelScalar(0.5, None)
    ```
    Where `0.5` is the volume level in decibels.


    - GetMasterVolumeLevel: The GetMasterVolumeLevel method gets the master
    volume level of the audio stream that enters or leaves the audio endpoint
    device.
    Example of usage:
    ```
    master_volume = audio_endpoint_volume.GetMasterVolumeLevel()
    print(master_volume)
    ```
    Where `master_volume` is the master volume level in decibels.


    - GetMasterVolumeLevelScalar: The GetMasterVolumeLevelScalar method gets
    the master volume level, in decibels, of the audio stream that enters or
    leaves the audio endpoint device.
    Example of usage:
    ```
    master_volume = audio_endpoint_volume.GetMasterVolumeLevelScalar()
    print(master_volume)
    ```
    Where `master_volume` is the master volume level in decibels.


    - SetChannelVolumeLevel: The SetChannelVolumeLevel method sets the volume
    level, in decibels, of the specified channel in the audio stream that
    enters or leaves the audio endpoint device.
    Example of usage:
    ```
    audio_endpoint_volume.SetChannelVolumeLevel(0, -10.0, None)
    ```
    Where `0` is the channel number and `-10.0` is the volume level in decibels.


    - SetChannelVolumeLevelScalar: The SetChannelVolumeLevelScalar method sets
    the volume level, in decibels, of the specified channel in the audio stream
    that enters or leaves the audio endpoint device.
    Example of usage:
    ```
    audio_endpoint_volume.SetChannelVolumeLevelScalar(0, 0.5, None)
    ```
    Where `0` is the channel number and `0.5` is the volume level in decibels.


    - GetChannelVolumeLevel: The GetChannelVolumeLevel method gets the volume
    level, in decibels, of the specified channel in the audio stream that
    enters or leaves the audio endpoint device.
    Example of usage:
    ```
    channel_volume = audio_endpoint_volume.GetChannelVolumeLevel(0)
    print(channel_volume)
    ```
    Where `0` is the channel number and `channel_volume` is the volume level in
    decibels.


    - GetChannelVolumeLevelScalar: The GetChannelVolumeLevelScalar method gets
    the volume level, in decibels, of the specified channel in the audio stream
    that enters or leaves the audio endpoint device.
    Example of usage:
    ```
    channel_volume = audio_endpoint_volume.GetChannelVolumeLevelScalar(0)
    print(channel_volume)
    ```
    Where `0` is the channel number and `channel_volume` is the volume level in
    decibels.


    - SetMute: The SetMute method sets the muting state of the audio stream
    that enters or leaves the audio endpoint device.
    Example of usage:
    ```
    audio_endpoint_volume.SetMute(True, None)
    ```
    Where `True` is the muting state.


    - GetMute: The GetMute method gets the muting state of the audio stream
    that enters or leaves the audio endpoint device.
    Example of usage:
    ```
    mute_status = audio_endpoint_volume.GetMute()
    print(mute_status)
    ```
    Where `mute_status` is the muting state.


    - GetVolumeStepInfo: The GetVolumeStepInfo method gets the range and
    increment of the volume settings of the audio stream that enters or leaves
    the audio endpoint device.
    Example of usage:
    ```
    step, step_count = audio_endpoint_volume.GetVolumeStepInfo()
    print(step, step_count)
    ```
    Where `step` is the range and `step_count` is the increment of the volume
    settings.


    - VolumeStepUp: The VolumeStepUp method increases the volume level of the
    audio stream by one step.
    Example of usage:
    ```
    audio_endpoint_volume.VolumeStepUp(None)
    ```
    Where `None` is the event context.


    - VolumeStepDown: The VolumeStepDown method decreases the volume level of
    the audio stream by one step.
    Example of usage:
    ```
    audio_endpoint_volume.VolumeStepDown(None)
    ```
    Where `None` is the event context.


    - QueryHardwareSupport: The QueryHardwareSupport method gets information
    about the hardware support of the audio endpoint device.
    Example of usage:
    ```
    hardware_support = audio_endpoint_volume.QueryHardwareSupport()
    print(hardware_support)
    ```
    Where `hardware_support` is the information about the hardware support.


    - GetVolumeRange: The GetVolumeRange method gets the volume range, in
    decibels, of the audio stream that enters or leaves the audio endpoint
    device.
    Example of usage:
    ```
    min_volume, max_volume, incr = audio_endpoint_volume.GetVolumeRange()
    print(min_volume, max_volume, incr)
    ```
    Where `min_volume` is the minimum volume, `max_volume` is the maximum
    volume, and `incr` is the increment of the volume range.


    Docs: https://learn.microsoft.com/en-gb/windows/win32/api/endpointvolume/nn-endpointvolume-iaudioendpointvolume
    """

    _iid_ = GUID("{5CDF2C82-841E-4546-9722-0CF74078229A}")
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            "RegisterControlChangeNotify",
            (["in"], POINTER(IAudioEndpointVolumeCallback), "pNotify"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "UnregisterControlChangeNotify",
            (["in"], POINTER(IAudioEndpointVolumeCallback), "pNotify"),
        ),
        COMMETHOD(
            [], HRESULT, "GetChannelCount", (["out"], POINTER(UINT), "pnChannelCount")
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetMasterVolumeLevel",
            (["in"], c_float, "fLevelDB"),
            (["in"], POINTER(GUID), "pguidEventContext"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetMasterVolumeLevelScalar",
            (["in"], c_float, "fLevel"),
            (["in"], POINTER(GUID), "pguidEventContext"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetMasterVolumeLevel",
            (["out"], POINTER(c_float), "pfLevelDB"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetMasterVolumeLevelScalar",
            (["out"], POINTER(c_float), "pfLevelDB"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetChannelVolumeLevel",
            (["in"], UINT, "nChannel"),
            (["in"], c_float, "fLevelDB"),
            (["in"], POINTER(GUID), "pguidEventContext"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetChannelVolumeLevelScalar",
            (["in"], DWORD, "nChannel"),
            (["in"], c_float, "fLevelDB"),
            (["in"], POINTER(GUID), "pguidEventContext"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetChannelVolumeLevel",
            (["in"], UINT, "nChannel"),
            (["out"], POINTER(c_float), "pfLevelDB"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetChannelVolumeLevelScalar",
            (["in"], DWORD, "nChannel"),
            (["out"], POINTER(c_float), "pfLevelDB"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetMute",
            (["in"], BOOL, "bMute"),
            (["in"], POINTER(GUID), "pguidEventContext"),
        ),
        COMMETHOD([], HRESULT, "GetMute", (["out"], POINTER(BOOL), "pbMute")),
        COMMETHOD(
            [],
            HRESULT,
            "GetVolumeStepInfo",
            (["out"], POINTER(DWORD), "pnStep"),
            (["out"], POINTER(DWORD), "pnStepCount"),
        ),
        COMMETHOD(
            [], HRESULT, "VolumeStepUp", (["in"], POINTER(GUID), "pguidEventContext")
        ),
        COMMETHOD(
            [], HRESULT, "VolumeStepDown", (["in"], POINTER(GUID), "pguidEventContext")
        ),
        COMMETHOD(
            [],
            HRESULT,
            "QueryHardwareSupport",
            (["out"], POINTER(DWORD), "pdwHardwareSupportMask"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetVolumeRange",
            (["out"], POINTER(c_float), "pfMin"),
            (["out"], POINTER(c_float), "pfMax"),
            (["out"], POINTER(c_float), "pfIncr"),
        ),
    )


class IPropertyStore(IUnknown):
    """
    The IPropertyStore interface provides methods for accessing and
    manipulating properties.
    A client obtains a reference to the IPropertyStore interface of a property
    store by calling the `IMMDevice::OpenPropertyStore` method. The property
    store represents the collection of properties of an audio endpoint device.
    Example of initialization:
    ```
    property_store = audio_device.OpenPropertyStore(0)
    ```
    Where `audio_device` is an instance of `IMMDevice` interface, 0 is the
    access mode. Possible values, their numbers and meanings:
    - STGM_READ = 0x00000000 (0): Opens the property store in read mode.
    - STGM_WRITE = 0x00000001 (1): Opens the property store in write mode.
    - STGM_READWRITE = 0x00000002 (2): Opens the property store in read/write mode.


    Methods:
    - GetCount: The GetCount method retrieves the number of properties in the
    property store.
    Example of usage:
    ```
    count = property_store.GetCount()
    print(count)
    ```
    Where `count` is the number of properties in the property store.


    - GetAt: The GetAt method retrieves a property key from the property store
    at the specified index.
    Example of usage:
    ```
    key = property_store.GetAt(0)
    print(key)
    ```
    Where `0` is the index of the property key and `key` is the property key.


    - GetValue: The GetValue method retrieves the value of a property in the
    property store.
    Example of usage:
    ```
    key = property_store.GetAt(0)
    value = property_store.GetValue(key)
    print(value)
    ```
    Where `0` is the index of the property key, `key` is the property key, and
    `value` is the value of the property.


    - SetValue: The SetValue method sets the value of a property in the property
    store.
    Example of usage:
    ```
    key = property_store.GetAt(0)
    value = property_store.GetValue(key)
    property_store.SetValue(key)
    ```
    Where `0` is the index of the property key, `key` is the property key, and
    `value` is the value of the property.


    - Commit: The Commit method saves a property to the property store.
    Example of usage:
    ```
    property_store.Commit()
    ```
    Where `property_store` is the instance of `IPropertyStore` interface.


    Docs: https://learn.microsoft.com/en-gb/windows/win32/api/propsys/nn-propsys-ipropertystore
    """

    _iid_ = GUID("{886d8eeb-8cf2-4446-8d02-cdba1dbdcf99}")
    _methods_ = (
        COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(DWORD), "cProps")),
        COMMETHOD(
            [],
            HRESULT,
            "GetAt",
            (["in"], DWORD, "iProp"),
            (["out"], POINTER(PROPERTYKEY), "pkey"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetValue",
            (["in"], POINTER(PROPERTYKEY), "key"),
            (["out"], POINTER(PROPVARIANT), "pv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetValue",
            (["in"], POINTER(PROPERTYKEY), "key"),
            (["in"], POINTER(PROPVARIANT), "propvar"),  # Corrected parameters
        ),
        COMMETHOD([], HRESULT, "Commit"),
    )


class IMMDevice(IUnknown):
    _iid_ = GUID("{D666063F-1587-4E43-81F1-B948E807363F}")
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            "Activate",
            (["in"], POINTER(GUID), "iid"),
            (["in"], DWORD, "dwClsCtx"),
            (["in"], POINTER(DWORD), "pActivationParams"),
            (["out"], POINTER(POINTER(IUnknown)), "ppInterface"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "OpenPropertyStore",
            (["in"], DWORD, "stgmAccess"),
            (["out"], POINTER(POINTER(IPropertyStore)), "ppProperties"),
        ),
        COMMETHOD([], HRESULT, "GetId", (["out"], POINTER(LPWSTR), "ppstrId")),
        COMMETHOD([], HRESULT, "GetState", (["out"], POINTER(DWORD), "pdwState")),
    )


class IMMDeviceCollection(IUnknown):
    _iid_ = GUID("{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}")
    _methods_ = (
        COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(UINT), "pcDevices")),
        COMMETHOD(
            [],
            HRESULT,
            "Item",
            (["in"], UINT, "nDevice"),
            (["out"], POINTER(POINTER(IMMDevice)), "ppDevice"),
        ),
    )


class IMMNotificationClient(IUnknown):
    _iid_ = GUID("{7991EEC9-7E89-4D85-8390-6C703CEC60C0}")
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            "OnDeviceStateChanged",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], DWORD, "dwNewState"),
        ),
        COMMETHOD([], HRESULT, "OnDeviceAdded", (["in"], LPCWSTR, "pwstrDeviceId")),
        COMMETHOD([], HRESULT, "OnDeviceRemoved", (["in"], LPCWSTR, "pwstrDeviceId")),
        COMMETHOD(
            [],
            HRESULT,
            "OnDefaultDeviceChanged",
            (["in"], DWORD, "flow"),
            (["in"], DWORD, "role"),
            (["in"], LPCWSTR, "pwstrDefaultDeviceId"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "OnPropertyValueChanged",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            #   (['in'], POINTER(GUID), 'key'))
            (["in"], POINTER(PROPERTYKEY), "key"),
        ),
    )


class IMMDeviceEnumerator(IUnknown):
    clsid = GUID("{BCDE0395-E52F-467C-8E3D-C4579291692E}")
    _iid_ = GUID("{A95664D2-9614-4F35-A746-DE8DB63617E6}")
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            "EnumAudioEndpoints",
            (["in"], DWORD, "dataFlow"),
            (["in"], DWORD, "dwStateMask"),
            (["out"], POINTER(POINTER(IMMDeviceCollection)), "ppDevices"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetDefaultAudioEndpoint",
            (["in"], DWORD, "dataFlow"),
            (["in"], DWORD, "role"),
            (["out"], POINTER(POINTER(IMMDevice)), "ppDevices"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetDevice",
            (["in"], LPCWSTR, "pwstrId"),
            (["out"], POINTER(POINTER(IMMDevice)), "ppDevice"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "RegisterEndpointNotificationCallback",
            (["in"], POINTER(IMMNotificationClient), "pClient"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "UnregisterEndpointNotificationCallback",
            (["in"], POINTER(IMMNotificationClient), "pClient"),
        ),
    )


class IPolicyConfig(IUnknown):
    clsid = GUID("{870af99c-171d-4f9e-af0d-e63df40c2bc9}")
    _case_insensitive_ = True
    _iid_ = GUID("{f8679f50-850a-41cf-9c72-430f290290c8}")
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            "GetMixFormat",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["out"], POINTER(POINTER(WAVEFORMATEX)), "pFormat"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetDeviceFormat",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], BOOL, "bDefault"),
            (["out"], POINTER(POINTER(WAVEFORMATEX)), "pFormat"),
        ),
        COMMETHOD([], HRESULT, "ResetDeviceFormat", (["in"], LPCWSTR, "pwstrDeviceId")),
        COMMETHOD(
            [],
            HRESULT,
            "SetDeviceFormat",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], POINTER(WAVEFORMATEX), "pEndpointFormat"),
            (["in"], POINTER(WAVEFORMATEX), "pMixFormat"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetProcessingPeriod",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], BOOL, "bDefault"),
            (["out"], POINTER(REFERENCE_TIME), "hnsDefaultDevicePeriod"),
            (["out"], POINTER(REFERENCE_TIME), "hnsMinimumDevicePeriod"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetProcessingPeriod",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], POINTER(REFERENCE_TIME), "hnsDevicePeriod"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetShareMode",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["out"], POINTER(DEVICE_SHARED_MODE), "pMode"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetShareMode",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], POINTER(DEVICE_SHARED_MODE), "pMode"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetPropertyValue",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], POINTER(IPolicyPropertyKey), "key"),
            (["out"], POINTER(IPolicyPropVariant), "pValue"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetPropertyValue",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], POINTER(IPolicyPropertyKey), "key"),
            (["in"], POINTER(IPolicyPropVariant), "pValue"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetDefaultEndpoint",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], DWORD, "eRole"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetEndpointVisibility",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], BOOL, "bVisible"),
        ),
    )
