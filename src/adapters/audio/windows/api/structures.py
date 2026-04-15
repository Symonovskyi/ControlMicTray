from typing import TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime, timedelta

from ctypes import (
    Structure, Union, POINTER, string_at,
    c_char, c_ubyte, c_short, c_ushort, c_long, c_ulong,
    c_int, c_uint, c_float, c_double, c_void_p, c_wchar_p
)
from ctypes.wintypes import (
    ULONG,
    LPWSTR,
    LPSTR,
    ULARGE_INTEGER,
    LARGE_INTEGER,
    VARIANT_BOOL,
    WORD,
    FILETIME,
    BYTE,
    DWORD,
    BOOL,
    UINT,
    INT
)
from comtypes import GUID, IUnknown
from comtypes.automation import (
    VARTYPE, BSTR, CY, DECIMAL, SCODE,
    VT_EMPTY, VT_NULL, VT_I1, VT_UI1, VT_I2, VT_UI2, VT_I4, VT_UI4,
    VT_INT, VT_UINT, VT_I8, VT_UI8, VT_R4, VT_R8,
    VT_BOOL, VT_ERROR, VT_CY, VT_FILETIME,
    VT_CLSID, VT_BSTR, VT_BLOB,
    VT_LPSTR, VT_LPWSTR, VT_UNKNOWN, VT_DISPATCH, VT_STREAM, VT_STORAGE,
    VT_VECTOR, VT_DECIMAL
)


# Эпоха FILETIME - 1 января 1601
FILETIME_EPOCH = datetime(1601, 1, 1)

def filetime_to_datetime(ft: FILETIME) -> datetime:
    """Конвертирует ctypes FILETIME в объект datetime Python."""
    # Собираем 64-битное значение из двух 32-битных частей
    # ft.dwHighDateTime << 32 | ft.dwLowDateTime
    microseconds = (ft.dwHighDateTime << 32 | ft.dwLowDateTime) / 10
    
    # Добавляем микросекунды к эпохе
    return FILETIME_EPOCH + timedelta(microseconds=microseconds)


class IDispatch(IUnknown):
    pass

class PROPVARIANT(Structure):
    pass

class BLOB(Structure):
    _fields_ = [
        ("cbSize", ULONG),
        ("pBlobData", POINTER(BYTE)),
    ]

class CLIPDATA(Structure):
    _fields_ = [
        ("cbSize", ULONG),
        ("ulClipFmt", c_long),
        ("pClipData", POINTER(BYTE)),
    ]

class BSTRBLOB(Structure):
    _fields_ = [
        ("cbSize", ULONG),
        ("pData", POINTER(BYTE)),
    ]


class CAC(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(c_char))] # noqa: E701
class CAUB(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(c_ubyte))] # noqa: E701
class CAI(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(c_short))] # noqa: E701
class CAUI(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(c_ushort))] # noqa: E701
class CAL(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(c_long))] # noqa: E701
class CAUL(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(c_ulong))] # noqa: E701
class CAH(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(LARGE_INTEGER))] # noqa: E701
class CAUH(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(ULARGE_INTEGER))] # noqa: E701
class CAFLT(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(c_float))] # noqa: E701
class CADBL(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(c_double))] # noqa: E701
class CABOOL(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(VARIANT_BOOL))] # noqa: E701
class CASCODE(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(SCODE))] # noqa: E701
class CACY(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(CY))] # noqa: E701
class CADATE(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(c_double))] # noqa: E701
class CAFILETIME(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(FILETIME))] # noqa: E701
class CACLSID(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(GUID))] # noqa: E701
class CACLIPDATA(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(CLIPDATA))] # noqa: E701
class CABSTR(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(BSTR))] # noqa: E701
class CABSTRBLOB(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(BSTRBLOB))] # noqa: E701
class CALPSTR(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(LPSTR))] # noqa: E701
class CALPWSTR(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(LPWSTR))] # noqa: E701
class CAPROPVARIANT(Structure): _fields_ = [("cElems", ULONG), ("pElems", POINTER(PROPVARIANT))] # noqa: E701


