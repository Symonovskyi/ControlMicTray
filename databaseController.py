# Built-in modules and own classes.
from sqlite3 import connect
from os import path
from getpass import getuser


class DatabaseController:
    """
    This class operates with database, which contains user settings.

    Properties:
    - get_user_hotkey - holds info about the current hotkey user combination.
    - get_user_theme - holds info about the app theme that have beem chosen 
    by user.
    """
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
                    UserLanguage text,
                    UserHotkey text,
                    OnSysStartup bool,
                    AppTheme bool);""")

                cursor.execute(f"""
                INSERT INTO UserSettings VALUES\
                    (\'{self.__user_name}\', 'en', 'CTRL + SHIFT + Z',\
                        '1', '1')""")

                db.commit()
            db.close()

    @property
    def get_user_hotkey(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            user_hotkey = cursor.execute(f"""SELECT UserHotkey FROM\
                UserSettings WHERE UserName = \'{self.__user_name}\'""")
        
            db.commit()
        db.close()
        return user_hotkey

    @property
    def get_user_theme(self):
        with connect(self.__db_name) as db:
            cursor = db.cursor()

            user_theme = cursor.execute(f"""SELECT AppTheme FROM UserSettings\
                WHERE UserName = \'{self.__user_name}\'""")

            db.commit()
        db.close()
        return user_theme