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

                sql_create = open("doc\\SQL\\CREATE_TABLES.sql")
                cursor.executescript(sql_create.read())
                sql_create.close()

                sql_data = open("doc\\SQL\\CREATE_DATE.sql")
                cursor.executescript(sql_data.read())
                sql_data.close()
                
                db.commit()
            db.close()

    # Getters.
    @property
    def user_name(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "UserName"
                           FROM "User"
                           WHERE "UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def hotkey_mic(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Hotkey"."HotkeyMic"
                           FROM "Hotkey", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def hotkey_walkie(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Hotkey"."HotkeyWalkie"
                           FROM "Hotkey", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def alerts_type(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Alerts"."AlertsType"
                           FROM "Alerts", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def standard_sound(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Alerts"."StandardSound"
                           FROM "Alerts", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def own_sound(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Alerts"."OwnSound"
                           FROM "Alerts", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def enable_program(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Autorun"."EnableProgram"
                           FROM "Autorun", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def enable_mic(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Autorun"."EnableMic"
                           FROM "Autorun", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def language_code(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Settings"."LanguageCode"
                           FROM "Settings", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def night_theme(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Settings"."NightTheme"
                           FROM "Settings", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def privacy_status(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Settings"."PrivacyStatus"
                           FROM "Settings", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def program_version(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "About"."ProgramVersion"
                           FROM "About", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def web_site(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "About"."WebSite"
                           FROM "About", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def email(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "About"."Email"
                           FROM "About", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def copyright(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "About"."Copyright"
                           FROM "About", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    @property
    def url_privacy_policy(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "About"."UrlPrivacyPolicy"
                           FROM "About", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            user_hotkey = cursor.fetchone()
        db.close()
        return user_hotkey[0]

    # Setters.
    @hotkey_mic.setter
    def hotkey_mic(self, value=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Hotkey"
                           SET "HotkeyWalkie" = \'{value}\'
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            db.commit()
        db.close()

    @hotkey_walkie.setter
    def hotkey_walkie(self, value=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Hotkey"
                           SET "HotkeyMic" = \'{value}\'
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            db.commit()
        db.close()

    @alerts_type.setter
    def alerts_type(self, value=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Alerts"
                           SET "AlertsType" = \'{value}\'
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            db.commit()
        db.close()

    @standard_sound.setter
    def standard_sound(self, value=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Alerts"
                           SET "StandardSound" = \'{value}\'
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            db.commit()
        db.close()

    @own_sound.setter
    def own_sound(self, value=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Alerts"
                           SET "OwnSound" = \'{value}\'
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            db.commit()
        db.close()

    @enable_program.setter
    def enable_program(self, value=int):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Autorun"
                           SET "EnableProgram" = {value}
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            db.commit()
        db.close()

    @enable_mic.setter
    def enable_mic(self, value=int):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Autorun"
                           SET "EnableMic" = {value}
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            db.commit()
        db.close()

    @language_code.setter
    def language_code(self, value=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Settings"
                           SET "LanguageCode" = \'{value}\'
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            db.commit()
        db.close()

    @night_theme.setter
    def night_theme(self, value=int):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Settings"
                           SET "NightTheme" = {value}
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            db.commit()
        db.close()

    @privacy_status.setter
    def privacy_status(self, value=int):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Settings"
                           SET "PrivacyStatus" = {value}
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            db.commit()
        db.close()
