from comtypes import CLSCTX_ALL, COMObject, POINTER
from comtypes.client import CreateObject
from ctypes import cast
from comtypes import COMError

from src.managers.winos.api.interfaces import (
    IAudioEndpointVolume, IMMDeviceEnumerator, IPolicyConfig, IMMNotificationClient, GUID
)
from src.managers.winos.api.constants import EDataFlow, DEVICE_STATE, ERole, STGM
from src.managers.winos.api.structures import PROPERTYKEY


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
        if self._get_state() == 1:
            iid = IAudioEndpointVolume._iid_
            endpoint_volume_ptr = self._imm_device.Activate(iid, CLSCTX_ALL, None)
            endpoint_volume = cast(endpoint_volume_ptr, POINTER(IAudioEndpointVolume))
            return endpoint_volume
        else:
            return None

    def get_id(self):
        return self._id

    def get_state(self):
        return self._state
    
    def get_mic_name(self):
        """
        Retrieves the friendly name of the microphone device.

        Returns:
            str: The friendly name (e.g., "Microphone (Default Device)").
        """
        # Open the property store in read mode (STGM_READ = 0)
        store = self._imm_device.OpenPropertyStore(STGM.STGM_READ.value.real)
        properties = {}

        if store is not None:
            propCount = store.GetCount()
            for j in range(propCount):
                try:
                    pk = store.GetAt(j)
                    value = store.GetValue(pk)
                    v = value.GetValue()
                except COMError:
                    continue
                value.clear()
                name = str(pk)
                properties[name] = v

        DEVPKEY_Device_FriendlyName = (
            "{a45c254e-df1c-4efd-8020-67d146a850e0} 14".upper()
        )
        value = properties.get(DEVPKEY_Device_FriendlyName)
        # Change all this logic using "if value is devpkey, then write it to the variable value"
        print('\n')
        print(f"Properties: {properties}")
        print('\n')
        return value


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
    def __init__(self):
        self._device_enumerator = CreateObject(IMMDeviceEnumerator.clsid, interface=IMMDeviceEnumerator, clsctx=CLSCTX_ALL) # ?Convert to context manager with Releasing!
        self._microphones = self._get_microphones()
        self._callbacks = []

    def _get_microphones(self):
        # Enumerate capture (microphone) devices
        all_devices_collection = self._device_enumerator.EnumAudioEndpoints(
            EDataFlow.eCapture.value,
            DEVICE_STATE.ACTIVE.value | DEVICE_STATE.DISABLED.value
        )
        count = all_devices_collection.GetCount()
        microphones = []
        for i in range(count):
            device = all_devices_collection.Item(i)
            microphones.append(Microphone(device))

        return microphones

    def get_all_microphones(self):
        return self._microphones

    def get_default_microphone(self):
        device_ptr = self._device_enumerator.GetDefaultAudioEndpoint(
            EDataFlow.eCapture.value,
            ERole.eMultimedia.value
        )
        device = device_ptr
        return Microphone(device)

    # ?Move to the actual microphone object!
    def set_default_microphone(self, microphone):
        policy_config = CreateObject(IPolicyConfig.clsid, interface=IPolicyConfig, clsctx=CLSCTX_ALL)
        policy_config.SetDefaultEndpoint(microphone.get_id(), 1)  # eMultimedia
        policy_config.Release()

    def register_callback(self, callback):
        self._device_enumerator.RegisterEndpointNotificationCallback(callback)
        self._callbacks.append(callback)

    def unregister_callback(self, callback):
        self._device_enumerator.UnregisterEndpointNotificationCallback(callback)
        self._callbacks.remove(callback)

# Example usage
if __name__ == "__main__":
    controller = MicrophonesController()
    
    # Get all microphones
    microphones: list[Microphone] = controller.get_all_microphones()
    for mic in microphones:
        print(f"Microphone ID: {mic.get_id()}, State: {mic.get_state()}, Name: {mic.get_mic_name()}")

    # Get default microphone
    default_mic = controller.get_default_microphone()
    print(f"Default Microphone ID: {default_mic.get_id()}, State: {default_mic.get_state()}, Name: {default_mic.get_mic_name()}")
    
    # # Set a microphone as default
    # if len(microphones) > 1:
    #     controller.set_default_microphone(microphones[0])



    # # Register a callback
    # class MyNotificationClient(COMObject):
    #     _com_interfaces_ = (IMMNotificationClient,)

    #     DeviceStates = {1: "Active", 2: "Disabled", 4: "NotPresent", 8: "Unplugged"}
    #     Roles = ["eConsole", "eMultimedia", "eCommunications", "ERole_enum_count"]
    #     DataFlow = ["eRender", "eCapture", "eAll", "EDataFlow_enum_count"]

    #     def OnDefaultDeviceChanged(self, flow_id, role_id, default_device_id):
    #         flow = self.DataFlow[flow_id]
    #         role = self.Roles[role_id]
    #         self.on_default_device_changed(flow, flow_id, role, role_id, default_device_id)

    #     def OnDeviceAdded(self, added_device_id):
    #         self.on_device_added(added_device_id)

    #     def OnDeviceRemoved(self, removed_device_id):
    #         self.on_device_removed(removed_device_id)

    #     def OnDeviceStateChanged(self, device_id, new_state_id):
    #         new_state = self.DeviceStates[new_state_id]
    #         self.on_device_state_changed(device_id, new_state, new_state_id)

    #     def OnPropertyValueChanged(self, device_id, property_struct):
    #         fmtid = property_struct.fmtid
    #         pid = property_struct.pid
    #         self.on_property_value_changed(device_id, property_struct, fmtid, pid)

    #     def on_default_device_changed(
    #         self, flow, flow_id, role, role_id, default_device_id
    #     ):
    #         print(f"Default device changed to {default_device_id} for flow {flow} and role {role}")
    #         return 0

    #     def on_device_added(self, added_device_id):
    #         print(f"Device {added_device_id} added")
    #         return 0

    #     def on_device_removed(self, removed_device_id):
    #         print(f"Device {removed_device_id} removed")
    #         return 0

    #     def on_device_state_changed(self, device_id, new_state, new_state_id):
    #         print(f"Device {device_id} state changed to {new_state}")
    #         return 0

    #     def on_property_value_changed(self, device_id, property_struct, fmtid, pid):
    #         print(f"Property value changed for device {device_id}: fmtid={fmtid}, pid={pid}, value={property_struct.union}")
    #         return 0


    # callback = MyNotificationClient()
    # controller.register_callback(callback)

    # while True:
    #     if input("Press 'q' to quit: ") == "q":
    #         # Unregister the callback
    #         controller.unregister_callback(callback)
    #         break
    #     else:
    #         continue
