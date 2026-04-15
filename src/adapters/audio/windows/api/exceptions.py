# src/platform/winos/api/exceptions.py

from typing import Optional


class WinApiError(Exception):
    """Base class for Windows API related errors."""

    pass


class WindowsAudioNotificationClientError(WinApiError):
    """Raised when a Windows audio notification client error occurs."""

    def __init__(self, device_id: str, message: Optional[str] = None):
        self.device_id = device_id
        super().__init__(
            message or f"Audio notification client error for device ID '{device_id}'."
        )


class WindowsAudioCOMError(WinApiError):
    """Raised when a Windows COM error occurs."""

    def __init__(
        self,
        message: Optional[str] = None,
        function: Optional[str] = None,
        hr: Optional[str] = None,
    ):
        if message and function and hr:
            msg = f"{message} (Function: {function}, HRESULT: {hr})"
        elif message and function:
            msg = f"{message} (Function: {function})"
        elif message and hr:
            msg = f"{message} (HRESULT: {hr})"
        elif function and hr:
            msg = f"An error occurred in function '{function}' with HRESULT '{hr}'."
        elif function:
            msg = f"An error occurred in function '{function}'."
        elif hr:
            msg = f"An error occurred with HRESULT '{hr}'."
        else:
            msg = message or "An unspecified COM error occurred."
        super().__init__(msg)
