from ctypes import byref, memmove, sizeof

from src.adapters.audio.windows.api.structures import (
    WAVEFORMATEX, KSJACK_DESCRIPTION, PROPVARIANT, GUID
)

def parse_complex_property(key_name: str, prop_var: PROPVARIANT):
    """
    Интеллектуальный парсинг значения в зависимости от имени ключа.
    """
    val = prop_var

    # 1. Если значение уже нормальное (int, str, bool) - просто возвращаем
    if not isinstance(val, bytes): 
        # Обработка GUID (CLSID), если GetValue вернул объект GUID
        if isinstance(val, GUID):
            return str(val)
        return val

    # Если мы здесь, значит val - это bytes (VT_BLOB), и нам нужно его расшифровать
    # Используем имя ключа как подсказку

    try:
        # --- ФОРМАТЫ ЗВУКА (AudioEngine) ---
        if "Format" in key_name:
            # Превращаем байты обратно в структуру WAVEFORMATEX
            wf = WAVEFORMATEX()
            # Осторожно: проверяем размер
            if len(val) >= sizeof(WAVEFORMATEX):
                memmove(byref(wf), val, sizeof(WAVEFORMATEX))
                return str(wf) # Используем наш красивый __str__
            return f"Blob[{len(val)} bytes] (Too small for WaveFormat)"

        # --- ОПИСАНИЕ ГНЕЗДА (Jack Description) ---
        elif "Jack_Description" in key_name:
            jack = KSJACK_DESCRIPTION()
            if len(val) >= sizeof(KSJACK_DESCRIPTION):
                memmove(byref(jack), val, sizeof(KSJACK_DESCRIPTION))
                return str(jack)
            
        # --- ФОРМ-ФАКТОР (FormFactor) ---
        # Обычно это Enum (число), но иногда приходит как blob
        elif "FormFactor" in key_name:
            # Обычно это просто int (VT_UI4), но если blob - это может быть 4 байта int
            if len(val) == 4:
                return int.from_bytes(val, byteorder='little')

    except Exception as e:
        return f"ParseError: {e}"

    # Если не знаем, что это - возвращаем просто размер блоба
    return f"RawBlob<{len(val)} bytes>"