# src/adapters/audio/win/winapi.py

import sys
import threading
import traceback
from typing import List, Optional, Callable, Any, Dict, Tuple
from comtypes import (
    CLSCTX_ALL,
    CoCreateInstance,
    CoInitializeEx,
    CoUninitialize,
    COMError,
    COMObject,
    POINTER,
    cast,
    HRESULT,
    COINIT_APARTMENTTHREADED
)

from src.core.entites import Microphone

from src.adapters.audio.windows.api.interfaces import (
    IAudioEndpointVolume,
    IAudioEndpointVolumeCallback,
    IPolicyConfig,
    IMMDeviceEnumerator,
    IMMNotificationClient,
    IMMDevice,
)
from src.adapters.audio.windows.api.constants import (
    EDataFlow,
    AudioDeviceState,
    ERole,
    STGM,
    PROPERTYKEY,
    DEVPKEY_Device_FriendlyName,  # PROPERTYKEY constant for getting device FriendlyName
)
from src.adapters.audio.windows.api.structures import AUDIO_VOLUME_NOTIFICATION_DATA
from src.adapters.audio.windows.api.exceptions import WindowsAudioNotificationClientError


# --- Internal COM object for handling general changes in audio devices notifications ---
# Its not part of the public API, so we use a leading underscore
class _WindowsAudioNotificationClientInternal(COMObject):
    """
    Internal COM object for handling audio endpoint notifications.

    This class implements the IMMNotificationClient interface to receive
    general notifications about audio device changes such as default device
    changes, device additions/removals, state changes, and property value changes.

    To make it work, its needed to register it with the IMMDeviceEnumerator
    using the `WinAudioAPI.register_notification_callback` method.
    """

    _com_interfaces_ = [IMMNotificationClient]

    def OnDefaultDeviceChanged(
        self, flow_id: int, role_id: int, default_device_id_str: Optional[str]
    ) -> HRESULT:
        """**Notifies event handler when the default audio device changes.**

        - Args:
            `flow_id` (int): The data flow type (EDataFlow).
            `role_id` (int): The role of the device (ERole).
            `default_device_id_str` (Optional[str]): The ID of the new default device, or None if no device is set.
        - Returns:
            `HRESULT` (comtypes.HRESULT): S_OK on success.
        """
        if WinAudioAPI._external_event_handler and flow_id == EDataFlow.eCapture.value:
            try:
                role_name_str = "UnknownRole"
                for role_enum_member in ERole:
                    if role_enum_member.value == role_id:
                        role_name_str = role_enum_member.name
                        break
                WinAudioAPI._external_event_handler(
                    "default_device_changed",
                    default_device_id_str,
                    {"role": role_name_str},
                )
            except Exception as e:
                # Printing traceback only once for each unique exception
                WinAudioAPI._print_exc_once_cls(
                    "Error in OnDefaultDeviceChanged callback handler:\n" + str(e)
                )
                raise WindowsAudioNotificationClientError(
                    default_device_id_str or "Unknown", str(e)
                ) from e
        return 0  # S_OK

    def OnDeviceAdded(self, added_device_id_str: str) -> HRESULT:
        """**Notifies event handler when a new audio device is added.**

        - Args:
            `added_device_id_str` (str): The ID of the added device.
        - Returns:
            `HRESULT` (comtypes.HRESULT): S_OK on success.
        """
        if WinAudioAPI._external_event_handler:
            try:
                WinAudioAPI._external_event_handler(
                    "device_added", added_device_id_str, None
                )
            except Exception as e:
                WinAudioAPI._print_exc_once_cls(
                    "Error in OnDeviceAdded callback handler:\n" + str(e)
                )
                raise WindowsAudioNotificationClientError(
                    added_device_id_str or "Unknown", str(e)
                ) from e
        return 0

    def OnDeviceRemoved(self, removed_device_id_str: str) -> HRESULT:
        """
        **Notifies event handler when an audio device is removed.**

        - Args:
            `removed_device_id_str` (str): The ID of the removed device.
        - Returns:
            `HRESULT` (comtypes.HRESULT): S_OK on success.
        """
        if WinAudioAPI._external_event_handler:
            try:
                WinAudioAPI._external_event_handler(
                    "device_removed", removed_device_id_str, None
                )
            except Exception as e:
                WinAudioAPI._print_exc_once_cls(
                    "Error in OnDeviceRemoved callback handler:\n" + str(e)
                )
                raise WindowsAudioNotificationClientError(
                    removed_device_id_str or "Unknown", str(e)
                ) from e
        return 0

    def OnDeviceStateChanged(self, device_id_str: str, new_state_id: int) -> HRESULT:
        """
        **Notifies event handler when the state of an audio device changes.**

        - Args:
            `device_id_str` (str): The ID of the device whose state changed.
            `new_state_id` (int): The new state of the device (AudioDeviceState enum value).
        - Returns:
            `HRESULT` (comtypes.HRESULT): S_OK on success.
        """
        if WinAudioAPI._external_event_handler:
            try:
                state_name_str = "UnknownState"
                for state_enum_member in AudioDeviceState:
                    if state_enum_member.value == new_state_id:
                        state_name_str = state_enum_member.name.lower()
                        break
                WinAudioAPI._external_event_handler(
                    "device_state_changed", device_id_str, {"new_state": state_name_str}
                )
            except Exception as e:
                WinAudioAPI._print_exc_once_cls(
                    "Error in OnDeviceStateChanged callback handler:\n" + str(e)
                )
                raise WindowsAudioNotificationClientError(
                    device_id_str or "Unknown", str(e)
                ) from e
        return 0

    def OnPropertyValueChanged(
        self, device_id_str: str, property_key: PROPERTYKEY
    ) -> HRESULT:
        """
        **Notifies event handler when a property value of an audio device changes.**

        - Args:
            `device_id_str` (str): The ID of the device whose property changed.
            `property_key` (PROPERTYKEY): PROPERTYKEY structure that identifies the property.
        - Returns:
            `HRESULT` (comtypes.HRESULT): S_OK on success.
        """
        if WinAudioAPI._external_event_handler:
            try:
                WinAudioAPI._external_event_handler(
                    "property_changed",
                    device_id_str,
                    {"key_fmtid": str(property_key.fmtid), "key_pid": property_key.pid},
                )
            except Exception as e:
                WinAudioAPI._print_exc_once_cls(
                    "Error in OnPropertyValueChanged callback handler:\n" + str(e)
                )
                raise WindowsAudioNotificationClientError(
                    device_id_str or "Unknown", str(e)
                ) from e
        return 0


