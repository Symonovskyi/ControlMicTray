# Built-in modules and own classes.
from sqlite3 import connect
from os import path
from getpass import getuser
from absolutePath import loadFile


class DatabaseController:
    """
    This class operates with database, which contains user settings.
    """
    def __init__(self):
        self.__db_name = "ControlMicTray.db"
        self.__user_name = getuser()
        self.__checkDatabaseForExistence()

    def __checkDatabaseForExistence(self):
        if not path.exists(self.__db_name):
            with connect(self.__db_name) as db:
                cursor = db.cursor()

                sql_create = open(loadFile("database/SQL/CREATE_TABLES.sql"))
                cursor.executescript(sql_create.read())
                sql_create.close()

                cursor.execute(
                    f"INSERT INTO 'User' (UserName) VALUES ('{self.__user_name}')")

                sql_data = open(loadFile("database/SQL/CREATE_DATA.sql"))
                cursor.executescript(sql_data.read())
                sql_data.close()

                db.commit()
            db.close()
        elif path.exists(self.__db_name):
            with connect(self.__db_name) as db:
                cursor = db.cursor()

                about_data = open(loadFile("database/SQL/UPDATE_ABOUT_DATA.sql"))
                cursor.executescript(about_data.read())
                about_data.close()

                db.commit()
            db.close()

    # Getters.

    @property
    def user_id(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "ID"
                           FROM "User"
                           WHERE "UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def user_name(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "UserName"
                           FROM "User"
                           WHERE "UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def hotkey_mic(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Hotkey"."HotkeyMic"
                           FROM "Hotkey", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def hotkey_walkie(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Hotkey"."HotkeyWalkie"
                           FROM "Hotkey", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def alerts_type(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Alerts"."AlertsType"
                           FROM "Alerts", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def standard_sound(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Alerts"."StandardSound"
                           FROM "Alerts", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def own_sound(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Alerts"."OwnSound"
                           FROM "Alerts", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def enable_program(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Autorun"."EnableProgram"
                           FROM "Autorun", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def enable_mic(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Autorun"."EnableMic"
                           FROM "Autorun", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def mic_status(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Autorun"."MicStatus"
                           FROM "Autorun", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def walkie_status(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Autorun"."WalkieStatus"
                           FROM "Autorun", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def language_code(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Settings"."LanguageCode"
                           FROM "Settings", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def night_theme(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Settings"."NightTheme"
                           FROM "Settings", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def privacy_status(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "Settings"."PrivacyStatus"
                           FROM "Settings", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def program_version(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "About"."ProgramVersion"
                           FROM "About", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def web_site(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "About"."WebSite"
                           FROM "About", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def email(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "About"."Email"
                           FROM "About", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def copyright(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "About"."Copyright"
                           FROM "About", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    @property
    def url_privacy_policy(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           SELECT "About"."UrlPrivacyPolicy"
                           FROM "About", "User"
                           WHERE "User"."UserName" = \'{self.__user_name}\'
                           """)
            value = cursor.fetchone()
        db.close()
        return value[0]

    # Setters.
    @hotkey_mic.setter
    def hotkey_mic(self, value=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Hotkey"
                           SET "HotkeyMic" = \'{value}\'
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
                           """)
            db.commit()
        db.close()

    @hotkey_walkie.setter
    def hotkey_walkie(self, value=str):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Hotkey"
                           SET "HotkeyWalkie" = \'{value}\'
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
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
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
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
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
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
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
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
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
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
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
                           """)
            db.commit()
        db.close()

    @mic_status.setter
    def mic_status(self, value=int):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Autorun"
                           SET "MicStatus" = {value}
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
                           """)
            db.commit()
        db.close()

    @walkie_status.setter
    def walkie_status(self, value=int):
        with connect(self.__db_name) as db:
            cursor = db.cursor()
            cursor.execute(f"""
                           UPDATE "Autorun"
                           SET "WalkieStatus" = {value}
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
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
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
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
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
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
                           WHERE ID = (
                                       SELECT "ID"
                                       FROM "User"
                                       WHERE "UserName" = \'{self.__user_name}\'
                                      )
                           """)
            db.commit()
        db.close()
