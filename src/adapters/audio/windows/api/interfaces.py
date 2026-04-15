# src/adapters/audio/windows/api/interfaces.py

from ctypes import HRESULT, POINTER, c_float
from ctypes.wintypes import BOOL, DWORD, LPCWSTR, LPWSTR, UINT
from comtypes import COMMETHOD, GUID, IUnknown
from typing import TYPE_CHECKING

from src.adapters.audio.windows.api.structures import (
    PROPERTYKEY,
    PROPVARIANT,
    AUDIO_VOLUME_NOTIFICATION_DATA,
    WAVEFORMATEX,
    DEVICE_SHARED_MODE,
    IPolicyPropertyKey,
    IPolicyPropVariant,
)
from src.adapters.audio.windows.api.constants import (
    EEndpointHardwareSupport,
    EAudioDeviceState,
    REFERENCE_TIME,
    EDataFlow,
    ERole
)


class IAudioEndpointVolumeCallback(IUnknown):
    """
    IAudioEndpointVolumeCallback interface provides notifications of changes
    in the volume level and muting state of an audio endpoint device.

    Example of usage:
    ```
    # The most simple external event handler for obtaining events and data.
    def external_event_handler(event_type: str, data: dict[str, str]):
        print({event_type:data})

    class EndpointVolumeCallbackClient(COMObject):
        # Define the neccesary `_com_objects_` magic var to point out that
        # we are waiting for changes from the specific device, such as
        # "mute state" or "volume range" changed.
        _com_objects_ = [IAudioEndpointVolumeCallback]

        def __init__(self, external_event_handler: Callable[str]=None):
            self.external_event_handler = external_event_handler

        def OnNotify(self, pNotify):
            print('Volume:', pNotify.fMasterVolume) # Device volume data
            print('Muted:', pNotify.bMuted) # Mute state of device

            # Top `print`-s are for example, in real case we may transfer the
            # `notified` data from system to our external handler like this:
            if self.self.external_event_handler:
                self.external_event_handler(pNotify.contents)
    ```

    :Returns:
    - <b>HRESULT</b>: If the method succeeds, it returns S_OK. If it fails,
    it returns an error code.


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

    if TYPE_CHECKING:
        def OnNotify(self, pNotifyData: AUDIO_VOLUME_NOTIFICATION_DATA) -> None:
            '''
            The OnNotify method notifies the client that the volume level or
            muting state of the audio endpoint device has changed.

            Docs: https://learn.microsoft.com/en-gb/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolumecallback-onnotify
            '''
            ...


class IAudioEndpointVolume(IUnknown):
    """
    The IAudioEndpointVolume interface represents the volume controls on the
    audio stream to or from an audio endpoint device.
    A client obtains a reference to the IAudioEndpointVolume
    interface of an endpoint device by calling the `IMMDevice::Activate`
    method with parameter `iid` set to `REFIID IID_IAudioEndpointVolume`.

    Example of device initialization:
    ```
    audio_endpoint_volume = audio_device.Activate(
        IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None
    )
    ```
    Where `audio_device` is an instance of `IMMDevice` interface.


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
            (["in"], UINT, "nChannel"),
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
            (["in"], UINT, "nChannel"),
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
            (["out"], POINTER(c_float), "pflVolumeMindB"),
            (["out"], POINTER(c_float), "pflVolumeMaxdB"),
            (["out"], POINTER(c_float), "pflVolumeIncrementdB"),
        ),
    )

    if TYPE_CHECKING:
        def RegisterControlChangeNotify(self, pNotify: IAudioEndpointVolumeCallback) -> None:
            '''
            The RegisterControlChangeNotify method registers a client's notification callback interface.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-registercontrolchangenotify
            '''
            ...

        def UnregisterControlChangeNotify(self, pNotify: IAudioEndpointVolumeCallback) -> None:
            '''
            The UnregisterControlChangeNotify method deletes the registration
            of a client's notification callback interface that the client
            registered in a previous call to the
            IAudioEndpointVolume::RegisterControlChangeNotify method.
            
            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-unregistercontrolchangenotify
            '''
            ...

        def GetChannelCount(self) -> int:
            '''
            The GetChannelCount method gets a count of the channels in the audio
            stream that enters or leaves the audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-getchannelcount
            '''
            ...
        

        def SetMasterVolumeLevel(self, fLevelDB: float, pguidEventContext: GUID) -> None:
            '''
            The SetMasterVolumeLevel method sets the master volume level,
            in decibels, of the audio stream that enters or leaves the
            audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-setmastervolumelevel
            '''
            ...

        def SetMasterVolumeLevelScalar(self, fLevel: float, pguidEventContext: GUID):
            '''
            The SetMasterVolumeLevelScalar method sets the master volume level
            of the audio stream that enters or leaves the audio endpoint device.
            The volume level is expressed as a normalized, audio-tapered
            value in the range from 0.0 to 1.0.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-setmastervolumelevelscalar
            '''
            ...

        def GetMasterVolumeLevel(self) -> float:
            '''
            The GetMasterVolumeLevel method gets the master volume level,
            in decibels, of the audio stream that enters or leaves the
            audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-getmastervolumelevel
            '''
            ...

        def GetMasterVolumeLevelScalar(self) -> float:
            '''
            The GetMasterVolumeLevelScalar method gets the master volume level
            of the audio stream that enters or leaves the audio endpoint device.
            The volume level is expressed as a normalized, audio-tapered value
            in the range from 0.0 to 1.0.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-getmastervolumelevelscalar
            '''
            ...

        def SetChannelVolumeLevel(
                self, nChannel: int, fLevelDB: float, pguidEventContext: GUID
                ) -> None:
            '''
            The SetChannelVolumeLevel method sets the volume level, in decibels,
            of the specified channel of the audio stream that enters or leaves
            the audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-setchannelvolumelevel
            '''
            ...

        def SetChannelVolumeLevelScalar(
                self, nChannel: int, fLevelDB: float, pguidEventContext: GUID
                ) -> None:
            '''
            The SetChannelVolumeLevelScalar method sets the normalized,
            audio-tapered volume level of the specified channel in the audio
            stream that enters or leaves the audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-setchannelvolumelevelscalar
            '''
            ...

        def GetChannelVolumeLevel(self, nChannel: int) -> float:
            '''
            The GetChannelVolumeLevel method gets the volume level, in decibels,
            of the specified channel in the audio stream that enters or leaves
            the audio endpoint device.
            
            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-getchannelvolumelevel
            '''
            ...

        def GetChannelVolumeLevelScalar(self, nChannel: int) -> float:
            '''
            The GetChannelVolumeLevelScalar method gets the normalized,
            audio-tapered volume level of the specified channel of the audio
            stream that enters or leaves the audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-getchannelvolumelevelscalar
            '''
            ...

        def SetMute(self, bMute: bool, pguidEventContext: GUID) -> None:
            '''
            The SetMute method sets the muting state of the audio stream that
            enters or leaves the audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-setmute
            '''
            ...

        def GetMute(self) -> bool:
            '''
            The GetMute method gets the muting state of the audio stream that
            enters or leaves the audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-getmute
            '''
            ...

        def GetVolumeStepInfo(self) -> tuple[str, str]:
            '''
            The GetVolumeStepInfo method gets information about the current
            step in the volume range.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-getvolumestepinfo
            '''
            ...

        def VolumeStepUp(self, pguidEventContext: GUID) -> None:
            '''
            The VolumeStepUp method increments, by one step, the volume level of the audio stream that enters or leaves the audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-volumestepup
            '''
            ...

        def VolumeStepDown(self, pguidEventContext: GUID) -> None:
            '''
            The VolumeStepDown method decrements, by one step, the volume
            level of the audio stream that enters or leaves the audio endpoint
            device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-volumestepdown
            '''
            ...

        def QueryHardwareSupport(self) -> EEndpointHardwareSupport:
            '''
            The QueryHardwareSupport method queries the audio endpoint device for its hardware-supported functions.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-queryhardwaresupport
            '''
            ...
        
        def GetVolumeRange(self) -> tuple[float, float, float]:
            '''
            The GetVolumeRange method gets the volume range, in decibels,
            of the audio stream that enters or leaves the audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/nf-endpointvolume-iaudioendpointvolume-getvolumerange
            '''
            ...


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

    if TYPE_CHECKING:
        def GetCount(self) -> str:
            '''
            This method returns a count of the number of properties that
            are attached to the file.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/propsys/nf-propsys-ipropertystore-getcount
            '''
            ...

        def GetAt(self, iProp: str) -> PROPERTYKEY:
            '''
            Gets a property key from the property array of an item.
            
            Docs: https://learn.microsoft.com/en-us/windows/win32/api/propsys/nf-propsys-ipropertystore-getat
            '''
            ...

        def GetValue(self, key: PROPERTYKEY) -> PROPVARIANT:
            '''
            This method retrieves the data for a specific property.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/propsys/nf-propsys-ipropertystore-getvalue
            '''
            ...

        def SetValue(self, key: PROPERTYKEY, propvar: PROPVARIANT) -> None:
            '''
            This method sets a property value or replaces or removes an existing value.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/propsys/nf-propsys-ipropertystore-setvalue
            '''
            ...

        def Commit(self) -> None:
            '''
            After a change has been made, this method saves the changes.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/propsys/nf-propsys-ipropertystore-commit
            '''
            ...


