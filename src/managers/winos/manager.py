from comtypes import CLSCTX_ALL, COMObject, POINTER, CoCreateInstance, CoInitialize
from ctypes import cast
from comtypes import COMError
from traceback import print_exc

from src.managers.winos.api.interfaces import (
    IAudioEndpointVolume, IMMDeviceEnumerator, IPolicyConfig,
    IMMNotificationClient
)
from src.managers.winos.api.constants import (
    EDataFlow, AudioDeviceState, ERole, STGM, DEVPKEY_Device_FriendlyName
)

class MyNotificationClient(COMObject):
    _com_interfaces_ = (IMMNotificationClient,)

    def OnDefaultDeviceChanged(self, flow_id, role_id, default_device_id):
        flow = [flow.name for flow in EDataFlow if flow.value == flow_id][0]
        role = [role.name for role in ERole if role.value == role_id][0]
        self.on_default_device_changed(flow, flow_id, role, role_id, default_device_id)

    def OnDeviceAdded(self, added_device_id):
        self.on_device_added(added_device_id)

    def OnDeviceRemoved(self, removed_device_id):
        self.on_device_removed(removed_device_id)

    def OnDeviceStateChanged(self, device_id, new_state_id):
        new_state = [new_state.name for new_state in AudioDeviceState if new_state.value.real == new_state_id][0]
        self.on_device_state_changed(device_id, new_state, new_state_id)

    def OnPropertyValueChanged(self, device_id, property_struct):
        fmtid = property_struct.fmtid
        pid = property_struct.pid
        self.on_property_value_changed(device_id, property_struct, fmtid, pid)



    def on_default_device_changed(
        self, flow, flow_id, role, role_id, default_device_id
    ):
        try:
            enumerator = MicrophonesController.enumerator()
            device_ptr = enumerator.GetDevice(default_device_id)
            device = Microphone(device_ptr)
            print(f"Default device changed: {device.friendly_name} - {device.state_str} - {role} - {flow}")
            return 0
        except Exception:
            print_exc()

    def on_device_added(self, added_device_id):
        enumerator = MicrophonesController.enumerator()
        device_ptr = enumerator.GetDevice(added_device_id)
        device = Microphone(device_ptr)
        print(f"Default device added: {device.friendly_name} - {device.state_str}")
        return 0

    def on_device_removed(self, removed_device_id):
        enumerator = MicrophonesController.enumerator()
        device_ptr = enumerator.GetDevice(removed_device_id)
        device = Microphone(device_ptr)
        print(f"Device removed: {device.friendly_name} - {device.state_str}")
        return 0

    def on_device_state_changed(self, device_id, new_state, new_state_id):
        enumerator = MicrophonesController.enumerator()
        device_ptr = enumerator.GetDevice(device_id)
        device = Microphone(device_ptr)
        print(f"Device {device.friendly_name} state changed to {new_state}")
        return 0

    def on_property_value_changed(self, device_id, property_struct, fmtid, pid):
        print(f"Property value changed for device {device_id}: fmtid={fmtid}, pid={pid}, value={property_struct}")
        return 0




class Microphone:
    def __init__(self, imm_device):
        self._imm_device = imm_device
        self._id = self._get_id()
        self._state = self._get_state()
        self._dev_endpoint_volume = self._activate_audio_endpoint_volume()

    def _get_id(self):
        id_ptr = self._imm_device.GetId()
        return id_ptr

    def _get_state(self):
        state_ptr = self._imm_device.GetState()
        return state_ptr

    def _activate_audio_endpoint_volume(self):
        if self._get_state() == AudioDeviceState.Active.value.real:
            iid = IAudioEndpointVolume._iid_
            endpoint_volume_ptr = self._imm_device.Activate(iid, CLSCTX_ALL, None)
            endpoint_volume = cast(endpoint_volume_ptr, POINTER(IAudioEndpointVolume))
            return endpoint_volume
        else:
            return None

    @property
    def id(self):
        return self._id

    @property
    def state_int(self) -> int:
        return self._state
    
    @property
    def state_str(self) -> str:
        """
        Returns the state of the microphone as an AudioDeviceState enum.
        """
        return AudioDeviceState(self._state).name
    
    @property
    def friendly_name(self):
        """
        Retrieves the friendly name of the microphone device.

        Returns:
            str: The friendly name (e.g., "Microphone (Default Device)").
        """
        # Open the property store in read mode (STGM_READ = 0)
        store = self._imm_device.OpenPropertyStore(STGM.STGM_READ.value.real)

        if store is not None:
            propCount = store.GetCount()
            for prop in range(propCount):
                try:
                    pk = store.GetAt(prop)
                    value = store.GetValue(pk)
                    v = value.GetValue()
                    if str(pk) == DEVPKEY_Device_FriendlyName:
                        device_name = v
                except COMError:
                    continue
                value.clear()

        return device_name

    def set_master_volume_level(self, level, event_context=None):
        if self._dev_endpoint_volume is not None:
            self._dev_endpoint_volume.SetMasterVolumeLevelScalar(level, event_context)

    def get_master_volume_level(self):
        if self._dev_endpoint_volume is not None:
            return self._dev_endpoint_volume.GetMasterVolumeLevelScalar()

    def set_mute(self, mute, event_context=None):
        if self._dev_endpoint_volume is not None:
            self._dev_endpoint_volume.SetMute(mute, event_context)

    def get_mute(self):
        if self._dev_endpoint_volume is not None:
            return self._dev_endpoint_volume.GetMute()



