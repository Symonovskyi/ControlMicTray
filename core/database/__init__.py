from sqlite3 import Connection, connect as sql_conn
from os import path
from getpass import getuser
from threading import RLock


class DatabaseManager:
    """
    Singleton manager for database operations.
    Thread-safe implementation using RLock for concurrent access protection.
    
    DB Layer only — no dependencies on UI or Logic layers.
    """

    _instance: "DatabaseManager" = None
    _db_name: str = "ControlMicTray.db"
    _user_name: str = getuser()
    _connection: Connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = sql_conn(cls._db_name, check_same_thread=False)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._lock = RLock()
        self.initialize_database()

    def execute_sql(self, sql_commands: str, is_select: bool = False):
        """Execute SQL command with thread safety."""
        with self._lock:
            with self._connection as conn:
                cursor = conn.cursor()
                if is_select:
                    cursor.execute(sql_commands)
                    result = cursor.fetchone()
                    return result[0] if result else None
                else:
                    cursor.executescript(sql_commands)
                    conn.commit()

    def initialize_database(self):
        """Initialize database schema and default data."""
        self.create_tables()

        if not self.user_exists():
            self.insert_initial_data()
            self.insert_user()
        else:
            self.update_about_data()

        self._initialized = True

    def user_exists(self) -> bool:
        """Check if current user exists in database."""
        sql_command = f"SELECT 1 FROM 'User' WHERE UserName = '{self._user_name}';"
        return self.execute_sql(sql_command, is_select=True) is not None

    def create_tables(self):
        """Create all database tables."""
        sql_commands = """
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
            "Theme"             INTEGER NOT NULL,
            "PrivacyStatus"     INTEGER NOT NULL,
            "ForcedMute"        INTEGER NOT NULL,
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
        """Insert current user into database."""
        sql_command = f"INSERT INTO 'User' (UserName) VALUES ('{self._user_name}');"
        self.execute_sql(sql_command)

    def insert_initial_data(self):
        """Insert default application settings."""
        sql_commands = f"""
        INSERT INTO 'User' (UserName) VALUES ('{self._user_name}');
        INSERT INTO "Alerts" (AlertsType, StandardSound, OwnSound) VALUES ('Off', '\\Sound\\StandardSound.mp3', NULL);
        INSERT INTO "Autorun" (EnableProgram, EnableMic, MicStatus, WalkieStatus) VALUES (1, 0, 1, 0);
        INSERT INTO "Hotkey" (HotkeyMic, HotkeyWalkie) VALUES ('Scroll_lock', 'Pause');
        INSERT INTO "Settings" (LanguageCode, Theme, PrivacyStatus, ForcedMute) VALUES ('ru', 1, 0, 1);
        INSERT INTO "About" (ProgramVersion, WebSite, Email, Copyright, UrlPrivacyPolicy) VALUES ('v.2024.04.04', 'https://controlmictray.pp.ua', 'i@controlmictray.pp.ua', 'Copyright © 2024\nSymonovskyi & Lastivka\nAll rights reserved', 'https://controlmictray.pp.ua/PrivacyPolicy.html');
        """
        self.execute_sql(sql_commands)

    def drop_tables(self):
        """Drop all database tables."""
        sql_commands = """
        DROP TABLE IF EXISTS "About";
        DROP TABLE IF EXISTS "Settings";
        DROP TABLE IF EXISTS "Hotkey";
        DROP TABLE IF EXISTS "Autorun";
        DROP TABLE IF EXISTS "Alerts";
        DROP TABLE IF EXISTS "User";
        """
        self.execute_sql(sql_commands)

    def update_about_data(self):
        """Update About table with current version info."""
        sql_commands = """
        UPDATE "About"
        SET ProgramVersion = 'v.2024.04.04', WebSite = 'https://controlmictray.pp.ua', Email = 'i@controlmictray.pp.ua', Copyright = 'Copyright © 2024\nSymonovskyi & Lastivka\nAll rights reserved', UrlPrivacyPolicy = 'https://controlmictray.pp.ua/PrivacyPolicy.html';
        """
        self.execute_sql(sql_commands)

    def get_property(self, table_name: str, column_name: str):
        """Get property value for current user."""
        sql = f"""
               SELECT "{column_name}" FROM "{table_name}"
               WHERE "ID" = (
                   SELECT "ID" FROM "User" WHERE "UserName" = '{self._user_name}'
               )
              """
        return self.execute_sql(sql, is_select=True)

    def set_property(self, table_name: str, column_name: str, value):
        """Set property value for current user."""
        with self._lock:
            sql = f"""
                   UPDATE "{table_name}"
                   SET "{column_name}" = ?
                   WHERE "ID" = (
                       SELECT "ID" FROM "User" WHERE "UserName" = '{self._user_name}'
                   )
                  """
            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (value,))
                conn.commit()