class PROPVARIANT_UNION(Union):
    _fields_ = [
        ("cVal", c_char), ("bVal", c_ubyte), ("iVal", c_short), ("uiVal", c_ushort),
        ("lVal", c_long), ("ulVal", c_ulong), ("intVal", c_int), ("uintVal", c_uint),
        ("hVal", LARGE_INTEGER), ("uhVal", ULARGE_INTEGER), ("fltVal", c_float),
        ("dblVal", c_double), ("boolVal", VARIANT_BOOL), ("scode", SCODE), ("cyVal", CY),
        ("date", c_double), ("filetime", FILETIME), ("puuid", POINTER(GUID)),
        ("pclipdata", POINTER(CLIPDATA)), ("bstrVal", BSTR), ("bstrblobVal", BSTRBLOB),
        ("blob", BLOB), ("pszVal", LPSTR), ("pwszVal", LPWSTR), ("punkVal", POINTER(IUnknown)),
        ("pdispVal", POINTER(IDispatch)), ("pStream", c_void_p), ("pStorage", c_void_p),
        ("pVersionedStream", c_void_p), ("parray", c_void_p),
        
        ("cac", CAC), ("caub", CAUB), ("cai", CAI), ("caui", CAUI),
        ("cal", CAL), ("caul", CAUL), ("cah", CAH), ("cauh", CAUH),
        ("caflt", CAFLT), ("cadbl", CADBL), ("cabool", CABOOL),
        ("cascode", CASCODE), ("cacy", CACY), ("cadate", CADATE),
        ("cafiletime", CAFILETIME), ("cauuid", CACLSID), ("caclipdata", CACLIPDATA),
        ("cabstr", CABSTR), ("cabstrblob", CABSTRBLOB), ("calpstr", CALPSTR),
        ("calpwstr", CALPWSTR), ("capropvar", CAPROPVARIANT),

        ("pcVal", POINTER(c_char)), ("pbVal", POINTER(c_ubyte)),
        ("piVal", POINTER(c_short)), ("puiVal", POINTER(c_ushort)),
        ("plVal", POINTER(c_long)), ("pulVal", POINTER(c_ulong)),
        ("pintVal", POINTER(c_int)), ("puintVal", POINTER(c_uint)),
        ("pfltVal", POINTER(c_float)), ("pdblVal", POINTER(c_double)),
        ("pboolVal", POINTER(VARIANT_BOOL)), ("pdecVal", POINTER(DECIMAL)),
        ("pscode", POINTER(SCODE)), ("pcyVal", POINTER(CY)),
        ("pdate", POINTER(c_double)), ("pbstrVal", POINTER(BSTR)),
        ("ppunkVal", POINTER(POINTER(IUnknown))), ("ppdispVal", POINTER(POINTER(IDispatch))),
        ("pparray", POINTER(c_void_p)), ("pvarVal", POINTER(PROPVARIANT)),
    ]


class PROPVARIANT(Structure):
    _fields_ = [
        ("vt", VARTYPE),
        ("reserved1", WORD),
        ("reserved2", WORD),
        ("reserved3", WORD),
        ("union", PROPVARIANT_UNION),
    ]

    def GetValue(self):
        try:
            base_vt = self.vt & 0xFFF

            if self.vt & VT_VECTOR:
                if base_vt == VT_UI1: # VT_VECTOR | VT_UI1
                    ca = self.union.caub
                    return [ca.pElems[i] for i in range(ca.cElems)]
                elif base_vt == VT_UI2: # VT_VECTOR | VT_UI2
                    ca = self.union.caui
                    return [ca.pElems[i] for i in range(ca.cElems)]
                elif base_vt == VT_UI4: # VT_VECTOR | VT_UI4
                    ca = self.union.caul
                    return [ca.pElems[i] for i in range(ca.cElems)]
                elif base_vt == VT_LPWSTR: # VT_VECTOR | VT_LPWSTR
                    ca = self.union.calpwstr
                    return [ca.pElems[i] for i in range(ca.cElems)]
                elif base_vt == VT_BSTR: # VT_VECTOR | VT_BSTR
                    ca = self.union.cabstr
                    return [ca.pElems[i] for i in range(ca.cElems)]
                elif base_vt == VT_FILETIME: # VT_VECTOR | VT_FILETIME
                    ca = self.union.cafiletime
                    if not ca.pElems:
                        return []
                    return [ca.pElems[i] for i in range(ca.cElems)]
                else:
                    return f"Unsupported VT_VECTOR type: {base_vt}"

            if base_vt == VT_EMPTY or base_vt == VT_NULL:
                return None
            elif base_vt == VT_I1:
                return self.union.cVal
            elif base_vt == VT_UI1:
                return self.union.bVal
            elif base_vt == VT_I2:
                return self.union.iVal
            elif base_vt == VT_UI2:
                return self.union.uiVal
            elif base_vt == VT_I4:
                return self.union.lVal
            elif base_vt == VT_UI4:
                return self.union.ulVal
            elif base_vt == VT_INT:
                return self.union.intVal
            elif base_vt == VT_UINT:
                return self.union.uintVal
            elif base_vt == VT_I8:
                return self.union.hVal
            elif base_vt == VT_UI8:
                return self.union.uhVal
            elif base_vt == VT_R4:
                return self.union.fltVal
            elif base_vt == VT_R8:
                return self.union.dblVal
            elif base_vt == VT_BOOL:
                return self.union.boolVal != 0
            elif base_vt == VT_ERROR:
                return self.union.scode
            elif base_vt == VT_CY:
                return self.union.cyVal
            elif base_vt == VT_FILETIME:
                try:
                    flt = self.union.filetime
                    dt_obj = filetime_to_datetime(flt)
                    return dt_obj.strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    print(f"Exception!: {e}")
            elif base_vt == VT_CLSID:
                return GUID.from_buffer_copy(self.union.puuid.contents)
            elif base_vt == VT_BLOB:
                blob = self.union.blob
                return string_at(blob.pBlobData, blob.cbSize)
            elif base_vt == VT_BSTR:
                return self.union.bstrVal
            elif base_vt == VT_DECIMAL:
                return self.decVal
            elif base_vt == VT_UNKNOWN:
                return self.union.punkVal
            elif base_vt == VT_DISPATCH:
                return self.union.pdispVal
            elif base_vt == VT_LPWSTR:
                return self.union.pwszVal
            elif base_vt == VT_LPSTR:
                return self.union.pszVal
            elif base_vt == VT_STREAM or base_vt == VT_STORAGE:
                return self.union.pStream
            else:
                return f"Unknown VARTYPE: {self.vt}"
        except Exception as e:
            print(e)
            return

