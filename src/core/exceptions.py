# src/core/exceptions.py

from typing import Any


class ControlMicTrayError(Exception):
    """
    Base exception class for all the errors from the app.
    """

    pass


class CoreError(ControlMicTrayError):
    """
    Exception class for all the sub-errors coming from `core` layer.
    """

    pass


class EntityNotFoundError(CoreError):
    """
    Triggers when the entity was not found by its ID.
    """

    def __init__(self, entity_id: str, entity_type: str = "Entity"):
        self.entity_id = entity_id
        self.entity_type = entity_type
        super().__init__(f"{entity_type} with ID '{entity_id}' not found.")


class NoInputDevicesAvailable(CoreError):
    """
    Triggers when there are no input devices available in the system.
    """

    def __init__(self):
        super().__init__("There are no input devices available!")



class ValidationError(CoreError):
    """
    Exception class for all the validation sub-errors.
    """

    pass


class VolumeOutOfRangeError(ValidationError):
    """
    Triggers when the setting of volume value becomes out out of range or with
    unsupported data type.
    """

    def __init__(self, invalid_volume: Any):
        self.invalid_volume = invalid_volume
        super().__init__(
            f"Volume must be between 0.0 and 100.0, but got '{invalid_volume}'. Volume datatype: {type(invalid_volume)}"
        )
