from sqlite3 import connect as sqlite3_connect, Error as SQLiteError, Cursor, Connection
from typing import Callable
from core.config.base import DB_SQLITE3, Notification as N


def is_connection_check(message: str) -> Callable:
    def _wrapper_function(function: Callable) -> Callable:
        def _wrapper(self, *args):
            if self.connection is not None:
                return function(self, *args)
            print(message)
        return _wrapper
    return _wrapper_function


class Singleton:
    """ Класс для определения единственного экземпляра (паттерн Синглтон) """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Реализует вызов экземпляра класса """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class CursorForSqlite:
    """ Контекстный менеджер для курсора. """
    __slots__ = ("__connection", "__cursor",)

    def __init__(self, connection: Connection) -> None:
        self.__connection = connection

    def __enter__(self) -> Cursor:
        self.__cursor = self.__connection.cursor()
        return self.__cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__cursor.close()


class IStorage:
    """ Интерфейс для любого хранилища """
    __slots__ = ()
    
    def connect(self) -> None:
        pass

    def save(self, _data: list) -> None:
        pass

    def read(self) -> list:
        pass


class IStorageSQL(IStorage):
    """ Хранилище данных в табличном формате """
    __slots__ = ()
    
    def create_table(self) -> None:
        pass


class DataBaseSQLite3(IStorageSQL, Singleton):
    """ База данных SQLite3 """
    __slots__ = ("connection",)
    
    def __init__(self) -> None:
        self.connection = None
        self.connect()
        self.create_table()

    def connect(self) -> None:
        """ Подключение к БД """
        try:
            # Подключение к базе
            self.connection = sqlite3_connect(DB_SQLITE3)
        except SQLiteError as error:
            print(error)

    @is_connection_check(message=N.CONNECTION_PROBLEMS)
    def create_table(self) -> None:
        """ Создание таблицы для БД """
        with CursorForSqlite(self.connection) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS user(
                login TEXT PRIMARY KEY,
                password TEXT,
                datetime TEXT);""")

    @is_connection_check(message=N.CONNECTION_PROBLEMS)
    def save(self, _data: list) -> None:
        """ Сохранение данных в БД """
        with CursorForSqlite(self.connection) as cursor:
            cursor.execute(f"INSERT or IGNORE INTO user VALUES (?, ?, ?);", (_data))
        self.connection.commit()

    @is_connection_check(message=N.CONNECTION_PROBLEMS)
    def read(self) -> list:
        """ Чтение данных из БД """
        with CursorForSqlite(self.connection) as cursor:
            cursor.execute(f"SELECT login, password FROM user;")
            return [item for item in cursor.fetchall()]

    def __del__(self):
        """ Разрываем соединение с базой """
        if self.connection is not None:
            self.connection.close()


def saver(_data: list, _storage: IStorage) -> None:
    _storage.save(_data)


def reader(_storage: IStorage) -> list:
    return _storage.read()
