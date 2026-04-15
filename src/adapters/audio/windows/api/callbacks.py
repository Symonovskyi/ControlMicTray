import traceback
from src.adapters.audio.windows.api.coreaudio import (
    PublicDeviceVolumeNotificationClient, PublicAudioNotificationClient
)
from src.adapters.audio.windows.api.constants import ERole, EDataFlow, EAudioDeviceState
from src.adapters.audio.windows.api.parsers import parse_complex_property
from src.services.logger import logger

from ctypes import windll, POINTER, HRESULT, byref
from src.adapters.audio.windows.api.structures import PROPERTYKEY, c_wchar_p


from comtypes import GUID

def G(guid_str):
    return str(GUID(guid_str))

# =============================================================================
# WINDOWS CORE AUDIO PROPERTY KEYS DATABASE
# Sources: FunctionDiscoveryKeys_devpkey.h, Mmdeviceapi.h, Audioenginebaseapo.h
# =============================================================================

KNOWN_PROPERTY_KEYS = {
    # --- PKEY_AudioEndpoint (Свойства Эндпоинта) ---
    # Описывают физическую суть устройства (форм-фактор, динамики, ассоциации)
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 0): "PKEY_AudioEndpoint_FormFactor",
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 1): "PKEY_AudioEndpoint_ControlPanelPageProvider",
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 2): "PKEY_AudioEndpoint_Association",
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 3): "PKEY_AudioEndpoint_PhysicalSpeakers",
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 4): "PKEY_AudioEndpoint_GUID",
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 5): "PKEY_AudioEndpoint_Disable_SysFx",
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 6): "PKEY_AudioEndpoint_FullRangeSpeakers",
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 7): "PKEY_AudioEndpoint_Supports_EventDriven_Mode",
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 8): "PKEY_AudioEndpoint_JackSubType",
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 9): "PKEY_AudioEndpoint_Default_VolumeInDb",
    (G("{1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E}"), 10): "PKEY_AudioEndpoint_Auxiliary_VolumeInDb",

    # --- PKEY_AudioEngine (Настройки Аудио-Движка) ---
    # Самая активная группа при подключении. Это согласование частоты, битности и форматов.
    (G("{3D6E1656-2E50-4C4C-8D85-D0ACAE3C6C68}"), 0): "PKEY_AudioEngine_DeviceFormat",  # Текущий формат устройства
    (G("{3D6E1656-2E50-4C4C-8D85-D0ACAE3C6C68}"), 1): "PKEY_AudioEngine_DeviceFormat_PCM",
    (G("{3D6E1656-2E50-4C4C-8D85-D0ACAE3C6C68}"), 2): "PKEY_AudioEngine_DeviceFormat_IEEE_FLOAT",
    (G("{3D6E1656-2E50-4C4C-8D85-D0ACAE3C6C68}"), 3): "PKEY_AudioEngine_OEMFormat",     # "Родной" формат железа
    (G("{3D6E1656-2E50-4C4C-8D85-D0ACAE3C6C68}"), 4): "PKEY_AudioEngine_OEMFormat_PCM",
    (G("{3D6E1656-2E50-4C4C-8D85-D0ACAE3C6C68}"), 5): "PKEY_AudioEngine_OEMFormat_IEEE_FLOAT",
    (G("{3D6E1656-2E50-4C4C-8D85-D0ACAE3C6C68}"), 6): "PKEY_AudioEngine_LoopbackFormat", # Формат прослушивания (Loopback)
    (G("{3D6E1656-2E50-4C4C-8D85-D0ACAE3C6C68}"), 9): "PKEY_AudioEngine_WindowsAudioSession_Format", # Формат WASAPI сессии
    (G("{3D6E1656-2E50-4C4C-8D85-D0ACAE3C6C68}"), 10): "PKEY_AudioEngine_SupportedDeviceFormats", # Список всех поддерживаемых форматов

    # --- Дополнительные специфичные ключи (из твоих логов) ---
    # PKEY_AudioEndpoint_WavFormat - специфичные форматы Wave
    (G("{3F777207-7E55-4A2A-8A26-39E31D49BDC1}"), 0): "PKEY_AudioEndpoint_WavFormat_Specific", 
    (G("{3F777207-7E55-4A2A-8A26-39E31D49BDC1}"), 1): "PKEY_AudioEndpoint_WavFormat_Extensible",

    # PKEY_AudioEndpoint_Supports_... - возможности драйвера
    (G("{9C119480-DDC2-4954-A150-5BD240D454AD}"), 1): "PKEY_AudioEndpoint_FullRangeSpeakers_Config", 
    (G("{9C119480-DDC2-4954-A150-5BD240D454AD}"), 2): "PKEY_AudioEndpoint_Supported_Format_Ranges",
    (G("{9C119480-DDC2-4954-A150-5BD240D454AD}"), 9): "PKEY_AudioEndpoint_Offload_Stream_Modes",
    (G("{9C119480-DDC2-4954-A150-5BD240D454AD}"), 10): "PKEY_AudioEndpoint_Offload_Supported",

    # PKEY_KS (Kernel Streaming) - физические гнезда
    (G("{B3F8FA53-0004-438E-9003-51A46E139BFC}"), 24): "PKEY_KS_Jack_Description", # Куда воткнуто (Front/Rear)
    (G("{B3F8FA53-0004-438E-9003-51A46E139BFC}"), 27): "PKEY_KS_Jack_Sink_Info",   # Инфо о приемнике (для HDMI/DP)

    # --- Системные и общие ключи ---
    (G("{A45C254E-DF1C-4EFD-8020-67D146A850E0}"), 2): "PKEY_Device_DeviceDesc",
    (G("{A45C254E-DF1C-4EFD-8020-67D146A850E0}"), 14): "PKEY_Device_FriendlyName",
    
    # Internal Driver / Package Keys (часто встречаются как Unknown в логах)
    (G("{624F56DE-FD24-473E-814A-DE40AACAED16}"), 3): "PKEY_AudioEndpoint_Package_Association", # Связь с пакетом драйверов
    (G("{194EF948-7CDB-403E-9F47-19418F7B24FD}"), 1): "PKEY_AudioEndpoint_PhysicalSpeakers_Config_Caps",
    (G("{194EF948-7CDB-403E-9F47-19418F7B24FD}"), 2): "PKEY_AudioEndpoint_PhysicalSpeakers_Config_Mask",

    # Device Interface
    (G("{026E516E-B814-414B-83CD-856D6FEF4822}"), 2): "PKEY_DeviceInterface_FriendlyName",
    
    # APO (Audio Processing Objects) Effects
    (G("{E4870E26-3CC5-4CD2-BA46-CA0A9A70ED04}"), 0): "PKEY_AudioEndpoint_Effect_Clsid",
    (G("{E4870E26-3CC5-4CD2-BA46-CA0A9A70ED04}"), 1): "PKEY_AudioEndpoint_Effect_Capabilties",

    # Location
    (G("{540B947E-8B40-45BC-A8A2-6A0B894CBDA2}"), 9): "PKEY_Device_Location_Physical",
}



