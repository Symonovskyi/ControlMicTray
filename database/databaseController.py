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

    def execute_sql(self, sql_commands, is_select=False):
        with connect(self.__db_name) as conn:
            cursor = conn.cursor()
            if is_select:
                cursor.execute(sql_commands)
                result = cursor.fetchone()
                return result[0] if result else None
            else:
                cursor.executescript(sql_commands)
                conn.commit()

    def initialize_database(self):
        if not path.exists(self.__db_name):
            self.create_tables()
            self.insert_initial_data()
            if not self.user_exists():
                self.insert_user()
        else:
            self.update_about_data()

    def user_exists(self):
        sql_command = f"SELECT 1 FROM 'User' WHERE UserName = '{self.__user_name}';"
        return self.execute_sql(sql_command, is_select=True) is not None

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

    def get_property(self, table_name, column_name):
        sql = f"""
               SELECT "{column_name}" FROM "{table_name}"
               WHERE "ID" = (
                   SELECT "ID" FROM "User" WHERE "UserName" = '{self.__user_name}'
               )
              """
        return self.execute_sql(sql, is_select=True)

    @property
    def user_id(self):
        return self.get_property("User", "ID")

    @property
    def user_name(self):
        return self.__user_name

    @property
    def hotkey_mic(self):
        return self.get_property("Hotkey", "HotkeyMic")

    @property
    def hotkey_walkie(self):
        return self.get_property("Hotkey", "HotkeyWalkie")

    @property
    def alerts_type(self):
        return self.get_property("Alerts", "AlertsType")

    @property
    def standard_sound(self):
        return self.get_property("Alerts", "StandardSound")

    @property
    def own_sound(self):
        return self.get_property("Alerts", "OwnSound")

    @property
    def enable_program(self):
        return self.get_property("Autorun", "EnableProgram")

    @property
    def enable_mic(self):
        return self.get_property("Autorun", "EnableMic")

    @property
    def mic_status(self):
        return self.get_property("Autorun", "MicStatus")

    @property
    def walkie_status(self):
        return self.get_property("Autorun", "WalkieStatus")

    @property
    def language_code(self):
        return self.get_property("Settings", "LanguageCode")

    @property
    def night_theme(self):
        return self.get_property("Settings", "NightTheme")

    @property
    def privacy_status(self):
        return self.get_property("Settings", "PrivacyStatus")

    @property
    def program_version(self):
        return self.get_property("About", "ProgramVersion")

    @property
    def web_site(self):
        return self.get_property("About", "WebSite")

    @property
    def email(self):
        return self.get_property("About", "Email")

    @property
    def copyright(self):
        return self.get_property("About", "Copyright")

    @property
    def url_privacy_policy(self):
        return self.get_property("About", "UrlPrivacyPolicy")

    def set_property(self, table_name, column_name, value):
        sql = f"""
               UPDATE "{table_name}"
               SET "{column_name}" = ?
               WHERE "ID" = (
                   SELECT "ID" FROM "User" WHERE "UserName" = '{self.__user_name}'
               )
              """
        with connect(self.__db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (value,))
            conn.commit()

    @hotkey_mic.setter
    def hotkey_mic(self, value):
        self.set_property("Hotkey", "HotkeyMic", value)

    @hotkey_walkie.setter
    def hotkey_walkie(self, value):
        self.set_property("Hotkey", "HotkeyWalkie", value)

    @alerts_type.setter
    def alerts_type(self, value):
        self.set_property("Alerts", "AlertsType", value)

    @standard_sound.setter
    def standard_sound(self, value):
        self.set_property("Alerts", "StandardSound", value)

    @own_sound.setter
    def own_sound(self, value):
        self.set_property("Alerts", "OwnSound", value)

    @enable_program.setter
    def enable_program(self, value):
        self.set_property("Autorun", "EnableProgram", value)

    @enable_mic.setter
    def enable_mic(self, value):
        self.set_property("Autorun", "EnableMic", value)

    @mic_status.setter
    def mic_status(self, value):
        self.set_property("Autorun", "MicStatus", value)

    @walkie_status.setter
    def walkie_status(self, value):
        self.set_property("Autorun", "WalkieStatus", value)

    @language_code.setter
    def language_code(self, value):
        self.set_property("Settings", "LanguageCode", value)

    @night_theme.setter
    def night_theme(self, value):
        self.set_property("Settings", "NightTheme", value)

    @privacy_status.setter
    def privacy_status(self, value):
        self.set_property("Settings", "PrivacyStatus", value)