class MicrophonesController:

    @classmethod
    def enumerator(cls) -> IMMDeviceEnumerator:
        try:
            device_enumerator: IMMDeviceEnumerator = CoCreateInstance(
                IMMDeviceEnumerator.clsid, interface=IMMDeviceEnumerator, clsctx=CLSCTX_ALL
            )
        except OSError:
            CoInitialize()
            device_enumerator: IMMDeviceEnumerator = CoCreateInstance(
                IMMDeviceEnumerator.clsid, interface=IMMDeviceEnumerator, clsctx=CLSCTX_ALL
            )
        finally:
            return device_enumerator

    @classmethod
    def get_all_microphones(cls) -> tuple[Microphone]:
        microphones = ()

        all_devices_collection = cls.enumerator().EnumAudioEndpoints(
            EDataFlow.eCapture.value,
            AudioDeviceState.Active.value | AudioDeviceState.Disabled.value | AudioDeviceState.Unplugged.value
        )
        count = all_devices_collection.GetCount()
        for i in range(count):
            device = all_devices_collection.Item(i)
            microphones += (Microphone(device),)

        return microphones

    @classmethod
    def get_default_microphone(cls) -> Microphone:
        device_ptr = cls.enumerator().GetDefaultAudioEndpoint(
            EDataFlow.eCapture.value,
            ERole.eMultimedia.value
        )
        return Microphone(device_ptr)

    @classmethod
    def is_mic_default(cls, mic: Microphone) -> tuple[bool, bool]:
        mul_device_ptr = cls.enumerator().GetDefaultAudioEndpoint(
            EDataFlow.eCapture.value,
            ERole.eMultimedia.value
        )

        com_device_ptr = cls.enumerator().GetDefaultAudioEndpoint(
            EDataFlow.eCapture.value,
            ERole.eCommunications.value
        )
        if mic.state_int != AudioDeviceState.Active.value.real:
            return False, False
        if mic.id == mul_device_ptr.GetId():
            return True, False
        if mic.id == com_device_ptr.GetId():
            return False, True

    @classmethod
    def set_by_default(cls, mic: Microphone):
        if mic.state_int == AudioDeviceState.Active.value.real:
            policy_config = CoCreateInstance(IPolicyConfig.clsid, interface=IPolicyConfig, clsctx=CLSCTX_ALL)
            policy_config.SetDefaultEndpoint(mic.id, ERole.eCommunications.value)
            policy_config.SetDefaultEndpoint(mic.id, ERole.eMultimedia.value)
            policy_config.Release()

    @classmethod
    def register_callback(cls):
        cls.callback = MyNotificationClient()
        cls.enumerator().RegisterEndpointNotificationCallback(cls.callback)

    @classmethod
    def unregister_callback(cls):
        if cls.callback is not None:
            cls.enumerator().UnregisterEndpointNotificationCallback(cls.callback)



# Example usage
if __name__ == "__main__":
    controller = MicrophonesController
    
    # Get all microphones
    microphones = controller.get_all_microphones()
    for mic in microphones:
        print(f"Microphone Name: {mic.friendly_name}. State: {mic.state_str}. Is Default: {controller.is_mic_default(mic)}")

    # Set a microphone as default
    if len(microphones) > 1:
        controller.set_by_default(microphones[1])
        print(controller.is_mic_default(microphones[0]))

    controller.register_callback()

    while True:
        try:
            if input("Press 'q' to quit: ") == "q":
                # Unregister the callback
                controller.unregister_callback()
                break
            else:
                continue
        except OSError as e:
            print(f"Error: {e}")
            controller.enumerator().Release()
            controller.unregister_callback()
            break