propsys = windll.propsys
ole32 = windll.ole32

propsys.PSGetNameFromPropertyKey.argtypes = [POINTER(PROPERTYKEY), POINTER(c_wchar_p)]
propsys.PSGetNameFromPropertyKey.restype = HRESULT

def get_property_key_name(prop_key: PROPERTYKEY) -> str:
    """
    Гибридное определение имени свойства:
    1. Windows Property System API
    2. Хардкодный словарь для аудио-специфичных ключей
    3. GUID + PID если ничего не нашли
    """
    # 1. Сначала ищем в нашем словаре (это быстрее и надежнее для аудио)
    # Ключ словаря: (строка GUID, int PID)
    lookup_key = (str(prop_key.fmtid), prop_key.pid)
    if lookup_key in KNOWN_PROPERTY_KEYS:
        return KNOWN_PROPERTY_KEYS[lookup_key]

    # 2. Если нет, спрашиваем систему
    ptr_name = c_wchar_p()
    try:
        res = propsys.PSGetNameFromPropertyKey(byref(prop_key), byref(ptr_name))
        if res == 0 and ptr_name.value:
            return ptr_name.value
    except Exception:
        pass # Игнорируем ошибки WinAPI здесь
    finally:
        if ptr_name:
            ole32.CoTaskMemFree(ptr_name)
    
    # 3. Если всё провалилось, возвращаем raw данные для дебага
    return f"UnknownKey: {prop_key.fmtid} / PID:{prop_key.pid}"


