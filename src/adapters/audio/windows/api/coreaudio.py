# src/adapters/audio/windows/api/winapi.py

import sys
import traceback
from traceback import print_exc as print_exception
from threading import get_ident as get_thread_ident
from typing import Optional, Tuple, Literal

# COM WITH MULTITHREADED APARTMENT
sys.coinit_flags = 0  # noqa: E402

from comtypes import ( # noqa: E402
    CLSCTX_ALL,
    COMObject,
    COMError,
    CoCreateInstance,
    CoUninitialize
)

from src.services.logger import logger # noqa: E402
from src.adapters.audio.windows.api.structures import ( # noqa: E402
    AUDIO_VOLUME_NOTIFICATION_DATA, PROPERTYKEY, PROPVARIANT
)
from src.adapters.audio.windows.api.interfaces import ( # noqa: E402
    IAudioEndpointVolumeCallback,
    IAudioEndpointVolume,
    IMMNotificationClient,
    IMMDeviceEnumerator,
    IPolicyConfig,
    IMMDevice
)
from src.adapters.audio.windows.api.constants import ( # noqa: E402
    DEVPKEY_Device_FriendlyName,
    EAudioDeviceState,
    EDataFlow,
    ERole,
    STGM
)


class PublicAudioNotificationClient(COMObject):
    """
    Internal COM object for handling audio endpoint notifications.

    This class implements the IMMNotificationClient interface to receive
    general notifications about audio device changes such as default device
    changes, device additions/removals, state changes, and property value changes.

    To make it work, its needed to register it with 
    `WindowsCoreAudioAPI.register_audio_notification_handler()` method.
    To unregister, use `WindowsCoreAudioAPI.unregister_audio_notification_handler()`

    This is **internal** COM class implementation, all the work it does is
    redirects data to the custom callback (event_handler).
    """

    _com_interfaces_ = (IMMNotificationClient,)

    def OnDefaultDeviceChanged(
        self, flow_id: int, role_id: int, default_device_id: str
    ):
        """**Notifies event handler when the default audio device changes.**

        - Args (data comes **in** this func):
            `flow_id` (int): The data flow type (EDataFlow).
            `role_id` (int): The role of the device (ERole).
            `default_device_id_str` (Optional[str]): The ID of the new default device, or None if no device is set.
        - Returns:
            `HRESULT` (comtypes.HRESULT): S_OK on success.
        """
        if flow_id == EDataFlow.eCapture.value:
            # self._event_handler(
            #     "default_device_changed",
            #     default_device_id,
            #     {"role": ERole(role_id).name},
            # )
            self.on_default_device_changed(
                flow_id, role_id, default_device_id
            )
        return 0  # S_OK

    def OnDeviceAdded(self, added_device_id_str: str):
        """**Notifies event handler when a new audio device is added.**

        - Args (data comes **in** this func):
            `added_device_id_str` (str): The ID of the added device.
        - Returns:
            `HRESULT` (comtypes.HRESULT): S_OK on success.
        """
        # self._event_handler(
        #     "device_added", added_device_id_str, None
        # )
        self.on_device_added(added_device_id_str)
        return 0  # S_OK

    def OnDeviceRemoved(self, removed_device_id_str: str):
        """
        **Notifies event handler when an audio device is removed.**

        - Args (data comes **in** this func):
            `removed_device_id_str` (str): The ID of the removed device.
        - Returns:
            `HRESULT` (comtypes.HRESULT): S_OK on success.
        """
        # self._event_handler(
        #     "device_removed", removed_device_id_str, None
        # )
        self.on_device_removed(removed_device_id_str)
        return 0  # S_OK

    def OnDeviceStateChanged(self, device_id_str: str, new_state_id: int):
        """
        **Notifies event handler when the state of an audio device changes.**

        - Args (data comes **in** this func):
            `device_id_str` (str): The ID of the device whose state changed.
            `new_state_id` (int): The new state of the device (AudioDeviceState enum value).
        - Returns:
            `HRESULT` (comtypes.HRESULT): S_OK on success.
        """
        # self._event_handler(
        #     "device_state_changed", device_id_str, {
        #         "new_state": EAudioDeviceState(new_state_id).name
        #     }
        # )
        self.on_device_state_changed(device_id_str, new_state_id)
        return 0  # S_OK

    def OnPropertyValueChanged(self, device_id_str: str, property_key_ptr: PROPERTYKEY):
        """
        **Notifies event handler when a property value of an audio device changes.**

        - Args (data comes **in** this func):
            `device_id_str` (str): The ID of the device whose property changed.
            `property_key_ptr` (POINTER[PROPERTYKEY]): Pointer to the PROPERTYKEY structure that identifies the property.
        - Returns:
            `HRESULT` (comtypes.HRESULT): S_OK on success.
        """
        # key_info = property_key_ptr.contents  # Разыменовываем указатель
        # self._event_handler(
        #     "property_changed",
        #     device_id_str,
        #     {"key_fmtid": str(key_info.fmtid), "key_pid": key_info.pid},
        # )
        self.on_property_value_changed(device_id_str, property_key_ptr)
        return 0  # S_OK

    # =========================================================================
    def on_default_device_changed(
            self, flow_id: int, role_id: int, default_device_id: str
        ):
        raise NotImplementedError

    def on_device_added(self, added_device_id_str: str):
        raise NotImplementedError

    def on_device_removed(self, removed_device_id_str: str):
        raise NotImplementedError

    def on_device_state_changed(self, device_id_str: str, new_state_id: int):
        raise NotImplementedError

    def on_property_value_changed(
            self, device_id_str: str, property_key_ptr: PROPERTYKEY
        ):
        raise NotImplementedError


