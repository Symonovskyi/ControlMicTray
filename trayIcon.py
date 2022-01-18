# Built-in modules.
from sys import argv, exit
from ctypes import POINTER, cast

# "pip install" modules.
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from comtypes import CLSCTX_ALL, COMObject
from pycaw.pycaw import AudioUtilities as aUtils
from pycaw.pycaw import IAudioEndpointVolume, IAudioEndpointVolumeCallback
# from pynput import keyboard
from keyboard import add_hotkey


class MicrophoneController():
    '''
    Class that uses "pycaw" module to operate with microphone.

    Methods:
    \nMuteMic() - mutes the mic.
    \nUnMuteMic() - unmutes the mic.

    Properties:
    \nGetDevicesCount - returns microphones count that are active in system.
    \nGetMicMuteState - returns the actual state of mic: muted or not.
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
    \nCheckIfMuted() - checks the actual state of mic, and mutes/unmutes it 
    according to its status. Also, changes the tray icon and check mark on 
    the first element menu.
    \nMicrophoneControl() - mutes or unmutes mic. The first menu item signal is 
    connected to this slot (func).
    \nHotkeyControl() - does the same as MicrophoneControl(), but when pressing
    preset keyboard shortcut.
    '''
    def __init__(self):
        super().__init__()
        self.mic = MicrophoneController()

        # Creating menu of tray.
        self.menu = QtWidgets.QMenu()

        # Calling the initialization func.
        self.TrayInit()

        # Adding hotkey for controling mic.
        add_hotkey('ctrl + shift + z', self.HotkeyControl)

    def TrayInit(self):
        # Adding and configuring "On\Off Microphone" menu element.
        self.turnMicro = self.menu.addAction("Вкл\выкл. микрофон")
        self.turnMicro.triggered.connect(self.MicrophoneControl)

        self.menu.addSeparator()

        # Adding and configuring "Mics quantity: {quantity}" menu element.
        quantityOfActiveMics = self.menu.addAction(
            f"Кол-ство микрофонов: {self.mic.GetDevicesCount}")
        quantityOfActiveMics.setEnabled(False)

        # Adding and configuring "Settings" menu element.
        settingsAction = self.menu.addAction("Настройки")
        settingsAction.setIcon(QIcon("images\\settings.png"))
        settingsAction.setEnabled(False)

        self.menu.addSeparator()

        # Adding and configuring "About..." menu element.
        aboutAction = self.menu.addAction("О программе...")
        aboutAction.setIcon(QIcon("images\\about.png"))
        aboutAction.setEnabled(False)

        # Adding and configuring "Exit" menu element.
        exitAction = self.menu.addAction("Выход")
        exitAction.setIcon(QIcon("images\\exit.png"))
        exitAction.triggered.connect(exit)

        # Connecting menu with tray.
        self.setContextMenu(self.menu)
        self.setToolTip("ControlMicTray")

        # Cheking mic status on startup.
        self.CheckIfMuted()

        self.show()

    def CheckIfMuted(self):
        ''' According to mic status, these changes are applied:
        - Tray Icon;
        - Mute/Unmute microphone;
        - Change text of the first menu element.
        '''
        if self.mic.GetMicMuteState == 0:
            self.setIcon(QIcon("images\\Microphone_dark_ON.svg"))
            self.mic.MuteMic()
            self.turnMicro.setText("Выключить микрофон")
        elif self.mic.GetMicMuteState == 1:
            self.setIcon(QIcon("images\\Microphone_dark_OFF.svg"))
            self.mic.UnMuteMic()
            self.turnMicro.setText("Включить микрофон")

    def MicrophoneControl(self):
        if self.turnMicro.isChecked():
            self.CheckIfMuted()
        else:
            self.CheckIfMuted()

    def HotkeyControl(self):
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

    app = QtWidgets.QApplication(argv)
    win = TrayApp()
    exit(app.exec())