class DeviceVolumeNotificationCallback(PublicDeviceVolumeNotificationClient):
    def __init__(self, device_id):
        self.__device_id = device_id

    @property
    def device_id(self):
        return self.__device_id

    def on_notify(self, new_volume, new_mute, event_context, channels, channel_volumes):
        try:
            logger.info("---"*5)
            logger.info(f"Device ID: {self.device_id}")
            logger.info(f"New Volume: {new_volume}")
            logger.info(f"New Mute: {new_mute}")
            logger.info(f"Event: {event_context}")
            logger.info(f"Channels: {channels}")
            logger.info(f"Channel volumes: {channel_volumes}")
            logger.info("---"*5)
        except Exception:
            traceback.print_exc()


class AudioNotificationCallback(PublicAudioNotificationClient):
    PROPERTYKEYS = {
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 2): 'DEVPKEY_Device_DeviceDesc',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 3): 'DEVPKEY_Device_HardwareIds',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 4): 'DEVPKEY_Device_CompatibleIds',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 6): 'DEVPKEY_Device_Service',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 9): 'DEVPKEY_Device_Class',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 10): 'DEVPKEY_Device_ClassGuid',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 11): 'DEVPKEY_Device_Driver',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 12): 'DEVPKEY_Device_ConfigFlags',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 13): 'DEVPKEY_Device_Manufacturer',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 14): 'DEVPKEY_Device_FriendlyName',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 15): 'DEVPKEY_Device_LocationInfo',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 16): 'DEVPKEY_Device_PDOName',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 17): 'DEVPKEY_Device_Capabilities',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 18): 'DEVPKEY_Device_UINumber',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 19): 'DEVPKEY_Device_UpperFilters',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 20): 'DEVPKEY_Device_LowerFilters',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 21): 'DEVPKEY_Device_BusTypeGuid',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 22): 'DEVPKEY_Device_LegacyBusType',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 23): 'DEVPKEY_Device_BusNumber',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 24): 'DEVPKEY_Device_EnumeratorName',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 25): 'DEVPKEY_Device_Security',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 26): 'DEVPKEY_Device_SecuritySDS',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 27): 'DEVPKEY_Device_DevType',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 28): 'DEVPKEY_Device_Exclusive',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 29): 'DEVPKEY_Device_Characteristics',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 30): 'DEVPKEY_Device_Address',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 31): 'DEVPKEY_Device_UINumberDescFormat',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 32): 'DEVPKEY_Device_PowerData',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 33): 'DEVPKEY_Device_RemovalPolicy',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 34): 'DEVPKEY_Device_RemovalPolicyDefault',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 35): 'DEVPKEY_Device_RemovalPolicyOverride',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 36): 'DEVPKEY_Device_InstallState',
        ("{A45C254E-DF1C-4EFD-8020-67D146A850E0}", 37): 'DEVPKEY_Device_LocationPaths',
        ("{4340A6C5-93FA-4706-972C-7B648008A5A7}", 2): 'DEVPKEY_Device_DevNodeStatus',
        ("{4340A6C5-93FA-4706-972C-7B648008A5A7}", 3): 'DEVPKEY_Device_ProblemCode',
        ("{4340A6C5-93FA-4706-972C-7B648008A5A7}", 4): 'DEVPKEY_Device_EjectionRelations',
        ("{4340A6C5-93FA-4706-972C-7B648008A5A7}", 5): 'DEVPKEY_Device_RemovalRelations',
        ("{4340A6C5-93FA-4706-972C-7B648008A5A7}", 6): 'DEVPKEY_Device_PowerRelations',
        ("{4340A6C5-93FA-4706-972C-7B648008A5A7}", 7): 'DEVPKEY_Device_BusRelations',
        ("{4340A6C5-93FA-4706-972C-7B648008A5A7}", 8): 'DEVPKEY_Device_Parent',
        ("{4340A6C5-93FA-4706-972C-7B648008A5A7}", 9): 'DEVPKEY_Device_Children',
        ("{4340A6C5-93FA-4706-972C-7B648008A5A7}", 10): 'DEVPKEY_Device_Siblings',
        ("{80497100-8C73-48B9-AAD9-CE387E19C56E}", 2): 'DEVPKEY_Device_Reported',
        ("{80497100-8C73-48B9-AAD9-CE387E19C56E}", 3): 'DEVPKEY_Device_Legacy',
        ("{78C34FC8-104A-4ACA-9EA4-524D52996E57}", 256): 'DEVPKEY_Device_InstanceId',
        ("{540B947E-8B40-45BC-A8A2-6A0B894CBDA2}", 1): 'DEVPKEY_Numa_Proximity_Domain',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 2): 'DEVPKEY_Device_DriverDate',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 3): 'DEVPKEY_Device_DriverVersion',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 4): 'DEVPKEY_Device_DriverDesc',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 5): 'DEVPKEY_Device_DriverInfPath',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 6): 'DEVPKEY_Device_DriverInfSection',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 7): 'DEVPKEY_Device_DriverInfSectionExt',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 8): 'DEVPKEY_Device_MatchingDeviceId',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 9): 'DEVPKEY_Device_DriverProvider',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 10): 'DEVPKEY_Device_DriverPropPageProvider',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 11): 'DEVPKEY_Device_DriverCoInstallers',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 12): 'DEVPKEY_Device_ResourcePickerTags',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 13): 'DEVPKEY_Device_ResourcePickerExceptions',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 14): 'DEVPKEY_Device_DriverRank',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 15): 'DEVPKEY_Device_DriverLogoLevel',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 17): 'DEVPKEY_Device_NoConnectSound',
        ("{A8B865DD-2E3D-4094-AD97-E593A70C75D6}", 18): 'DEVPKEY_Device_GenericDriverInstalled',
        ("{CF73BB51-3ABF-44A2-85E0-9A3DC7A12132}", 2): 'DEVPKEY_DrvPkg_Model',
        ("{CF73BB51-3ABF-44A2-85E0-9A3DC7A12132}", 3): 'DEVPKEY_DrvPkg_VendorWebSite',
        ("{CF73BB51-3ABF-44A2-85E0-9A3DC7A12132}", 4): 'DEVPKEY_DrvPkg_DetailedDescription',
        ("{CF73BB51-3ABF-44A2-85E0-9A3DC7A12132}", 5): 'DEVPKEY_DrvPkg_DocumentationLink',
        ("{CF73BB51-3ABF-44A2-85E0-9A3DC7A12132}", 6): 'DEVPKEY_DrvPkg_Icon',
        ("{CF73BB51-3ABF-44A2-85E0-9A3DC7A12132}", 7): 'DEVPKEY_DrvPkg_BrandingIcon',
        ("{4321918B-F69E-470D-A5DE-4D88C75AD24B}", 19): 'DEVPKEY_DeviceClass_UpperFilters',
        ("{4321918B-F69E-470D-A5DE-4D88C75AD24B}", 20): 'DEVPKEY_DeviceClass_LowerFilters',
        ("{4321918B-F69E-470D-A5DE-4D88C75AD24B}", 25): 'DEVPKEY_DeviceClass_Security',
        ("{4321918B-F69E-470D-A5DE-4D88C75AD24B}", 26): 'DEVPKEY_DeviceClass_SecuritySDS',
        ("{4321918B-F69E-470D-A5DE-4D88C75AD24B}", 27): 'DEVPKEY_DeviceClass_DevType',
        ("{4321918B-F69E-470D-A5DE-4D88C75AD24B}", 28): 'DEVPKEY_DeviceClass_Exclusive',
        ("{4321918B-F69E-470D-A5DE-4D88C75AD24B}", 29): 'DEVPKEY_DeviceClass_Characteristics',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 2): 'DEVPKEY_DeviceClass_Name',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 3): 'DEVPKEY_DeviceClass_ClassName',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 4): 'DEVPKEY_DeviceClass_Icon',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 5): 'DEVPKEY_DeviceClass_ClassInstaller',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 6): 'DEVPKEY_DeviceClass_PropPageProvider',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 7): 'DEVPKEY_DeviceClass_NoInstallClass',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 8): 'DEVPKEY_DeviceClass_NoDisplayClass',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 9): 'DEVPKEY_DeviceClass_SilentInstall',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 10): 'DEVPKEY_DeviceClass_NoUseClass',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 11): 'DEVPKEY_DeviceClass_DefaultService',
        ("{259ABFFC-50A7-47CE-AF08-68C9A7D73366}", 12): 'DEVPKEY_DeviceClass_IconPath',
        ("{713D1703-A2E2-49F5-9214-56472EF3DA5C}", 2): 'DEVPKEY_DeviceClass_ClassCoInstallers',
        ("{026E516E-B814-414B-83CD-856D6FEF4822}", 2): 'DEVPKEY_DeviceInterface_FriendlyName',
        ("{026E516E-B814-414B-83CD-856D6FEF4822}", 3): 'DEVPKEY_DeviceInterface_Enabled',
        ("{026E516E-B814-414B-83CD-856D6FEF4822}", 4): 'DEVPKEY_DeviceInterface_ClassGuid',
        ("{14C83A99-0B3F-44B7-BE4C-A178D3990564}", 2): 'DEVPKEY_DeviceInterfaceClass_DefaultInterface',
    }

    def __init__(self, coreaudio):
        self.coreaudio = coreaudio.get_instance()

    def explain_propertykey(self, fmtid: str, pid: int) -> str:
        return self.PROPERTYKEYS.get((str(fmtid), pid), f"Unknown PROPERTYKEY ({fmtid}#{pid})")

    def on_default_device_changed(
            self, flow_id: int, role_id: int, default_device_id: str
        ):
        try:
            device_name = self.coreaudio.get_device_friendly_name(default_device_id)
            flow = EDataFlow(flow_id).name
            role = ERole(role_id).name
            logger.info(f"on_default_device_changed: device_name - {device_name}  flow - {flow}  role - {role}")
        except Exception:
            traceback.print_exc()
        
        return 0

    def on_device_added(self, added_device_id_str: str):
        try:
            device_name = self.coreaudio.get_device_friendly_name(added_device_id_str)
            logger.info(f"on_device_added: {device_name}")
        except Exception:
            traceback.print_exc()

        return 0

    def on_device_removed(self, removed_device_id_str: str):
        try:
            device_name = self.coreaudio.get_device_friendly_name(removed_device_id_str)
            logger.info(f"on_device_state_removed: {device_name}")
        except Exception:
            traceback.print_exc()

        return 0

    def on_device_state_changed(self, device_id, new_state_id):
        try:
            device_name = self.coreaudio.get_device_friendly_name(device_id)
            # old_device_state = self.coreaudio.get_device_state(device_id)
            new_device_state = new_state_id
            # logger.info(f"on_device_state_changed: {device_name} {old_device_state} {new_device_state}")
            logger.info(f"on_device_state_changed: {device_name}. State: {EAudioDeviceState(new_device_state)}")
        except Exception:
            traceback.print_exc()

        return 0

    def on_property_value_changed(self, device_id, property_struct):
        try:
        # 1. Проверяем, живо ли устройство (чтобы не ловить ошибки чтения)
            state = self.coreaudio.get_device_state(device_id)
            if state in ["NotPresent", "Unplugged"]:
                # Можно логировать, но читать свойства нельзя
                # logger.debug(f"Device {device_id} is gone, skipping property read.")
                return 0

            # 2. Получаем имя ключа (наш "умный" метод из прошлого ответа)
            key_struct = property_struct
            key_name = get_property_key_name(key_struct) # Предположим, ты добавил это в API

            # 3. Читаем сырое значение (PROPVARIANT)
            # ВАЖНО: Нам нужен сам объект PROPVARIANT, а не обработанный GetValue(),
            # чтобы передать его в парсер (или можно переделать парсер, чтобы он принимал bytes)
            # Но давай используем твой метод _get_device_property, который возвращает результат GetValue()
            
            # Внимание: твой метод _get_device_property сразу делает .GetValue().
            # Если GetValue возвращает bytes (для BLOB), то всё ок.
            
            raw_value = self.coreaudio._get_device_property(
                device_id, key_struct.fmtid, key_struct.pid
            )

            # 4. Парсим значение красиво
            # Нам нужно передать raw_value. Если raw_value это bytes, парсер попытается сделать структуру.
            # Если raw_value это уже int/str - парсер вернет как есть.
            
            # !!! Небольшой хак: мой парсер выше ожидал PROPVARIANT, но давай адаптируем его под raw_value
            # (код парсера выше я написал с учетом .GetValue(), так что можно передавать raw_value,
            # но нужно чуть подправить сигнатуру функции parse_complex_property(key_name, val))
            
            formatted_value = parse_complex_property(key_name, raw_value)

            logger.info(f"PROP: {key_name} -> {formatted_value}")

        except Exception:
            traceback.print_exc()
            # logger.error(f"Error reading property: {e}")
            # pass # Игнорируем спам ошибок при отключении
        
        return 0

        # state = self.coreaudio.get_device_state(device_id)
        # if state == "NotPresent":
        #     return 0 # Устройство удалено, свойства недоступны
        # if device_id == "{0.0.1.00000000}.{5c63ab0b-5af7-4759-a791-fd8451ca018c}":
        #     dev_name = self.coreaudio.get_device_friendly_name(device_id)
            
        #     print()
        #     logger.info(f"Changed device '{dev_name}' property {property_struct.fmtid}/{property_struct.pid}")
        #     print(f"{get_property_key_name(property_struct)}")
        #     print()


            # try:
            #     fmtid = property_struct.fmtid
            #     pid = property_struct.pid

            #     dev_name = self.coreaudio.get_device_friendly_name(device_id)

            #     print()
            #     logger.info(f"Changed device '{dev_name}' property {fmtid},{pid}")
            #     prop = self.coreaudio._get_device_property(device_id, fmtid, pid)
            #     logger.info(f"Property: {prop} :: {self.explain_propertykey(fmtid, pid)}")
            #     print()

            #     # if (fmtid,pid) == (GUID("{A45C254E-DF1C-4EFD-8020-67D146A850E0}"),2):
            #     #     print(1)
            #     #     self.coreaudio._set_device_property(device_id, property_struct, propvar, "ty()")
            #         # print(2)
            # except Exception as e:
            #     traceback.print_exc()
            #     print(f"Exception!: {e}")
        
        # return 0