class PublicDeviceVolumeNotificationClient(COMObject):
    """
    Internal COM object for handling device endpoint notifications.

    This class implements the IAudioEndpointVolumeCallback interface to receive
    device-spesific notifications about audio device changes such as device
    mute state changed and volume state changed events.

    To make it work, its needed to register it with
    `WindowsCoreAudioAPI.register_device_notification_handler()` method.
    To unregister, use `WindowsCoreAudioAPI.register_device_notification_handler()`.

    This is **internal** COM class implementation, all the work it does is
    redirects data to the custom callback (event_handler).
    """
    _com_interfaces_ = [IAudioEndpointVolumeCallback]

    def OnNotify(self, pNotify: AUDIO_VOLUME_NOTIFICATION_DATA):
        try:
        # get the data of the PAUDIO_VOLUME_NOTIFICATION_DATA Structure
            notify_data = pNotify.contents

            channels = notify_data.nChannels
            volumes = notify_data.afChannelVolumes
            channel_volumes = volumes[:channels]

            event_context = notify_data.guidEventContext

            self.on_notify(
                new_volume=notify_data.fMasterVolume,
                new_mute=notify_data.bMuted,
                event_context=event_context,
                channels=channels,
                channel_volumes=channel_volumes,
            )
        except Exception:
            traceback.print_exc()

    def on_notify(self, new_volume, new_mute, event_context, channels, channel_volumes):
        raise NotImplementedError


