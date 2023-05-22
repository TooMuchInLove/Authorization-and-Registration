# -*- coding: utf-8 -*-

from sqlite3 import connect
from sqlite3 import Error as SQLiteError

from config import TABLE_USER
from config import DB_SQLITE3

# Имя файла в директории
FileName = str
# Текстовые данные
Text = str
# Данные в виде списка
ListData = list


class Singleton:
    """ Класс для определения единственного экземпляра """
    _instance = None
    def __new__(cls, *args, **kwargs):
        """ Реализует вызов экземпляра класса """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Storage:
    """ Интерфейс для любого хранилища """
    def save(self, _data: ListData) -> None:
        pass

    def read(self) -> Text:
        pass


class StorageSQL(Storage):
    """ Хранилище данных в табличном формате """
    def create_table(self) -> None:
        pass


class StorageSQLite3DB(StorageSQL, Singleton):
    """ База данных SQLite3 """
    def __init__(self) -> None:
        # Подключение к базе
        self.connection()
        # Создание таблиц
        self.create_table()

    def connection(self) -> None:
        """ Подключение к БД """
        try:
            # Подключение к базе
            self.__connect = connect(DB_SQLITE3)
            # Создание курсора для запросов в базу
            self.__cursor = self.__connect.cursor()
        except SQLiteError as error:
            print(error)

    def create_table(self) -> None:
        """ Создание таблицы для БД """
        self.__cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_USER}(
                login TEXT PRIMARY KEY,
                password TEXT,
                datetime TEXT
            );
        """)

    def save(self, _data: ListData) -> None:
        """ Сохранение данных в БД """
        self.__cursor.execute(
            f"INSERT or IGNORE INTO {TABLE_USER} VALUES (?, ?, ?);", (_data)
        )
        self.__connect.commit()

    def read(self) -> ListData:
        """ Чтение данных из БД """
        self.__cursor.execute(f"SELECT login, password FROM {TABLE_USER};")
        return [item for item in self.__cursor.fetchall()]

    def __del__(self):
        """ Разрываем соединение с базой """
        self.__connect.close()


def save_data(_data: ListData, _storage: Storage) -> None:
    _storage.save(_data)


def read_data(_storage: Storage) -> ListData:
    return _storage.read()
