from ctypes import POINTER, cast, HRESULT, c_float, sizeof
from ctypes.wintypes import BOOL, DWORD, UINT
import comtypes
from comtypes import CLSCTX_INPROC_SERVER, COMMETHOD, GUID, IUnknown

class IMMDevice(IUnknown):
    _iid_ = GUID("{D666063F-1587-4E43-81F1-B948E807363F}")
    _methods_ = ()

class IMMDeviceCollection(IUnknown):
    _iid_ = GUID("{0BD7A1BE-7A1A-44DB-8397-C0C0C78C1E16}")
    _methods_ = (
        COMMETHOD([], HRESULT, "GetCount", (['out'], POINTER(UINT), "pcDevices")),
        COMMETHOD([], HRESULT, "Item", (['in'], UINT, "nDevice"), (['out'], POINTER(POINTER(IMMDevice)), "ppDevice")),
    )

class IMMDeviceEnumerator(IUnknown):
    _iid_ = GUID("{A95664D2-9614-4F35-A746-DE8DB63617E6}")
    _methods_ = (
        COMMETHOD([], HRESULT, "EnumAudioEndpoints", (['in'], DWORD, "dataFlow"),
                  (['in'], DWORD, "dwStateMask"), (['out'], POINTER(POINTER(IMMDeviceCollection)), "ppDevices")),
        COMMETHOD([], HRESULT, "GetDefaultAudioEndpoint", (['in'], DWORD, "dataFlow"),
                  (['in'], DWORD, "role"), (['out'], POINTER(POINTER(IMMDevice)), "ppDevice")),
    )

class IAudioEndpointVolume(IUnknown):
    _iid_ = GUID("{5CDF2C82-841E-4546-9722-0CF74078229A}")
    _methods_ = (
        COMMETHOD([], HRESULT, "GetMute", (['out'], POINTER(BOOL), "pbMute")),
    )

class VideoConferenceModule:
    def __init__(self):
        try:
            self.enumerator = comtypes.CoCreateInstance(
                IMMDeviceEnumerator._iid_, IMMDeviceEnumerator, CLSCTX_INPROC_SERVER
            )
        except Exception as e:
            print(f"❌ Ошибка инициализации COM-объектов: {e}")
            self.enumerator = None
        
        self.toolbar = Toolbar()
        self.push_to_talk_pressed = False

    def get_all_microphones(self):
        if not self.enumerator:
            print("❌ COM-объект IMMDeviceEnumerator недоступен")
            return []
        try:
            devices = POINTER(IMMDeviceCollection)()
            hr = self.enumerator.EnumAudioEndpoints(1, 1, devices)  # 1 - Capture, 1 - Active devices
            if hr != 0:
                print(f"❌ Ошибка при перечислении устройств: {hr}")
                return []
            
            count = UINT()
            devices.GetCount(count)
            
            microphone_list = []
            for i in range(count.value):
                device = POINTER(IMMDevice)()
                devices.Item(i, device)
                microphone_list.append(f"Микрофон {i + 1}")  # Имя можно извлечь через IPropertyStore
            
            return microphone_list
        except Exception as e:
            print(f"❌ Ошибка при получении списка микрофонов: {e}")
            return []
    
    def get_default_audio_device(self, role=0):
        if not self.enumerator:
            print("❌ COM-объект IMMDeviceEnumerator недоступен")
            return None
        try:
            device = POINTER(IMMDevice)()
            hr = self.enumerator.GetDefaultAudioEndpoint(1, role, device)
            if hr != 0:
                print(f"❌ Ошибка получения устройства по умолчанию: {hr}")
                return None
            return device
        except Exception as e:
            print(f"❌ Ошибка получения устройства по умолчанию: {e}")
            return None

class Toolbar:
    def __init__(self):
        self.mic_muted = False
    
    def setMicrophoneMute(self, muted):
        self.mic_muted = muted
        print(f"🎤 Панель: микрофон {'🔴 МУТ' if muted else '🟢 ВКЛ'}")

# --- Тестируем ---
vc_module = VideoConferenceModule()
print("🎤 Доступные микрофоны:", vc_module.get_all_microphones())
print("🔊 Основной микрофон:", vc_module.get_default_audio_device(role=0))
print("📞 Микрофон для связи:", vc_module.get_default_audio_device(role=2))
