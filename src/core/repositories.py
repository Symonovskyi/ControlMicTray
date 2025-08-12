# src/core/repositories.py

import abc
from typing import Optional, Tuple

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
    def get_all_devices(self) -> Tuple[Microphone]:
        """
        Loads input devices collection from system.

        Returns:
            Tuple[Microphone]: tuple with all system input devices collection.

        Raises:
            NoInputDevicesAvailable: when there are no input devices available in the system
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_device_by_id(self, mic_id: str) -> Optional[Microphone]:
        """
        Returns the input device object by its ID.
        
        Args:
            mic_id (str): system unique ID of the device.

        Returns:
            Optional[Microphone]: the `Microphone` object. If not found, returns `None`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_default_device(self) -> Optional[Microphone]:
        """
        Returns the current default input device set in system.

        Returns:
            Optional[Microphone]: the `Microphone` object. If not found, returns `None`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_device_mute(self, is_muted: bool, mic_id: str=None) -> bool:
        """
        Changes the mute state of device with `mic_id` to `is_muted` state.

        If the `mic_id` is not specified, muting effect will be done for the
        current active input device, e.g. "device by default".

        Returns:
            bool: success/unsuccess muting.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_device_volume(self, level: float, mic_id: str=None) -> bool:
        """
        Changes the volume scalar of device with `mic_id` to `level`.
        
        If the `mic_id` is not specified, volume changing effect will be done
        for the current active input device, e.g. "device by default".

        Returns:
            bool: success/unsuccess volume changing.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_device_as_default(self, mic_id: str) -> bool:
        """
        Changes the current active input device to device with `mic_id`.

        Returns:
            bool: success/unsuccess setting device as default.
        """
        raise NotImplementedError
