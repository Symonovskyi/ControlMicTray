# Built-in modules and own classes.
from sqlite3 import connect
from os import path
from getpass import getuser


class DatabaseController:
    def __init__(self):
        self.__db_name = "ControlMicTray.db"
        self.__user_name = getuser()
        self.__checkDatabaseForExistence()

    def __checkDatabaseForExistence(self):
        if not path.exists(self.__db_name):
            with connect(self.__db_name) as db:
                cursor = db.cursor()

                cursor.execute("""CREATE TABLE UserSettings(
                    UserName text,
                    UserHotkey text,
                    AppTheme bool);""")

                db.commit()

                cursor.execute(f"""
                INSERT INTO UserSettings VALUES\
                    (\'{self.__user_name}\', NULL, NULL)
                """)

                db.commit()

    @property
    def getUserHotkey(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            user_hotkey = cursor.execute(f"""SELECT UserHotkey FROM\
                UserSettings WHERE UserName = \'{self.__user_name}\'""")

            db.commit()
            return user_hotkey

    @property
    def getUserTheme(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            user_theme = cursor.execute(f"""SELECT AppTheme FROM UserSettings\
                WHERE UserName = \'{self.__user_name}\'""")

            db.commit()
            return user_theme