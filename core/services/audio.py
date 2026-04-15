import sys
import logging
import threading

from comtypes import CoUninitialize, CoInitialize, GUID
from pycaw.callbacks import AudioEndpointVolumeCallback, MMNotificationClient
from pycaw.constants import DEVICE_STATE
from pycaw.pycaw import (
    AudioUtilities, EDataFlow, ERole,
    AudioDevice, IAudioEndpointVolume, IMMDeviceEnumerator
)
from PyQt6.QtCore import QObject, pyqtSignal

from core.events import EventBus


sys.coinit_flags = 0


class InternalAudioOSBus(QObject):
    devices_list_changed = pyqtSignal(dict)
    default_device_changed = pyqtSignal(str)


class AudioInputService(QObject):
    def __init__(self, bus: EventBus) -> None:
        super().__init__()

        self._bus = bus
        self._internal_bus = InternalAudioOSBus()

        self.__device_callback: _DeviceCallback = None
        self.__volume_callback: _VolumeCallback = None

        self.__enumerator: IMMDeviceEnumerator = None
        self.__microphone_interface: IAudioEndpointVolume = None

        self.__cache_lock = threading.Lock()
        self.__cached_microphone: AudioDevice = None
        self.__cached_devices: list[AudioDevice] = None

        # Connect commands from orchestrator to slots
        self._bus.shared.cmd_set_mic_mute.connect(self.set_mute)
        self._bus.shared.cmd_set_default_mic.connect(self.set_default_device)

        # OS events
        self._internal_bus.devices_list_changed.connect(self._on_device_change)
        self._internal_bus.default_device_changed.connect(self._on_device_change)

    def initialize(self) -> None:
        """Fetch microphone and devices in background thread."""

        logging.info("AudioInputService starting...")
        try:
            CoInitialize()
            self.__enumerator = AudioUtilities.GetDeviceEnumerator()
        except Exception as e:
            logging.error("AudioInputService failed to initialize: %s", e)

        try:
            self.get_all_devices() # caching all devices on init
            self.__register_callbacks() # register callback for default device on init 
            
            # init
            self._internal_bus.devices_list_changed.emit(dict())
            self._internal_bus.default_device_changed.emit(self.__cached_microphone.id)
            # self._bus.shared.app_mic_state_updated.emit(self.is_muted())

        except Exception:
            raise

    def __invalidate_cache(self) -> None:
        """Clear cached data when devices change."""
        with self.__cache_lock:
            self.__cached_microphone = None
            self.__cached_devices = None

    def __get_microphone_device(self) -> AudioDevice | None:
        """
        Get default microphone as AudioDevice.
        Returns None if no mic available.
        """
        with self.__cache_lock:
            if self.__cached_microphone is None:
                mic_pointer = AudioUtilities.GetMicrophone()
                if mic_pointer:
                    mic = AudioUtilities.CreateDevice(mic_pointer)
                if mic:
                    self.__cached_microphone = mic
                    return self.__cached_microphone
                return None
            return self.__cached_microphone

    def __get_microphone_interface(self) -> IAudioEndpointVolume | None:
        """Get volume control interface for microphone."""
        if self.__microphone_interface is None:
            mic = self.__get_microphone_device()
            logging.warning(f"MIC: {mic}")
            if mic:
                try:
                    self.__microphone_interface = mic.EndpointVolume
                    return self.__microphone_interface
                except Exception:
                    pass
            return None
        return self.__microphone_interface

    def __register_callbacks(self) -> None:
        """Hook up device and volume change notifications."""
        try:
            if self.__enumerator and not self.__device_callback:
                self.__device_callback = _DeviceCallback(self._internal_bus)
                self.__enumerator.RegisterEndpointNotificationCallback(self.__device_callback)

            volume = self.__get_microphone_interface()
            if volume and not self.__volume_callback:
                self.__volume_callback = _VolumeCallback(self._bus)
                volume.RegisterControlChangeNotify(self.__volume_callback)
        except Exception:
            pass

    def __unregister_callbacks(self) -> None:
        """Unhook device and volume notifications."""
        try:
            if self.__device_callback and self.__enumerator:
                self.__enumerator.UnregisterEndpointNotificationCallback(self.__device_callback)
                self.__device_callback = None

            if self.__volume_callback and self.__microphone_interface:
                self.__microphone_interface.UnregisterControlChangeNotify(self.__volume_callback)
                self.__volume_callback = None
        except Exception:
            pass

    def _on_device_change(self, payload) -> None:
        """Handle audio device add/remove/change."""
        # Unregister old volume callback
        if self.__volume_callback and self.__microphone_interface:
            try:
                self.__microphone_interface.UnregisterControlChangeNotify(self.__volume_callback)
            except Exception:
                pass
            self.__volume_callback = None

        # Clear cached data and interface
        self.__invalidate_cache()
        self.__microphone_interface = None

        # Get new microphone (may be None if no mic connected)
        mic = self.__get_microphone_device()
        if mic:
            try:
                self.__microphone_interface = mic.EndpointVolume
                with self.__cache_lock:
                    self.__cached_microphone = mic
            except Exception as e:
                logging.warning(e)

        # Re-register volume callback if we have a mic
        if self.__microphone_interface:
            try:
                self.__volume_callback = _VolumeCallback(self._bus)
                self.__microphone_interface.RegisterControlChangeNotify(self.__volume_callback)
            except Exception as e:
                logging.warning(e)
        
        if isinstance(payload, dict):
            devices = self.get_all_devices()
            self._bus.shared.os_devices_list_changed.emit(devices)
        elif isinstance(payload, str):
            self._bus.shared.os_default_mic_changed.emit(payload)

        self._bus.shared.os_mic_state_changed.emit(self.is_muted()) # ?? (in callback we have the same logic)
    
    def get_device_name(self, device_id: str) -> str | None:
        """Get device FriendlyName"""
        try:
            devices = self.get_all_devices()
            if devices:
                return devices[device_id]
        except Exception as e:
            logging.error("Failed to get dev_name: %s", e)
            raise
        return None

    def get_all_devices(self) -> dict[str, str]:
        """List all active microphone devices."""
        with self.__cache_lock:
            if self.__cached_devices is not None:
                return self.__cached_devices

        try:
            devices: list[AudioDevice] = AudioUtilities.GetAllDevices(
                data_flow=EDataFlow.eCapture.value,
                device_state=DEVICE_STATE.ACTIVE.value
            )
            result = {d.id:d.FriendlyName for d in devices}
            with self.__cache_lock:
                self.__cached_devices = result
            return result
        except Exception:
            return dict()

    def set_default_device(self, device_id: str) -> bool:
        """
        Switch default microphone.
        Returns True on success, False otherwise.
        """
        try:
            AudioUtilities.SetDefaultDevice(device_id, roles=[ERole.eConsole])
            self._bus.shared.answ_set_default_mic.emit(device_id) # sucess
        except Exception as e:
            logging.error("Failed to set default microphone: %s", e)
            self._bus.shared.answ_set_default_mic.emit(None)

    def set_mute(self, state: bool) -> bool:
        """Toggle mute state of the microphone."""
        try:
            interface = self.__get_microphone_interface()
            if interface:
                interface.SetMute(state, None)

                self._bus.shared.answ_set_mic_mute.emit(state) # sucess
        except Exception as e:
            logging.error("Failed to set mute of microphone: %s", e)
            self._bus.shared.answ_set_mic_mute.emit(None)

    def is_muted(self) -> bool:
        """
        Check if microphone is muted.
        Returns True if muted, False otherwise.
        """
        try:
            interface = self.__get_microphone_interface()
            if interface:
                return bool(interface.GetMute())
        except Exception as e:
            logging.error("Failed to get mic status: %s", e)
        return True  # Safe default (considered muted)

    def cleanup(self) -> None:
        self.__unregister_callbacks()
        CoUninitialize()