# --- Internal COM object for handling changes in audio volume/mute state notifications ---
# Its not part of the public API, so we use a leading underscore
class _WindowsVolumeNotificationClientInternal(COMObject):
    _com_interfaces_ = [IAudioEndpointVolumeCallback]

    def __init__(self, device_id: str):
        super().__init__()
        self._device_id = (
            device_id  # Сохраняем ID устройства, для которого этот callback
        )

    def OnNotify(
        self, pNotifyData: "POINTER[AUDIO_VOLUME_NOTIFICATION_DATA]"
    ) -> HRESULT:
        if WinAudioAPI._external_event_handler:
            try:
                notify_data = pNotifyData.contents
                event_data = {
                    "is_muted": bool(notify_data.bMuted),
                    "master_volume": float(notify_data.fMasterVolume),
                    "event_context_guid": str(notify_data.guidEventContext),
                }
                # Отправляем событие с указанием ID устройства
                WinAudioAPI._external_event_handler(
                    "volume_changed", self._device_id, event_data
                )
            except Exception:
                WinAudioAPI._print_exc_once_cls(
                    f"Error in Volume OnNotify for device {self._device_id}"
                )
        return 0  # S_OK


# --- Main API class ---
class WinAudioAPI:
    """
    **Windows Audio API for managing audio devices.**

    This class provides methods to interact with audio devices on Windows,
    including enumerating devices, getting default devices, and handling
    device notifications.
    It uses COM interfaces to interact with the Windows audio subsystem.
    It is a pseudo-singleton class, so you should call `WinAudioAPI.initialize()` once
    before using any methods, and `WinAudioAPI.uninitialize()` when done, or
    closing the app/thread. This class is not thread-safe!

    **Usage:**
    ```python
    from src.adapters.audio.win import WinAudioAPI
    from src.adapters.audio.win.api.constants import ERole

    WinAudioAPI.initialize()  # Initialize COM and device enumerator
    devices = WinAudioAPI.get_all_devices()  # Get all capture devices
    default_device = WinAudioAPI.get_default_capture_device(ERole.eCommunications.value)  # Get default communications device

    WinAudioAPI.register_callbacks(my_event_handler)  # Register callbacks for device and volume events
    # Where `my_event_handler` is a callable that takes (event_type, device_id, data) parameters
    WinAudioAPI.unregister_callbacks()  # Unregister all callbacks when done
    WinAudioAPI.uninitialize()  # Uninitialize COM and clean up resources
    ```
    """

    # Для отслеживания режима инициализации COM
    _com_init_mode_is_sta: Optional[bool] = None
    # device_id -> (IAudioEndpointVolume_ptr, CallbackCOMObject)
    _active_volume_callbacks: Dict[
        str,
        Tuple[
            "POINTER[IAudioEndpointVolume]", _WindowsVolumeNotificationClientInternal
        ],
    ] = {}
    # Thread ID where COM was initialized
    _com_initialized_thread_id: Optional[int] = None
    # Placeholder for IMMDeviceEnumerator for enumerating audio devices
    _device_enumerator_instance: Optional[IMMDeviceEnumerator] = None
    # Placeholder for the internal COM object that handles notifications
    _notification_client_com_obj: Optional[_WindowsAudioNotificationClientInternal] = (
        None
    )
    # External event handler for device notifications
    _external_event_handler: Optional[
        Callable[[str, Optional[str], Optional[Any]], None]
    ] = None
    # Placeholder for user registration event handler
    _user_registered_event_handler: Optional[
        Callable[[str, Optional[str], Optional[Any]], None]
    ] = None
    _printed_exceptions_log = set()  # For _print_exc_once_cls

    @classmethod
    def _print_exc_once_cls(cls, message_prefix: str):
        """Prints the traceback for an exception only once."""
        exc_info = sys.exc_info()
        # Create a unique key for the exception (type + message)
        # The traceback may vary depending on the call stack,
        # so it's better to rely on the type and message for "sameness".
        exc_key = (exc_info[0], str(exc_info[1]))
        if exc_key not in cls._printed_exceptions_log:
            tb_str = "".join(traceback.format_exception(*exc_info))
            print(f"{message_prefix}:\n{tb_str}")
            cls._printed_exceptions_log.add(exc_key)

    @classmethod
    def initialize(cls) -> None:
        current_thread_id = threading.get_ident()
        if (
            cls._com_initialized_thread_id is not None
            and cls._com_initialized_thread_id != current_thread_id
        ):
            raise RuntimeError(
                f"COM was initialized in thread {cls._com_initialized_thread_id} by this API, but now in {current_thread_id}. Cross-thread COM usage with this API wrapper is problematic."
            )

        if (
            cls._com_initialized_thread_id is None
        ):  # Если наш API еще не инициализировал COM в этом потоке
            try:
                # Пытаемся инициализировать в режиме STA
                CoInitializeEx(COINIT_APARTMENTTHREADED)
                cls._com_initialized_thread_id = current_thread_id
                cls._com_init_mode_is_sta = True
                print(
                    f"INFO: COM Initialized (STA) by WinAudioAPI in thread {current_thread_id}."
                )
            except COMError as e:
                # HRESULT для RPC_E_CHANGED_MODE (0x80010106, в comtypes это может быть -2147417850)
                # Означает, что COM уже инициализирован в этом потоке, но в другом режиме (вероятно, MTA)
                if e.hresult == -2147417850:  # RPC_E_CHANGED_MODE
                    cls._com_initialized_thread_id = (
                        current_thread_id  # Запоминаем, что COM инициализирован
                    )
                    cls._com_init_mode_is_sta = False  # Но не нами и не в STA
                    print(
                        "WARNING: COM already initialized in this thread with a different concurrency model (MTA). WinAudioAPI prefers STA. Functionality might be affected if components require STA."
                    )
                else:
                    # Другая ошибка COM при инициализации
                    raise RuntimeError(f"Failed to initialize COM: {e}") from e
            except OSError as e_os:  # Иногда comtypes бросает OSError
                if (
                    hasattr(e_os, "winerror") and e_os.winerror == -2147417850
                ):  # RPC_E_CHANGED_MODE
                    cls._com_initialized_thread_id = current_thread_id
                    cls._com_init_mode_is_sta = False
                    print(
                        "WARNING: COM already initialized (OSError), possibly in a different mode (MTA)."
                    )
                else:
                    raise RuntimeError(
                        f"Failed to initialize COM (OSError): {e_os}"
                    ) from e_os

        # Если COM инициализирован (нами или кем-то еще в этом потоке), продолжаем
        if cls._device_enumerator_instance is None:
            if (
                cls._com_initialized_thread_id != current_thread_id
                and cls._com_initialized_thread_id is not None
            ):
                # Этого не должно произойти, если предыдущая проверка на поток корректна
                print(
                    f"CRITICAL WARNING: Attempting to create enumerator in thread {current_thread_id} while COM was marked initialized by API in thread {cls._com_initialized_thread_id}"
                )

            try:
                cls._device_enumerator_instance = CoCreateInstance(
                    IMMDeviceEnumerator.clsid,
                    interface=IMMDeviceEnumerator,
                    clsctx=CLSCTX_ALL,
                )
            except COMError as e:
                # Если создание энумератора не удалось, но мы думали, что COM инициализирован,
                # возможно, стоит сбросить флаг _com_initialized_thread_id, если это была наша инициализация,
                # но это усложнит логику. Пока просто бросаем ошибку.
                # Если инициализация была не нашей (MTA), то CoCreateInstance для STA-компонента может упасть.
                if cls._com_init_mode_is_sta is False:  # Если мы знаем, что режим MTA
                    print(
                        "ERROR: Failed to create IMMDeviceEnumerator. This might be due to COM being initialized in MTA mode, while the enumerator might prefer STA."
                    )
                raise RuntimeError(f"Failed to create IMMDeviceEnumerator: {e}") from e

        # Note: Volume callbacks will be registered when register_callbacks() is called by user

        cls._printed_exceptions_log.clear()  # Сбрасываем лог ошибок при новой инициализации

    @classmethod
    def uninitialize(cls) -> None:
        current_thread_id = threading.get_ident()
        # Деинициализируем, только если наш API сам инициализировал COM в этом потоке и в режиме STA
        # или если мы просто хотим очистить наши ресурсы, даже если COM был инициализирован кем-то еще.
        # Для простоты, если _com_initialized_thread_id установлен для текущего потока,
        # то мы считаем, что имеем право управлять нашими объектами и вызывать CoUninitialize,
        # если мы же и вызвали CoInitialize.

        # Unregister all callbacks if any are registered
        if cls._user_registered_event_handler is not None:
            cls.unregister_callbacks()

        if cls._com_initialized_thread_id == current_thread_id:
            if cls._device_enumerator_instance is not None:
                cls._device_enumerator_instance = None

            # Вызываем CoUninitialize только если мы сами инициализировали COM в STA
            # или если мы уверены, что это безопасно.
            # Если COM был инициализирован кем-то еще (особенно в MTA),
            # вызов CoUninitialize может нарушить работу другого кода.
            # Самый безопасный подход: если _com_init_mode_is_sta is True, то мы вызывали CoInitializeEx(STA).
            if (
                cls._com_init_mode_is_sta is True
            ):  # Только если мы инициализировали в STA
                try:
                    CoUninitialize()
                    print(
                        f"INFO: COM Uninitialized by WinAudioAPI in thread {current_thread_id}."
                    )
                except Exception as e:  # Ловим на всякий случай
                    cls._print_exc_once_cls(f"Error during CoUninitialize: {e}")

            cls._com_initialized_thread_id = None
            cls._com_init_mode_is_sta = None  # Сбрасываем флаг режима

        cls._printed_exceptions_log.clear()



    @classmethod
    def _get_device_enumerator(cls) -> IMMDeviceEnumerator:
        if cls._device_enumerator_instance is None:
            raise RuntimeError(
                "WinAudioAPI not initialized. Call WinAudioAPI.initialize() first."
            )
        return cls._device_enumerator_instance

    @classmethod
    def _to_entity(cls, imm_device: "POINTER[IMMDevice]") -> Microphone:
        try:
            return Microphone(
                id = cls.get_device_id(imm_device),
                name = cls.get_device_friendly_name(imm_device),
                volume = cls.get_device_volume_scalar(imm_device),
                muted = cls.get_device_mute(imm_device),
                active = cls.get_device_state_value(imm_device) == AudioDeviceState.Active.value,
                default = cls.get_default_capture_device().id == imm_device.GetId()
            )
        except Exception as e:
            print(e)

    @classmethod
    def get_all_capture_devices(cls) -> List['IMMDevice']:
        enumerator = cls._get_device_enumerator()
        devices = []
        try:
            collection = enumerator.EnumAudioEndpoints(
                EDataFlow.eCapture.value,
                AudioDeviceState.Active.value | AudioDeviceState.Disabled.value
            )
            count = collection.GetCount()
            for i in range(count):
                device = collection.Item(i)
                devices.append(device)
                # devices.append(cls._to_entity(device))
        except COMError as e:
            raise RuntimeError(f"Failed to enumerate audio endpoints: {e}") from e
        return devices

    @classmethod
    def get_default_capture_device(
        cls, role_value: ERole = ERole.eCommunications
    ) -> Optional['IMMDevice']:
        enumerator = cls._get_device_enumerator()
        try:
            imm_device = enumerator.GetDefaultAudioEndpoint(
                EDataFlow.eCapture.value, role_value.value
            )
            return imm_device

            # return Microphone(
            #     id = cls.get_device_id(imm_device),
            #     name = cls.get_device_friendly_name(imm_device),
            #     volume = cls.get_device_volume_scalar(imm_device),
            #     muted = cls.get_device_mute(imm_device),
            #     active = cls.get_device_state_value(imm_device) == AudioDeviceState.Active.value,
            #     default = True
            # )
        except COMError as e:
            if (
                e.hresult == -2147023728
            ):  # E_NOTFOUND (0x80070490) - нет такого устройства
                return None
            # Другие COMError могут быть более серьезными
            raise RuntimeError(
                f"Failed to get default audio endpoint (role_value: {role_value}): {e}"
            ) from e

    @classmethod
    def get_device_by_name(cls, device_name: str) -> Microphone:
        devices = cls.get_all_capture_devices()
        for device in devices:
            if device.name == device_name:
                return device

    @classmethod
    def get_device_by_id(cls, device_id: str) -> Optional["POINTER[IMMDevice]"]:
        enumerator = cls._get_device_enumerator()
        try:
            return enumerator.GetDevice(device_id)
        except COMError as e:
            if e.hresult == -2147024809: # NO_SUCH_DEVICE
                return None
            if e.hresult == -2147023728:  # ELEMENT_NOT_FOUND (0x80070490)
                return None
            # raise RuntimeError(f"Failed to get device by ID '{device_id}': {e}") from e

    @classmethod
    def get_device_id(cls, imm_device: "POINTER[IMMDevice]") -> str:
        return str(imm_device.GetId())

    @classmethod
    def get_device_state_value(cls, imm_device: "POINTER[IMMDevice]") -> int:
        return imm_device.GetState()

    @classmethod
    def get_device_friendly_name(cls, imm_device: "POINTER[IMMDevice]") -> str:
        try:
            store = imm_device.OpenPropertyStore(STGM.STGM_READ.value)
            if not store:
                return "Unknown (no property store)"

            # PROPVARIANT используется для хранения значения свойства
            pv_name = store.GetValue(DEVPKEY_Device_FriendlyName)
            name = str(pv_name.GetValue())  # GetValue PROPVARIANT'а
            pv_name.clear()  # Очищаем PROPVARIANT
            # store.Release() # comtypes
            return name
        except COMError as e:
            if e.hresult == -2147023728:  # ELEMENT_NOT_FOUND
                return "Unknown (name property missing)"
            return f"Unknown (COM Error {e.hresult:#010x} getting name)"
        except Exception:  # Ловим другие возможные ошибки
            cls._print_exc_once_cls(
                f"Generic error in get_device_friendly_name for {cls.get_device_id(imm_device)}"
            )
            return "Unknown (error getting name)"

    @classmethod
    def get_device_mute(cls, imm_device: "POINTER[IMMDevice]") -> Optional[bool]:
        if cls.get_device_state_value(imm_device) != AudioDeviceState.Active.value:
            return None
        try:
            endpoint_volume_ptr = imm_device.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            audio_ep_volume = cast(endpoint_volume_ptr, POINTER(IAudioEndpointVolume))
            mute_status = bool(audio_ep_volume.GetMute())
            # audio_ep_volume.Release() # comtypes
            return mute_status
        except COMError:
            return None

    @classmethod
    def set_device_mute(cls, mute: bool, imm_device: "POINTER[IMMDevice]") -> bool:
        if cls.get_device_state_value(imm_device) != AudioDeviceState.Active.value:
            return False
        try:
            endpoint_volume_ptr = imm_device.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            audio_ep_volume = cast(endpoint_volume_ptr, POINTER(IAudioEndpointVolume))
            audio_ep_volume.SetMute(mute, None)
            # audio_ep_volume.Release() # comtypes
            return True
        except COMError:
            return False

    @classmethod
    def get_device_volume_scalar(
        cls, imm_device: "POINTER[IMMDevice]"
    ) -> Optional[float]:
        if cls.get_device_state_value(imm_device) != AudioDeviceState.Active.value:
            return None
        try:
            endpoint_volume_ptr = imm_device.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            audio_ep_volume = cast(endpoint_volume_ptr, POINTER(IAudioEndpointVolume))
            volume = float(audio_ep_volume.GetMasterVolumeLevelScalar())
            # audio_ep_volume.Release() # comtypes
            return volume
        except COMError:
            return None

    @classmethod
    def set_device_volume_scalar(
        cls, imm_device: "POINTER[IMMDevice]", volume: float
    ) -> bool:
        if not (0.0 <= volume <= 1.0):
            raise ValueError("Volume must be between 0.0 and 1.0")
        if cls.get_device_state_value(imm_device) != AudioDeviceState.Active.value:
            return False
        try:
            endpoint_volume_ptr = imm_device.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            audio_ep_volume = cast(endpoint_volume_ptr, POINTER(IAudioEndpointVolume))
            audio_ep_volume.SetMasterVolumeLevelScalar(volume, None)
            # audio_ep_volume.Release() # comtypes
            return True
        except COMError:
            return False

    @classmethod
    def set_default_device(
        cls, device_id: str, role_value: int
    ) -> bool:  # Принимаем значение ERole
        imm_device = cls.get_device_by_id(device_id)
        if (
            not imm_device
            or cls.get_device_state_value(imm_device) != AudioDeviceState.Active.value
        ):
            return False  # Устройство не найдено или неактивно
        try:
            policy_config: IPolicyConfig = CoCreateInstance(
                IPolicyConfig.clsid, interface=IPolicyConfig, clsctx=CLSCTX_ALL
            )
            policy_config.SetDefaultEndpoint(device_id, role_value)
            # policy_config.Release() # comtypes
            return True
        except COMError:
            return False

    @classmethod
    def set_default_device_all_roles(cls, device_id: str) -> bool:
        """Sets device as default for all roles (Console, Communications, Multimedia)."""
        imm_device = cls.get_device_by_id(device_id)
        if (
            not imm_device
            or cls.get_device_state_value(imm_device) != AudioDeviceState.Active.value
        ):
            return False  # Устройство не найдено или неактивно

        success_count = 0
        try:
            policy_config: IPolicyConfig = CoCreateInstance(
                IPolicyConfig.clsid, interface=IPolicyConfig, clsctx=CLSCTX_ALL
            )

            # Set as default for all three roles
            for role in [ERole.eConsole, ERole.eCommunications, ERole.eMultimedia]:
                try:
                    policy_config.SetDefaultEndpoint(device_id, role.value)
                    success_count += 1
                except COMError as e:
                    cls._print_exc_once_cls(
                        f"Failed to set default device for role {role.name}: {e}"
                    )

            # policy_config.Release() # comtypes
            return (
                success_count > 0
            )  # Return True if at least one role was set successfully
        except COMError:
            return False

    # @classmethod
    # def register_notification_callback(cls, handler: Callable[[str, Optional[str], Optional[Any]], None]) -> None:
    #     enumerator = cls._get_device_enumerator()
    #     if cls._notification_client_com_obj is not None:
    #         # Если уже зарегистрирован, просто обновляем ссылку на внешний обработчик
    #         cls._external_event_handler = handler
    #         return

    #     cls._external_event_handler = handler
    #     cls._notification_client_com_obj = _WindowsAudioNotificationClientInternal()
    #     try:
    #         enumerator.RegisterEndpointNotificationCallback(cls._notification_client_com_obj)
    #     except COMError as e:
    #         cls._notification_client_com_obj = None # Сбрасываем, если регистрация не удалась
    #         cls._external_event_handler = None
    #         raise RuntimeError(f"Failed to register COM notification callback: {e}") from e

    # @classmethod
    # def unregister_notification_callback(cls) -> None:
    #     # Не принимаем handler, т.к. у нас только один внутренний COM-объект
    #     if cls._notification_client_com_obj and cls._device_enumerator_instance:
    #         try:
    #             cls._device_enumerator_instance.UnregisterEndpointNotificationCallback(cls._notification_client_com_obj)
    #         except COMError: # Игнорируем ошибку при отмене регистрации, но логируем
    #             cls._print_exc_once_cls("Error during UnregisterEndpointNotificationCallback in WinAudioAPI.unregister")

    #     # Освобождаем ссылки, чтобы comtypes могли очистить
    #     if cls._notification_client_com_obj is not None:
    #         # cls._notification_client_com_obj.Release() # comtypes
    #         cls._notification_client_com_obj = None
    #     cls._external_event_handler = None

    @classmethod
    def _register_volume_callback_for_device(
        cls, device_id: str, imm_device_ptr: "POINTER[IMMDevice]"
    ):
        if device_id in cls._active_volume_callbacks:
            return  # Уже зарегистрирован

        try:
            # Активируем IAudioEndpointVolume
            endpoint_volume_ptr_raw = imm_device_ptr.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            audio_ep_volume = cast(
                endpoint_volume_ptr_raw, POINTER(IAudioEndpointVolume)
            )

            # Создаем и регистрируем callback
            volume_callback_obj = _WindowsVolumeNotificationClientInternal(device_id)
            audio_ep_volume.RegisterControlChangeNotify(volume_callback_obj)

            cls._active_volume_callbacks[device_id] = (
                audio_ep_volume,
                volume_callback_obj,
            )
            device = cls.get_device_by_id(device_id)
            device_name = cls.get_device_friendly_name(device)
            print(f"INFO: Volume callback registered for device {device_id}: {device_name}")

        except COMError as e:
            cls._print_exc_once_cls(
                f"Failed to register volume callback for {device_id}: {e.hresult:#0x} {e.text}"
            )
        except Exception as e_gen:
            cls._print_exc_once_cls(
                f"Generic error registering volume callback for {device_id}: {e_gen}"
            )

    @classmethod
    def _unregister_volume_callback_for_device(cls, device_id: str):
        if device_id in cls._active_volume_callbacks:
            audio_ep_volume, volume_callback_obj = cls._active_volume_callbacks.pop(
                device_id
            )
            try:
                audio_ep_volume.UnregisterControlChangeNotify(volume_callback_obj)
                print(f"INFO: Volume callback unregistered for device {device_id}")
            except COMError as e:
                cls._print_exc_once_cls(
                    f"Failed to unregister volume callback for {device_id}: {e.hresult:#0x} {e.text}"
                )

    @classmethod
    def _internal_system_event_handler(
        cls, event_type: str, device_id: Optional[str], data: Optional[Any]
    ):
        """Обрабатывает системные события и управляет volume callbacks, затем вызывает пользовательский обработчик."""

        # Логика управления volume callbacks
        if device_id:  # Только если есть ID устройства
            if event_type == "device_added":
                try:
                    dev_ptr = cls.get_device_by_id(device_id)
                    if (
                        dev_ptr
                        and cls.get_device_state_value(dev_ptr)
                        == AudioDeviceState.Active.value
                    ):
                        cls._register_volume_callback_for_device(device_id, dev_ptr)
                except Exception as e:
                    cls._print_exc_once_cls(
                        f"Error processing device_added for volume CB {device_id}: {e}"
                    )

            elif event_type == "device_removed":
                cls._unregister_volume_callback_for_device(device_id)

            elif event_type == "device_state_changed":
                new_state_str = data.get("new_state", "") if data else ""
                if (
                    new_state_str == AudioDeviceState.Active.name.lower()
                ):  # Если стал активным
                    try:
                        dev_ptr = cls.get_device_by_id(device_id)
                        if dev_ptr:
                            cls._register_volume_callback_for_device(device_id, dev_ptr)
                    except Exception as e:
                        cls._print_exc_once_cls(
                            f"Error processing state_changed (to active) for volume CB {device_id}: {e}"
                        )

                # Если стал неактивным, отключенным, удаленным и т.д.
                elif new_state_str in [
                    AudioDeviceState.Disabled.name.lower(),
                    AudioDeviceState.NotPresent.name.lower(),
                    AudioDeviceState.Unplugged.name.lower(),
                ]:
                    cls._unregister_volume_callback_for_device(device_id)

        # Вызываем пользовательский обработчик, если он есть
        if cls._user_registered_event_handler:
            try:
                cls._user_registered_event_handler(event_type, device_id, data)
            except Exception:
                cls._print_exc_once_cls(
                    "Error in user-registered event handler via _internal_system_event_handler"
                )

    @classmethod
    def _register_device_notification_callback(cls) -> None:
        """Registers device notification callback with COM."""
        enumerator = cls._get_device_enumerator()

        if cls._notification_client_com_obj is None:
            cls._external_event_handler = cls._internal_system_event_handler
            cls._notification_client_com_obj = _WindowsAudioNotificationClientInternal()

            try:
                enumerator.RegisterEndpointNotificationCallback(
                    cls._notification_client_com_obj
                )
            except COMError as e:
                cls._notification_client_com_obj = None
                cls._external_event_handler = None
                cls._user_registered_event_handler = None
                raise RuntimeError(
                    f"Failed to register COM notification callback: {e}"
                ) from e

    @classmethod
    def _unregister_device_notification_callback(cls) -> None:
        """Unregisters device notification callback from COM."""
        if cls._notification_client_com_obj and cls._device_enumerator_instance:
            try:
                cls._device_enumerator_instance.UnregisterEndpointNotificationCallback(
                    cls._notification_client_com_obj
                )
            except COMError:
                cls._print_exc_once_cls(
                    "Error during UnregisterEndpointNotificationCallback in WinAudioAPI.unregister"
                )

        if cls._notification_client_com_obj is not None:
            cls._notification_client_com_obj = None

        cls._external_event_handler = None

    @classmethod
    def _register_volume_notification_callback(
        cls, device_id: str, imm_device_ptr: "POINTER[IMMDevice]"
    ) -> None:
        """Registers volume notification callback for a specific device."""
        cls._register_volume_callback_for_device(device_id, imm_device_ptr)

    @classmethod
    def _unregister_volume_notification_callback(cls, device_id: str) -> None:
        """Unregisters volume notification callback for a specific device."""
        cls._unregister_volume_callback_for_device(device_id)

    @classmethod
    def register_callbacks(
        cls, user_handler: Callable[[str, Optional[str], Optional[Any]], None]
    ) -> None:
        """Registers all callbacks (both device and volume notifications) with the provided user handler."""
        cls._user_registered_event_handler = user_handler
        cls._register_device_notification_callback()

        # Register volume callbacks for all active devices
        try:
            active_devices = cls.get_all_capture_devices()
            for dev_ptr in active_devices:
                dev_id = cls.get_device_id(dev_ptr)
                if cls.get_device_state_value(dev_ptr) == AudioDeviceState.Active.value:
                    cls._register_volume_notification_callback(dev_id, dev_ptr)
        except Exception as e:
            cls._print_exc_once_cls(
                f"Error registering volume callbacks during register_callbacks: {e}"
            )

    @classmethod
    def unregister_callbacks(cls) -> None:
        """Unregisters all callbacks (both device and volume notifications)."""
        # Unregister all volume callbacks
        all_device_ids_with_vol_cb = list(cls._active_volume_callbacks.keys())
        for dev_id in all_device_ids_with_vol_cb:
            cls._unregister_volume_notification_callback(dev_id)
        cls._active_volume_callbacks.clear()

        # Unregister device notification callback
        cls._unregister_device_notification_callback()
        cls._user_registered_event_handler = None
