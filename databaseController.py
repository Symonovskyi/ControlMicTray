# Built-in modules and own classes.
from sqlite3 import connect
from os import path
from getpass import getuser


class DatabaseController:
    """
    This class operates with database, which contains user settings.

    Properties. For all of these implemented getters and setters:
    - user_language - holds string of current language using by user.
    - user_hotkey_mic - holds string about the current hotkey combination for
    turning mic on/off.
    - user_hotkey_walkie - holds string about the current hotkey combination
    for turning walkie-talkie mode on.
    - on_startup_setting - holds boolean about the setting 'is app starting on
    system boot or not'.
    - user_theme - holds boolean about the app theme. 0 - white, 1 - gray.
    """

    def __init__(self):
        self.__db_name = "ControlMicTray.db"
        self.__user_name = getuser()
        self.__checkDatabaseForExistence()

    def __checkDatabaseForExistence(self):
        if not path.exists(self.__db_name):
            with connect(self.__db_name) as db:
                cursor = db.cursor()

                # Creating tables.
                cursor.execute("""
                               CREATE TABLE "User" (
                                   "ID"	INTEGER NOT NULL UNIQUE,
                                   "UserName"	VARCHAR(254) NOT NULL,
                                   PRIMARY KEY("ID" AUTOINCREMENT)
                               );
                               CREATE TABLE "Alerts" (
                                   "ID"	INTEGER NOT NULL UNIQUE,
                                   "AlertsType"	VARCHAR(254) NOT NULL,
                                   "StandardSound"	VARCHAR(254) NOT NULL,
                                   "OwnSound"	VARCHAR(254),
                                   FOREIGN KEY("ID") REFERENCES "User"("ID"),
                                   PRIMARY KEY("ID" AUTOINCREMENT)
                               );
                               CREATE TABLE "Autorun" (
                                   "ID"	INTEGER NOT NULL UNIQUE,
                                   "EnableProgram"	INTEGER NOT NULL,
                                   "EnableMic"	INTEGER NOT NULL,
                                   PRIMARY KEY("ID" AUTOINCREMENT),
                                   FOREIGN KEY("ID") REFERENCES "User"("ID")
                               );
                               CREATE TABLE "Hotkey" (
                                   "ID"	INTEGER NOT NULL UNIQUE,
                                   "HotkeyMic"	VARCHAR(32),
                                   "HotkeyWalkie"	VARCHAR(32),
                                   PRIMARY KEY("ID" AUTOINCREMENT),
                                   FOREIGN KEY("ID") REFERENCES "User"("ID")
                               );
                               CREATE TABLE "Settings" (
                                   "ID"	INTEGER NOT NULL UNIQUE,
                                   "LanguageCode"	VARCHAR(4) NOT NULL,
                                   "NightTheme"	INTEGER NOT NULL,
                                   FOREIGN KEY("ID") REFERENCES "User"("ID"),
                                   PRIMARY KEY("ID" AUTOINCREMENT)
                               );
                               CREATE TABLE "About" (
                                   "ID"	INTEGER NOT NULL UNIQUE,
                                   "ProgramVersion"	VARCHAR(32) NOT NULL,
                                   "WebSite"	VARCHAR(32) NOT NULL,
                                   "Email"	VARCHAR(32) NOT NULL,
                                   "Copyright"	VARCHAR(64) NOT NULL,
                                   "UrlPrivacyPolicy"	VARCHAR(64) NOT NULL,
                                   PRIMARY KEY("ID" AUTOINCREMENT)
                               );
                               """)

                # Appending datas by default.
                cursor.execute(f"""
                               INSERT INTO "User" (UserName) VALUES ('{self.__user_name}');
                               INSERT INTO "Alerts" (AlertsType, StandardSound, OwnSound) VALUES ('Off', '\Sound\StandardSound.mp3', (NULL));
                               INSERT INTO "Autorun" (EnableProgram, EnableMic) VALUES (1, 1);
                               INSERT INTO "Hotkey" (HotkeyMic, HotkeyWalkie) VALUES ('Scroll lock', 'HOME');
                               INSERT INTO "Settings" (LanguageCode, NightTheme) VALUES ('rus', 1);
                               INSERT INTO "About" (ProgramVersion, WebSite, Email, Copyright, UrlPrivacyPolicy) VALUES ('v.1.2022.01.31-alpha', 'https://controlmictray.pp.ua/', 'info@controlmictray.pp.ua', 'Copyright © 2022\nSimonovskiy & Lastivka\nAll rights reserved', 'https://controlmictray.pp.ua/PrivacyPolicy.html');
                               """)

                db.commit()
            db.close()