class _VolumeCallback(AudioEndpointVolumeCallback):
    """Forwards volume changes to the service."""

    def __init__(self, bus: EventBus):
        super().__init__()
        self._bus = bus
        self._last_device_mute = None

    def on_notify(self, new_volume, new_mute, event_context, channels, channel_volumes):
        # supress callbacks about volume changes (for now)
        if bool(new_mute) != self._last_device_mute:

            self._bus.shared.os_mic_state_changed.emit(bool(new_mute))
            self._last_device_mute = bool(new_mute)


class _DeviceCallback(MMNotificationClient):
    """Forwards device changes to the service."""

    friendly_name_fmtid = GUID('{A45C254E-DF1C-4EFD-8020-67D146A850E0}')

    def __init__(self, internal_bus: InternalAudioOSBus):
        super().__init__()
        self._bus = internal_bus
        self._last_def_device_id = None

    def on_default_device_changed(self, flow, flow_id, role, role_id, default_device_id):
        """Handle default microphone device changes."""
        # Only care about capture (input) devices with console role
        if flow_id != EDataFlow.eCapture.value or role_id != ERole.eConsole.value:
            return
        # Deduplicate rapid events
        if default_device_id == self._last_def_device_id:
            return
        self._last_def_device_id = default_device_id

        self._bus.default_device_changed.emit(self._last_def_device_id)

    def on_device_state_changed(self, device_id, new_state, new_state_id):
        """Handle device state changes (connected/disconnected)."""
        # React to Active, Disabled, and Unplugged states
        if new_state_id not in (
            DEVICE_STATE.ACTIVE.value,
            DEVICE_STATE.DISABLED.value,
            DEVICE_STATE.UNPLUGGED.value
        ):
            return
        self._bus.devices_list_changed.emit(dict())

    def on_property_value_changed(self, device_id, property_struct, fmtid, pid):
        """
        Hadnler of device property changes.
        Now it's handling only device.FriendlyName changes.
        """
        if fmtid == self.friendly_name_fmtid and pid == 2:
            self._bus.devices_list_changed.emit(dict())