# --- Main API class ---
class WindowsCoreAudioAPI:
    """
    **Windows Core Audio API for managing audio devices.**

    This class provides methods to interact with audio devices on Windows,
    including enumerating devices, getting default devices, changing muting and
    volume device state, also handling device notifications.

    It uses COM interfaces to interact with the Windows audio subsystem.
    It is a pseudo-singleton class, so you should call
    `WindowsCoreAudioAPI.initialize()` once before using any methods, and
    `WindowsCoreAudioAPI.uninitialize()` when done, or closing the app/thread.
    This class is not thread-safe!

    **Usage:**
    ```python
    from src.adapters.audio.windows.api.coreaudio import WindowsCoreAudioAPI

    WindowsCoreAudioAPI.initialize()  # Initialize COM and device enumerator
    api = WindowsCoreAudioAPI.get_instance()  # Get API instance
    devices = api.enumerate_devices(enabled_only=False)  # Get all capture devices
    default_device = api.get_default_communication_device()  # Get default communications device

    audio_notif_callback = api.register_device_notification_handler(default_device.GetId(), my_callback)  # Register callback for default device
    # Where `my_callback` is a callable that takes (event_type, device_id, data) parameters
    api.unregister_device_notification_handler(audio_notif_callback)  # Unregister device callback when done
    WindowsCoreAudioAPI.uninitialize()  # Uninitialize COM and clean up resources
    ```
    """

    # Pseudo-singleton
    _instance: Optional["WindowsCoreAudioAPI"] = None

    def __init__(self):
        """
        Calls when WindowsCoreAudioAPI was initialized by
        `WindowsCoreAudioAPI.initialize()`.
        """
        # Storing thread ID for logs
        self._curr_thread = get_thread_ident()

        # Storing enumerator (pseudo-singleton)
        self._enumerator = CoCreateInstance(
            IMMDeviceEnumerator.clsid,
            interface=IMMDeviceEnumerator,
            clsctx=CLSCTX_ALL,
        )

        self.device_callbacks: dict = {}

    @classmethod
    def initialize(cls) -> None:
        """
        Main init func. Before *any* calls to WindowsCoreAudioAPI this func
        needs to be called mandatory.
        """
        if cls._instance is None:
            cls._instance = WindowsCoreAudioAPI()
            logger.info(
                f"WindowsCoreAudioAPI initialized (MTA) in thread {cls._instance._curr_thread}"
            )

    @classmethod
    def get_instance(cls) -> "WindowsCoreAudioAPI":
        """
        To use `WindowsCoreAudioAPI`, call this func *only* after calling
        `WindowsCoreAudioAPI.initialize()`. Using example:

        ```python
        from src.adapters.audio.windows.api.coreaudio import WindowsCoreAudioAPI

        WindowsCoreAudioAPI.initialize()  # Mandatory!

        api = WindowsCoreAudioAPI.get_instance()
        active_devices = api.enumerate_devices()
        print(active_devices)

        WindowsCoreAudioAPI.uninitialize()  # Mandatory!
        ```
        """
        if cls._instance is None:
            raise RuntimeError("WindowsCoreAudioAPI not initialized. Call initialize() first.")
        return cls._instance

    @classmethod
    def uninitialize(cls) -> None:
        """
        Main uninit func. After working with WindowsCoreAudioAPI this func
        needs to be called mandatory.
        """
        if cls._instance is not None:
            try:
                CoUninitialize()
                logger.info(
                    f"WindowsCoreAudioAPI (MTA) uninitialized in thread {cls._instance._curr_thread}"
                )
            except Exception:
                print_exception()
            cls._instance = None

    def _get_device(self, device_id: str) -> Optional[IMMDevice]:
        return self._enumerator.GetDevice(device_id)

    def _get_audio_endpoint_volume(self, device_id: str) -> Optional[IAudioEndpointVolume]:
        imm_device = self._enumerator.GetDevice(device_id)

        endpoint_volume_ptr = imm_device.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        audio_endpoint_volume = endpoint_volume_ptr.QueryInterface(IAudioEndpointVolume)
        return audio_endpoint_volume

    def _get_device_property(self, device_id: str, fmtid: str, pid: int):
        imm_device = self._get_device(device_id)
        store = imm_device.OpenPropertyStore(STGM.STGM_READ.value)
        if not store:
            raise WindowsError("Unknown (no property store)")
        
        search_value = bytes(fmtid)
        for i in range(store.GetCount()):
            pk = store.GetAt(i)
            if not (bytes(pk.fmtid) == search_value and pk.pid == pid):
                continue

            value = store.GetValue(pk)
            return value.GetValue()

    # def _set_device_property(self, device_id: str, propkey: PROPERTYKEY, propvar: PROPVARIANT, value: str):
    #     try:
    #         imm_device = self._get_device(device_id)
    #         store = imm_device.OpenPropertyStore(STGM.STGM_WRITE.value)
    #         if not store:
    #             raise WindowsError("Unknown (no property store)")

    #         pv_for_write = PROPVARIANT()
    #         # pv_for_write.vt = 31
    #         pv_u = PROPVARIANT_UNION()
    #         pv_u.pwszVal = value

    #         pv_for_write.union = pv_u

    #         store.SetValue(propkey, pv_for_write)
    #     except Exception:
    #         traceback.print_exc()
    #     else:
    #         store.Commit()

    def enumerate_devices(self, enabled_only: bool = True) -> Optional[Tuple[IMMDevice]]:
        devices = tuple()

        if enabled_only:
            devices_states = EAudioDeviceState.Active.value | EAudioDeviceState.Disabled.value
        else:
            devices_states = sum(v.value for v in EAudioDeviceState._member_map_.values())

        collection = self._enumerator.EnumAudioEndpoints(
            EDataFlow.eCapture.value,
            devices_states
        )
        count = collection.GetCount()
        for i in range(count):
            device = collection.Item(i)
            devices += (device, )

        return devices

    def get_device_state(self, device_id: str) -> EAudioDeviceState:
        return EAudioDeviceState(self._get_device(device_id).GetState()).name

    def get_device_friendly_name(self, device_id: str) -> str:
        return self._get_device_property(
            device_id,
            DEVPKEY_Device_FriendlyName.fmtid,
            DEVPKEY_Device_FriendlyName.pid
        )

    def get_default_multimedia_device(self) -> Optional[IMMDevice]:
        imm_device = self._enumerator.GetDefaultAudioEndpoint(
            EDataFlow.eCapture.value, ERole.eMultimedia.value
        )
        return imm_device

    def get_default_communication_device(self) -> Optional[IMMDevice]:
        imm_device = self._enumerator.GetDefaultAudioEndpoint(
            EDataFlow.eCapture.value, ERole.eCommunications.value
        )
        return imm_device

    def set_default_device(self, device_id: str, role_value: ERole=None) -> Optional[bool]:
        imm_device = self._get_device(device_id)
        if (
            not imm_device
            or imm_device.GetState() != EAudioDeviceState.Active.value
        ):
            return False  # Устройство не найдено или неактивно

        policy_config: IPolicyConfig = CoCreateInstance(
            IPolicyConfig.clsid, interface=IPolicyConfig, clsctx=CLSCTX_ALL
        )

        if role_value:
            roles = [role_value]
        else:
            roles = [ERole.eConsole, ERole.eCommunications, ERole.eMultimedia]

        for role in roles:
            policy_config.SetDefaultEndpoint(device_id, role.value)

        return True

    def get_device_mute(self, device_id: str) -> Optional[bool]:
        a_ep_vol = self._get_audio_endpoint_volume(device_id)
        mute_status = bool(a_ep_vol.GetMute())
        return mute_status

    def set_device_mute(
            self,
            device_id: str,
            mute_state: bool,
            guid_event_context: Optional[str]=None
        ) -> bool:
        a_ep_vol = self._get_audio_endpoint_volume(device_id)
        if guid_event_context:
            a_ep_vol.SetMute(mute_state, guid_event_context)
        else:
            a_ep_vol.SetMute(mute_state, None)
        return True

    def get_device_volume(self, device_id: str) -> float | None:
        a_ep_vol = self._get_audio_endpoint_volume(device_id)
        volume = float(a_ep_vol.GetMasterVolumeLevelScalar())
        return volume

    def set_device_volume(self, device_id: str, volume: float) -> bool | None:
        if not (0.0 <= volume <= 1.0):
            raise ValueError("Volume must be between 0.0 and 1.0")

        a_ep_vol = self._get_audio_endpoint_volume(device_id)
        a_ep_vol.SetMasterVolumeLevelScalar(volume, None)
        return True

    def set_endpoint_visibility(self, device_id: str, device_state: bool) -> Optional[bool]:
        policy_config: IPolicyConfig = CoCreateInstance(
                IPolicyConfig.clsid, interface=IPolicyConfig, clsctx=CLSCTX_ALL
            )

        policy_config.SetEndpointVisibility(device_id, device_state)
        return True

    def register_audio_notification_handler(self, callback):
        try:
            self._enumerator.RegisterEndpointNotificationCallback(callback)
        except Exception:
            traceback.print_exc()

    def unregister_audio_notification_handler(self, callback):
        try:
            self._enumerator.UnregisterEndpointNotificationCallback(callback)
        except Exception:
            traceback.print_exc()

    def register_device_notification_handler(self, callback):
        ep_vol = self._get_audio_endpoint_volume(callback.device_id)
        ep_vol.RegisterControlChangeNotify(callback)
        self.device_callbacks[callback.device_id] = (ep_vol, callback)

    def unregister_device_notification_handler(self, callback):
        ep_vol, dev_callb = self.device_callbacks.pop(callback.device_id)
        ep_vol.UnregisterControlChangeNotify(dev_callb)
