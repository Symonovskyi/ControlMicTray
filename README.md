# ControlMicTray

### Video Demo: [Video at Loom](https://www.loom.com/share/e9984bf32efb461ebff44223645f18ac)
### Developed with :yellow_heart: :blue_heart:, Python and PyQt6!

>## *This project are made by two **Ukrainian** developers*:
>- [timo364](https://github.com/timo364) (Me, as coder);
>- [Sif-on](https://github.com/Sif-on) (My mate, as Project Manager and Designer).

## Warning! This app uses external library, cloned from GitHub: [Python Core Audio Windows Library](https://github.com/AndreMiras/pycaw)
## This is just a reference on an external source code.


# The project aim
This app will allow you to _control_ your microphone mute state, using two methods:
- By tray menu entries;
- By keyboard hotkeys, that can set by yourself.

# Realized stuff as of 09.08.2022:
- [x] Muting and unmuting microphone by hotkey, manually set in the setiings of app;
- [x] Muting and unmuting microphone in the tray menu;
- [x] A bit buggy dark and light themes;
- [x] Turning off mic at the app startup;
- [x] Very laggy, but free to use "Walkie-Talkie" mode;
- [ ] Multi-language support;
- [ ] Auto app startup (chekbox in settings);
- [ ] App notifications;
- [ ] Auto updates support.

# Project structure
```
📦project
 ┣ 📂EXE
 ┃ ┣ 📜ControlMicTray_Setup.zip
 ┃ ┗ 📜Автозагрузка.lnk
 ┣ 📂database
 ┃ ┣ 📂SQL
 ┃ ┃ ┣ 📜CREATE_DATA.sql
 ┃ ┃ ┣ 📜CREATE_TABLES.sql
 ┃ ┃ ┣ 📜DROP_TABLE.sql
 ┃ ┃ ┗ 📜UPDATE_ABOUT_DATA.sql
 ┃ ┣ 📜__init__.py
 ┃ ┗ 📜databaseController.py
 ┣ 📂logic
 ┃ ┣ 📜absolutePath.py
 ┃ ┣ 📜microphoneController.py
 ┣ 📂ui
 ┃ ┣ 📂resources
 ┃ ┃ ┣ 📜About.svg
 ┃ ┃ ┣ 📜ControlMicTray.ico
 ┃ ┃ ┣ 📜Exit.svg
 ┃ ┃ ┣ 📜Frame.svg
 ┃ ┃ ┣ 📜Microphone.svg
 ┃ ┃ ┣ 📜Microphone_dark.svg
 ┃ ┃ ┣ 📜Microphone_dark_OFF.svg
 ┃ ┃ ┣ 📜Microphone_dark_ON.svg
 ┃ ┃ ┣ 📜Microphone_light.svg
 ┃ ┃ ┣ 📜Microphone_light_OFF.svg
 ┃ ┃ ┣ 📜Microphone_light_ON.svg
 ┃ ┃ ┣ 📜Off.svg
 ┃ ┃ ┣ 📜On.svg
 ┃ ┃ ┣ 📜Settings.svg
 ┃ ┣ 📂styles
 ┃ ┃ ┗ 📜styles.py
 ┃ ┣ 📂ui_py
 ┃ ┃ ┣ 📜AboutWindow.ui
 ┃ ┃ ┣ 📜AboutWindowUI.py
 ┃ ┃ ┣ 📜SettingsWindow.ui
 ┃ ┃ ┣ 📜SettingsWindowUI.py
 ┃ ┃ ┣ 📜old_AboutWindow.ui
 ┃ ┃ ┗ 📜old_SettingsWindow.ui
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜aboutWindow.py
 ┃ ┣ 📜settingsWindow.py
 ┃ ┣ 📜test.py
 ┃ ┗ 📜trayIcon.py
 ┣ 📜.gitignore
 ┣ 📜README.md
 ┣ 📜main.py
 ┗ 📜requirements.txt
```

> "EXE" folder contains zip file with compiled .exe file and .db for saving all app data. ***This is what you want!***

## For updates and contributors, see: [ControlMicTray GitHub](https://github.com/Sif-on/ControlMicTray)