class IMMDevice(IUnknown):
    _iid_ = GUID("{D666063F-1587-4E43-81F1-B948E807363F}")
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            "Activate",
            (["in"], POINTER(GUID), "iid"),
            (["in"], DWORD, "dwClsCtx"),
            (["in"], POINTER(PROPVARIANT), "pActivationParams"),
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

    if TYPE_CHECKING:
        def Activate(self, iid: GUID, dwClsCtx: str, pActivationParams: PROPVARIANT) -> IAudioEndpointVolume | IUnknown:
            '''
            The Activate method creates a COM object with the specified interface.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdevice-activate
            '''
            ...

        def OpenPropertyStore(self, stgmAccess: str) -> IPropertyStore:
            '''
            The OpenPropertyStore method retrieves an interface to the device's
            property store.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdevice-openpropertystore
            '''
            ...

        def GetId(self) -> GUID:
            '''
            The GetId method retrieves an endpoint ID string that identifies
            the audio endpoint device.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdevice-getid
            '''
            ...

        def GetState(self) -> str:
            '''
            The GetState method retrieves the current device state.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdevice-getstate
            '''
            ...


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

    if TYPE_CHECKING:
        def GetCount(self) -> int:
            '''
            The GetCount method retrieves a count of the devices in the device
            collection.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdevicecollection-getcount
            '''
            ...

        def Item(self, nDevice: int) -> IMMDevice:
            '''
            The Item method retrieves a pointer to the specified item in the
            device collection.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdevicecollection-item
            '''
            ...


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
            (["in"], PROPERTYKEY, "key"),
        ),
    )

    if TYPE_CHECKING:
        def OnDeviceStateChanged(self, pwstrDeviceId: GUID, dwNewState: str) -> None:
            '''
            The OnDeviceStateChanged method indicates that the state of an
            audio endpoint device has changed.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immnotificationclient-ondevicestatechanged
            '''
            ...

        def OnDeviceAdded(self, pwstrDeviceId: GUID) -> None:
            '''
            The OnDeviceAdded method indicates that a new audio endpoint device
            has been added.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immnotificationclient-ondeviceadded
            '''
            ...

        def OnDeviceRemoved(self, pwstrDeviceId: GUID) -> None:
            '''
            The OnDeviceRemoved method indicates that an audio endpoint device
            has been removed.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immnotificationclient-ondeviceremoved
            '''
            ...

        def OnDefaultDeviceChanged(self, flow: EDataFlow, role: ERole) -> None:
            '''
            The OnDefaultDeviceChanged method notifies the client that the
            default audio endpoint device for a particular device role has
            changed.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immnotificationclient-ondefaultdevicechanged
            '''
            ...
        
        def OnPropertyValueChanged(self, pwstrDeviceId: GUID, key: PROPERTYKEY) -> None:
            '''
            The OnPropertyValueChanged method indicates that the value of a
            property belonging to an audio endpoint device has changed.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immnotificationclient-onpropertyvaluechanged
            '''
            ...


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

    if TYPE_CHECKING:
        def EnumAudioEndpoints(self, dataFlow: EDataFlow, dwStateMask: EAudioDeviceState) -> IMMDeviceCollection:
            '''
            The EnumAudioEndpoints method generates a collection of audio
            endpoint devices that meet the specified criteria.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdeviceenumerator-enumaudioendpoints
            '''
            ...
        
        def GetDefaultAudioEndpoint(self, dataFlow: EDataFlow, dwStateMask: EAudioDeviceState) -> IMMDeviceCollection:
            '''
            The GetDefaultAudioEndpoint method retrieves the default audio
            endpoint for the specified data-flow direction and role.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdeviceenumerator-getdefaultaudioendpoint
            '''
            ...

        def GetDevice(self, pwstrId: GUID) -> IMMDevice:
            '''
            The GetDevice method retrieves an audio endpoint device that is
            identified by an endpoint ID string.

            https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdeviceenumerator-getdevice
            '''
            ...

        def RegisterEndpointNotificationCallback(self, pClient: IMMNotificationClient) -> None:
            '''
            The RegisterEndpointNotificationCallback method registers a
            client's notification callback interface.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdeviceenumerator-registerendpointnotificationcallback
            '''
            ...

        def UnregisterEndpointNotificationCallback(self, pClient: IMMNotificationClient) -> None:
            '''
            The UnregisterEndpointNotificationCallback method deletes the
            registration of a notification interface that the client registered
            in a previous call to the
            IMMDeviceEnumerator::RegisterEndpointNotificationCallback method.

            Docs: https://learn.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdeviceenumerator-unregisterendpointnotificationcallback
            '''
            ...


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
        COMMETHOD(
            [],
            HRESULT,
            "ResetDeviceFormat",
            (["in"], LPCWSTR, "pwstrDeviceId")
        ),
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
            (["out"], POINTER(REFERENCE_TIME), "pmftDefaultPeriod"),
            (["out"], POINTER(REFERENCE_TIME), "pmftMinimumPeriod"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetProcessingPeriod",
            (["in"], LPCWSTR, "pwstrDeviceId"),
            (["in"], POINTER(REFERENCE_TIME), "pmftPeriod"),
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

    if TYPE_CHECKING:
        def GetMixFormat(self, pwstrDeviceId: GUID) -> WAVEFORMATEX:
            ...

        def GetDeviceFormat(
                self, pwstrDeviceId: GUID, bDefault: bool
            ) -> WAVEFORMATEX:
            ...

        def ResetDeviceFormat(self, pwstrDeviceId: GUID) -> None:
            ...

        def SetDeviceFormat(
                self,
                pwstrDeviceId: GUID,
                pEndpointFormat: WAVEFORMATEX,
                pMixFormat: WAVEFORMATEX
            ) -> None:
            ...

        def GetProcessingPeriod(
                self, pwstrDeviceId: GUID, bDefault: bool
            ) -> tuple[REFERENCE_TIME, REFERENCE_TIME]:
            ...

        def SetProcessingPeriod(
                self, pwstrDeviceId: GUID, pmftPeriod: REFERENCE_TIME
            ) -> None:
            ...

        def GetShareMode(self, pwstrDeviceId: GUID) -> DEVICE_SHARED_MODE:
            ...

        def SetShareMode(
                self, pwstrDeviceId: GUID, pMode: DEVICE_SHARED_MODE
            ) -> None:
            ...

        def GetPropertyValue(
                self, pwstrDeviceId: GUID, key: IPolicyPropertyKey
            ) -> IPolicyPropertyKey:
            ...

        def SetPropertyValue(
                self, pwstrDeviceId: GUID,
                key: IPolicyPropertyKey,
                pValue: IPolicyPropertyKey
            ) -> None:
            ...

        def SetDefaultEndpoint(self, pwstrDeviceId: GUID, eRole: ERole) -> None:
            ...

        def SetEndpointVisibility(self, pwstrDeviceId: GUID, bVisible: bool) -> None:
            ...
