# src/core/repositories.py

import abc
from typing import Optional, Tuple, Callable

from src.core.entites import Microphone, AppSettings


class SettingsRepository(abc.ABC):
    """
    Repo for working with persistent storage of app data.
    """

    @abc.abstractmethod
    def save(self, settings: AppSettings) -> None:
        """Saves `settings` object to the persistent storage."""
        raise NotImplementedError

    @abc.abstractmethod
    def load(self) -> AppSettings:
        """
        Loads `settings` object from persistent storage.

        If the storage is empty, returns `settings` object with fields
        defined by default.

        Returns:
            AppSettings: settings object with all sub-params included.
        """
        raise NotImplementedError


class AudioDeviceRepository(abc.ABC):
    """
    Audio Device Manager and Repositiry.
    """

    @abc.abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def uninitialize(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_devices(self):
        """
        Loads input devices collection from system.

        Returns:
            Tuple[Microphone]: tuple with all system input devices collection.

        Raises:
            NoInputDevicesAvailable: when there are no input devices available in the system
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_device_by_id(self, device_id: str):
        """
        Returns the input device object by its ID.
        
        Args:
            device_id (str): system unique ID of the device.

        Returns:
            Optional[Microphone]: the `Microphone` object. If not found, returns `None`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_default_device(self):
        """
        Returns the current default input device set in system.

        Returns:
            Optional[Microphone]: the `Microphone` object. If not found, returns `None`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_default_device(self, device_id: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_device_mute(self, device_id: str=None) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_device_volume(self, device_id: str=None) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def set_device_mute(self, is_muted: bool, device_id: str=None) -> bool:
        """
        Changes the mute state of device with `device_id` to `is_muted` state.

        If the `device_id` is not specified, muting effect will be done for the
        current active input device, e.g. "device by default".

        Returns:
            bool: success/unsuccess muting.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_device_volume(self, level: float, device_id: str=None) -> bool:
        """
        Changes the volume scalar of device with `device_id` to `level`.
        
        If the `device_id` is not specified, volume changing effect will be done
        for the current active input device, e.g. "device by default".

        Returns:
            bool: success/unsuccess volume changing.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def register_devices_event_handler(self, external_event_handler: Callable) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def unregister_devices_event_handler(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_device_name(self, device_id: str) -> str:
        raise NotImplementedError