# Built-in modules.
import sys
from ctypes import POINTER, cast

# "pip install" modules.
from PyQt5 import QtGui, QtWidgets
from comtypes import CLSCTX_ALL, COMObject
from pycaw.pycaw import AudioUtilities as aUtils
from pycaw.pycaw import IAudioEndpointVolume, IAudioEndpointVolumeCallback


class MicrophoneController():
    '''
    Class that uses "pycaw" module to operate with microphone.

    Methods:
    MuteMic() - mutes the mic.
    UnMuteMic() - unmutes the mic.

    Properties:
    GetDevicesCount - returns microphones count that are active in system.
    GetMicMuteState - returns the actual state of mic: muted or not.
    '''
    def __init__(self):
        mic_device = aUtils.GetMicrophone()
        interface = mic_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,\
            None)
        self.mic = cast(interface, POINTER(IAudioEndpointVolume))

    #TODO: get the real count of microphones only.
    @property
    def GetDevicesCount(self):
        return len(aUtils.GetAllDevices())

    @property
    def GetMicMuteState(self):
        return self.mic.GetMute()

    def MuteMic(self):
        self.mic.SetMute(True, None)

    def UnMuteMic(self):
        self.mic.SetMute(False, None)


class TrayApp(QtWidgets.QSystemTrayIcon):
    '''
    Class that actually creates the tray icon and it's menu elements.
    Also, this class configures the behaviour of menu items.

    Methods:
    TrayInit() - initializates all tray menu elements and configuring them.
    CheckIfMuted() - checks the actual state of mic, changes the 
    tray icon and check mark on the first element menu.
    MicrophoneControl() - mutes or unmutes mic. The first menu item signal is 
    connected to this slot (func).
    '''
    def __init__(self):
        super().__init__()
        self.mic = MicrophoneController()

        # Creating menu of tray.
        self.menu = QtWidgets.QMenu()

        self.TrayInit()

    def TrayInit(self):
        self.turnMicro = self.menu.addAction("Вкл\выкл. микрофон")
        self.turnMicro.triggered.connect(self.MicrophoneControl)
        self.turnMicro.setCheckable(True)

        self.menu.addSeparator()

        quantityOfActiveMics = self.menu.addAction(
            f"Кол-ство микрофонов: {self.mic.GetDevicesCount}")
        quantityOfActiveMics.setEnabled(False)

        settingsAction = self.menu.addAction("Настройки")
        settingsAction.setEnabled(False)

        self.menu.addSeparator()

        aboutAction = self.menu.addAction("О программе...")
        aboutAction.setEnabled(False)

        exitAction = self.menu.addAction("Выход")
        exitAction.triggered.connect(sys.exit)

        self.setContextMenu(self.menu)
        self.setToolTip("Статус микрофона")

        self.CheckIfMuted()

        self.show()

    def CheckIfMuted(self):
        if self.mic.GetMicMuteState == 0:
            self.setIcon(QtGui.QIcon("images\\Microphone_dark_ON.svg"))
            self.turnMicro.setChecked(True)
        elif self.mic.GetMicMuteState == 1:
            self.setIcon(QtGui.QIcon("images\\Microphone_dark_OFF.svg"))
            self.turnMicro.setChecked(False)

    def MicrophoneControl(self):
        if self.turnMicro.isChecked():
            self.mic.UnMuteMic()
            self.CheckIfMuted()
        else:
            self.mic.MuteMic()
            self.CheckIfMuted()


# class AudioEndpointVolumeCallback(COMObject):
#     _com_interfaces_ = [IAudioEndpointVolumeCallback]
#     t = TrayApp

#     def OnNotify(self, pNotify):
#         # self.t().CheckIfMuted()
#         print(1)


if __name__ == '__main__':
    #TODO: When the actual status of mic changes, call CheckIfMuted() method.
    # The whole stuff below is for to do above stuff.

    # devices = aUtils.GetMicrophone()
    # interface = devices.Activate(
    #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    # volume = cast(interface, POINTER(IAudioEndpointVolume))
    # callback = AudioEndpointVolumeCallback()
    # volume.RegisterControlChangeNotify(callback)

    app = QtWidgets.QApplication(sys.argv)
    win = TrayApp()
    sys.exit(app.exec())
