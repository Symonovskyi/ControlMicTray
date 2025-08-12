# src/adapters/audio/factory.py

import platform
from typing import Type, Any


def get_audio_adapter() -> Type[Any]:
    """
    Returns the appropriate audio API wrapper based on the current operating system.

    Returns:
        Type[Any]: The audio API wrapper class for the current platform

    Raises:
        NotImplementedError: If the current platform is not supported
    """
    system = platform.system().lower()

    if system == "windows":
        # from src.adapters.audio.windows import WinAudioAPI
        # return WinAudioAPI
        raise NotImplementedError(
                f"Audio API wrapper is not available for platform: {system}"
            )

    elif system == "darwin":
        # from src.adapters.audio.macos import MacOSAudioAPI
        # return MacOSAudioAPI
        raise NotImplementedError(
            f"Audio API wrapper is not available for platform: {system}"
        )

    elif system in ["linux", "unix"]:
        # from src.adapters.audio.unix import UnixAudioAPI
        # return UnixAudioAPI
        raise NotImplementedError(
            f"Audio API wrapper is not available for platform: {system}"
        )

    else:
        raise NotImplementedError(
            f"Audio API wrapper is not available for platform: {system}"
        )
