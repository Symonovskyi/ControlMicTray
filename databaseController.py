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

                # Creating table UserSettings.
                cursor.execute("""CREATE TABLE UserSettings(
                    UserName text,
                    UserLanguage text,
                    UserHotkeyMic text,
                    UserHotkeyWalkie text,
                    OnSysStartup bool,
                    AppTheme bool);""")

                # Appending settings by default.
                cursor.execute(f"""
                    INSERT INTO UserSettings VALUES\
                        (\'{self.__user_name}\', 'en', 'Scroll lock',\
                            'HOME', '1', '1')""")

                db.commit()
            db.close()

    # Getters.
    @property
    def user_language(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute(f"""SELECT UserLanguage FROM\
                UserSettings WHERE UserName = \'{self.__user_name}\'""")
        
            user_lang = cursor.fetchone()
        db.close()
        return str(user_lang)[2:-3]

    @property
    def user_hotkey_mic(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute(f"""SELECT UserHotkeyMic FROM\
                UserSettings WHERE UserName = \'{self.__user_name}\'""")
        
            user_hotkey = cursor.fetchone()
        db.close()
        return str(user_hotkey)[2:-3]

    @property
    def user_hotkey_walkie(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute(f"""SELECT UserHotkeyWalkie FROM\
                UserSettings WHERE UserName = \'{self.__user_name}\'""")
        
            user_hotkey = cursor.fetchone()
        db.close()
        return str(user_hotkey)[2:-3]

    @property
    def user_on_startup_setting(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute(f"""SELECT OnSysStartup FROM\
                UserSettings WHERE UserName = \'{self.__user_name}\'""")

            on_sys_startup = cursor.fetchall()
        db.close()
        return str(on_sys_startup)[2:-3]

    @property
    def user_theme(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute(f"""SELECT AppTheme FROM UserSettings\
                WHERE UserName = \'{self.__user_name}\'""")

            user_theme = cursor.fetchall()
        db.close()
        return str(user_theme)[2:-3]

    #Setters.
    @user_language.setter
    def user_language(self, lang=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute(f"""UPDATE UserSettings SET UserLanguage = \
                \'{lang}\' WHERE UserName = \'{self.__user_name}\'""")

            db.commit()
        db.close()

    @user_hotkey_mic.setter
    def user_hotkey_mic(self, hotkey=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute(f"""UPDATE UserSettings SET UserHotkeyMic = \
                \'{hotkey}\' WHERE UserName = \'{self.__user_name}\'""")
        
            db.commit()
        db.close()

    @user_hotkey_walkie.setter
    def user_hotkey_walkie(self, hotkey=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute(f"""UPDATE UserSettings SET UserHotkeyWalkie = \
                \'{hotkey}\' WHERE UserName = \'{self.__user_name}\'""")
        
            db.commit()
        db.close()

    @user_on_startup_setting.setter
    def user_on_startup_setting(self, val=bool):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute(f"""UPDATE UserSettings SET OnSysStartup = \
                \'{val}\' WHERE UserName = \'{self.__user_name}\'""")
        
            db.commit()
        db.close()

    @user_theme.setter
    def user_theme(self, val=bool):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute(f"""UPDATE TOP (1) UserSettings SET AppTheme = \
                \'{val}\' WHERE UserName = \'{self.__user_name}\'""")
        
            db.commit()
        db.close()
