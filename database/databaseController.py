from sqlite3 import connect
from os import path
from getpass import getuser

class DatabaseController:
    """
    This class operates with database, which contains user settings.
    """
    def __init__(self):
        self.__db_name = "ControlMicTray.db"
        self.__user_name = getuser()
        self.initialize_database()

    def execute_sql(self, sql_commands):
        with connect(self.__db_name) as conn:
            cursor = conn.cursor()
            cursor.executescript(sql_commands)
            conn.commit()

    def initialize_database(self):
        if not path.exists(self.__db_name):
            self.create_tables()
            self.insert_initial_data()
            self.insert_user()
        else:
            self.update_about_data()
    
    def create_tables(self):
        sql_commands = f"""
        CREATE TABLE IF NOT EXISTS "User" (
            "ID"                INTEGER NOT NULL UNIQUE,
            "UserName"          VARCHAR(254) NOT NULL,
            PRIMARY KEY("ID" AUTOINCREMENT)
        );
        CREATE TABLE IF NOT EXISTS "Alerts" (
            "ID"                INTEGER NOT NULL UNIQUE,
            "AlertsType"        VARCHAR(254) NOT NULL,
            "StandardSound"     VARCHAR(254) NOT NULL,
            "OwnSound"          VARCHAR(254),
            FOREIGN KEY("ID")   REFERENCES "User"("ID"),
            PRIMARY KEY("ID" AUTOINCREMENT)
        );
        CREATE TABLE IF NOT EXISTS "Autorun" (
            "ID"                INTEGER NOT NULL UNIQUE,
            "EnableProgram"     INTEGER NOT NULL,
            "EnableMic"         INTEGER NOT NULL,
            "MicStatus"         INTEGER NOT NULL,
            "WalkieStatus"      INTEGER NOT NULL,
            FOREIGN KEY("ID")   REFERENCES "User"("ID"),
            PRIMARY KEY("ID" AUTOINCREMENT)
        );
        CREATE TABLE IF NOT EXISTS "Hotkey" (
            "ID"                INTEGER NOT NULL UNIQUE,
            "HotkeyMic"         VARCHAR(32),
            "HotkeyWalkie"      VARCHAR(32),
            FOREIGN KEY("ID")   REFERENCES "User"("ID"),
            PRIMARY KEY("ID" AUTOINCREMENT)
        );
        CREATE TABLE IF NOT EXISTS "Settings" (
            "ID"                INTEGER NOT NULL UNIQUE,
            "LanguageCode"      VARCHAR(4) NOT NULL,
            "NightTheme"        INTEGER NOT NULL,
            "PrivacyStatus"     INTEGER NOT NULL,
            FOREIGN KEY("ID")   REFERENCES "User"("ID"),
            PRIMARY KEY("ID" AUTOINCREMENT)
        );
        CREATE TABLE IF NOT EXISTS "About" (
            "ID"                INTEGER NOT NULL UNIQUE,
            "ProgramVersion"    VARCHAR(32) NOT NULL,
            "WebSite"           VARCHAR(32) NOT NULL,
            "Email"             VARCHAR(32) NOT NULL,
            "Copyright"         VARCHAR(64) NOT NULL,
            "UrlPrivacyPolicy"  VARCHAR(64) NOT NULL,
            PRIMARY KEY("ID" AUTOINCREMENT)
        );
        """
        self.execute_sql(sql_commands)

    def insert_user(self):
        sql_command = f"INSERT INTO 'User' (UserName) VALUES ('{self.__user_name}');"
        self.execute_sql(sql_command)


    def insert_initial_data(self):
        sql_commands = f"""
        INSERT INTO 'User' (UserName) VALUES ('{self.__user_name}');
        INSERT INTO "Alerts" (AlertsType, StandardSound, OwnSound) VALUES ('Off', '\Sound\StandardSound.mp3', NULL);
        INSERT INTO "Autorun" (EnableProgram, EnableMic, MicStatus, WalkieStatus) VALUES (1, 0, 1, 0);
        INSERT INTO "Hotkey" (HotkeyMic, HotkeyWalkie) VALUES ('Scroll_lock', 'Pause');
        INSERT INTO "Settings" (LanguageCode, NightTheme, PrivacyStatus) VALUES ('ru', 1, 0);
        INSERT INTO "About" (ProgramVersion, WebSite, Email, Copyright, UrlPrivacyPolicy) VALUES ('v.2024.04.04', 'https://controlmictray.pp.ua', 'i@controlmictray.pp.ua', 'Copyright © 2024\nSymonovskyi & Lastivka\nAll rights reserved', 'https://controlmictray.pp.ua/PrivacyPolicy.html');
        """
        self.execute_sql(sql_commands)

    def drop_tables(self):
        sql_commands = f"""
        DROP TABLE IF EXISTS "About";
        DROP TABLE IF EXISTS "Settings";
        DROP TABLE IF EXISTS "Hotkey";
        DROP TABLE IF EXISTS "Autorun";
        DROP TABLE IF EXISTS "Alerts";
        DROP TABLE IF EXISTS "User";
        """
        self.execute_sql(sql_commands)

    def update_about_data(self):
        sql_commands = f"""
        UPDATE "About"
        SET ProgramVersion = 'v.2024.04.04', WebSite = 'https://controlmictray.pp.ua', Email = 'i@controlmictray.pp.ua', Copyright = 'Copyright © 2024\nSymonovskyi & Lastivka\nAll rights reserved', UrlPrivacyPolicy = 'https://controlmictray.pp.ua/PrivacyPolicy.html';
        """
        self.execute_sql(sql_commands)

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