class PROPERTYKEY(Structure):
    _fields_ = [
        ("fmtid", GUID),
        ("pid", DWORD),
    ]

    if TYPE_CHECKING:
        fmtid: GUID
        pid: str

    def __str__(self):
        return "fmtid: %s\npid:%s" % (self.fmtid, self.pid)


class KSJACK_DESCRIPTION(Structure):
    _fields_ = [
        ("ChannelMapping", DWORD),
        ("Color", DWORD),      # Цвет гнезда (0x00FF00 = Green)
        ("ConnectionType", DWORD),
        ("GeoLocation", DWORD), # Спереди, сзади, HDMI и т.д.
        ("GenLocation", DWORD),
        ("PortConnection", DWORD),
        ("IsConnected", BOOL),
    ]

    def __str__(self):
        # Простая расшифровка локации
        loc_map = {0: "Rear", 1: "Front", 2: "Left", 3: "Right", 4: "Top", 5: "Bottom"}
        loc = loc_map.get(self.GeoLocation, f"Unk({self.GeoLocation})")
        connected = "Plugged" if self.IsConnected else "Unplugged"
        return f"<Jack: {loc} Panel, Color: {hex(self.Color)}, {connected}>"


class WAVEFORMATEX(Structure):
    _fields_ = [
        ("wFormatTag", WORD),
        ("nChannels", WORD),
        ("nSamplesPerSec", WORD),
        ("nAvgBytesPerSec", WORD),
        ("nBlockAlign", WORD),
        ("wBitsPerSample", WORD),
        ("cbSize", WORD),
    ]

    if TYPE_CHECKING:
        wFormatTag: str
        nChannels: str
        nSamplesPerSec: str
        nAvgBytesPerSec: str
        nBlockAlign: str
        wBitsPerSample: str
        cbSize: str

    def __str__(self):
        return (f"<WAVEFORMATEX: {self.nSamplesPerSec}Hz, "
                f"{self.wBitsPerSample}bit, {self.nChannels}ch>")


class AUDIO_VOLUME_NOTIFICATION_DATA(Structure):
    _fields_ = [
        ("guidEventContext", GUID),
        ("bMuted", BOOL),
        ("fMasterVolume", c_float),
        ("nChannels", UINT),
        ("afChannelVolumes", c_float * 8),
    ]

    if TYPE_CHECKING:
        @dataclass
        class contents:
            guidEventContext: GUID
            bMuted: bool
            fMasterVolume: float
            nChannels: int
            afChannelVolumes: list[float]
    
    # def __str__(self):
    #     return (f"<AUDIO_VOLUME_NOTIFICATION_DATA: MuteState: {self.contents.bMuted}, "
    #             f"MasterVolume: {self.contents.fMasterVolume}")


class DEVICE_SHARED_MODE(Structure):
    _fields_ = [("dummy_", INT)]


class IPolicyPropertyKey(Structure):
    pass


class IPolicyPropVariant(Structure):
    pass
