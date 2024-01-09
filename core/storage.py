from sqlite3 import connect as sqlite3_connect, Error as SQLiteError
from core.config.base import DB_SQLITE3


class Singleton:
    """ Класс для определения единственного экземпляра (паттерн Синглтон) """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Реализует вызов экземпляра класса """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class IStorage:
    """ Интерфейс для любого хранилища """
    def connect(self) -> None:
        pass

    def save(self, _data: list) -> None:
        pass

    def read(self) -> list:
        pass


class IStorageSQL(IStorage):
    """ Хранилище данных в табличном формате """
    def create_table(self) -> None:
        pass


class DataBaseSQLite3(IStorageSQL, Singleton):
    """ База данных SQLite3 """
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

    def create_table(self) -> None:
        """ Создание таблицы для БД """
        if self.connection is not None:  # FIXME: исправить на декоратор
            with self.connection.cursor() as cursor:
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS user(
                    login TEXT PRIMARY KEY,
                    password TEXT,
                    datetime TEXT);""")

    def save(self, _data: list) -> None:
        """ Сохранение данных в БД """
        if self.connection is not None:  # FIXME: исправить на декоратор
            with self.connection.cursor() as cursor:
                cursor.execute(f"INSERT or IGNORE INTO user VALUES (?, ?, ?);", (_data))
            self.connection.commit()

    def read(self) -> list:
        """ Чтение данных из БД """
        if self.connection is not None:  # FIXME: исправить на декоратор
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT login, password FROM user;")
                return [item for item in cursor.fetchall()]

    def __del__(self):
        """ Разрываем соединение с базой """
        if self.connection is not None:  # FIXME: исправить на декоратор
            self.connection.close()


def saver(_data: list, _storage: IStorage) -> None:
    _storage.save(_data)


def reader(_storage: IStorage) -> list:
    return _storage.read()
