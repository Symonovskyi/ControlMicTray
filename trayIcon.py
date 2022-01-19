# Built-in modules.
from sys import argv, exit
from ctypes import POINTER, cast

# "pip install" modules.
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from comtypes import CLSCTX_ALL, COMObject
from pycaw.pycaw import AudioUtilities as aUtils
from pycaw.pycaw import IAudioEndpointVolume, IAudioEndpointVolumeCallback
from keyboard import add_hotkey


class MicrophoneController():
    '''
    Class that uses "pycaw" module to operate with microphone.

    Methods:
    - MuteMic() - mutes the mic.
    - UnMuteMic() - unmutes the mic.

    Properties:
    - GetDevicesCount - holds microphones count that are active in system.
    - GetMicMuteState - holds the actual state of mic: muted or not.
    - GetMic - holds the actual microphone instance.
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

    @property
    def GetMic(self):
        return self.mic

    def MuteMic(self):
        self.mic.SetMute(True, None)

    def UnMuteMic(self):
        self.mic.SetMute(False, None)


class TrayApp(QtWidgets.QSystemTrayIcon):
    '''
    Class that actually creates the tray icon and it's menu elements.
    Also, this class configures the behaviour of menu items.

    Methods:
    - TrayInit() - initializates all tray menu elements and configuring them.
    - CheckIfMuted() - checks the actual state of mic, and mutes/unmutes it 
    according to its status. Also, changes the tray icon and check mark on 
    the first element menu.
    '''
    def __init__(self):
        super().__init__()
        self.mic = MicrophoneController()

        # Creating menu of tray.
        self.menu = QtWidgets.QMenu()

        # Calling the initialization func.
        self.TrayInit()

        # Adding hotkey for controling mic.
        add_hotkey('CTRL + SHIFT + Z', self.CheckIfMuted)

    def TrayInit(self):
        # Adding and configuring "On\Off Microphone" menu element.
        self.turnMicro = self.menu.addAction("Вкл\выкл. микрофон")
        # Connecting menu element to appropriate method.
        self.turnMicro.triggered.connect(self.CheckIfMuted)

        self.menu.addSeparator()

        # Adding and configuring "Mics quantity: {quantity}" menu element.
        quantityOfActiveMics = self.menu.addAction(
            f"Кол-ство микрофонов: {self.mic.GetDevicesCount}")
        quantityOfActiveMics.setIcon(QIcon("images\\Microphone_light.svg"))
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
        self.CheckIfMuted(mode="InterfaceOnly")

        self.mic.GetMic.RegisterControlChangeNotify(
            AudioEndpointVolumeCallback())

        self.show()

    def CheckIfMuted(self, mode=None):
        ''' According to mic status, these changes are applied:
        - Tray Icon;
        - First menu element icon;
        - Change text of the first menu element;
        - Mute/Unmute microphone if mode =! "InterfaceOnly".
        '''
        if mode == "InterfaceOnly":
            if self.mic.GetMicMuteState == 0:
                self.setIcon(QIcon("images\\Microphone_dark_ON.svg"))
                self.turnMicro.setIcon(QIcon("images\\on.png"))
                self.turnMicro.setText("Выключить микрофон")
            elif self.mic.GetMicMuteState == 1:
                self.setIcon(QIcon("images\\Microphone_dark_OFF.svg"))
                self.turnMicro.setIcon(QIcon("images\\off.png"))
                self.turnMicro.setText("Включить микрофон")
        else:
            if self.mic.GetMicMuteState == 0:
                self.mic.MuteMic()
                self.CheckIfMuted(mode="InterfaceOnly")
            elif self.mic.GetMicMuteState == 1:
                self.mic.UnMuteMic()
                self.CheckIfMuted(mode="InterfaceOnly")

    # @classmethod
    # def UpdateInterface(cls):
    #     # cls.CheckIfMuted(cls, mode='InterfaceOnly')
    #     mic = MicrophoneController()
    #     if mic.GetMicMuteState == 0:
    #         print(1)
    #         cls.setIcon(QIcon("images\\Microphone_dark_ON.svg"))
    #     elif mic.GetMicMuteState == 1:
    #         cls.setIcon(QIcon("images\\Microphone_dark_OFF.svg"))


class AudioEndpointVolumeCallback(COMObject):
    _com_interfaces_ = [IAudioEndpointVolumeCallback]

    def OnNotify(self, pNotify):
        TrayApp.CheckIfMuted(mode="InterfaceOnly")


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)
    win = TrayApp()
    exit(app.exec())
