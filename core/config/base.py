from enum import Enum
from dataclasses import dataclass

# Ширина приложения
WIDTH = 400
# Высота приложения / минимальная
HEIGHT_MIN = 300
# Высота приложения / максимальная
HEIGHT_MAX = 500
# Высота компонентов приложения
HEIGHT_WIDGETS = 30
# Максимальная длина строки в поле
MAX_LEN_FIELD = 100
# Задержка для всплывающего сообщения
TIMEOUT = 1500
# Кодирование
UTF8 = "utf-8"
# Соль для хэштрования пароля
SALT = b"\x83\x95\xe8g\xcd\xa2nx{\x0e\x94\xdf\x9a\xc4I\xd2JUs\x084c(\xeb)M\x86\xce\x8ff\xfc"
# Название БД
DB_SQLITE3 = "db/users.db"


class FontStyle(Enum):
    """ Список шрифтов и их размеров """
    VERDANA = "Verdana"
    SIZE_1 = 1
    SIZE_5 = 5
    SIZE_10 = 10
    SIZE_15 = 15
    SIZE_20 = 20
    SIZE_30 = 30
    SIZE_40 = 40


class Pallete(Enum):
    """ Цветовая палитра """
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    DARK_RED = "#D72323"
    ORANGE = "#FF9C00"
    DARK_GREY_1 = "#232323"
    DARK_GREY_2 = "#2A2A2A"
    LIGHT_GREY = "#CED6E0"
    DARK_BLUE = "#283149"
    LIGHT_BLUE = "#4C5C8A"


@dataclass(slots=True)
class Notification:
    """ Список уведомлений """
    EMPTY = "Поле пустое"
    REPEAT_PASSWORD = "Введите пароль ещё раз"
    INVALID_PASSWORD = "Пароль неверный. Попробуйте ещё раз"
    AUTHORIZATION_SUCCESSFUL = "Авторизация прошла успешно"
    USER_ALREADY_EXISTS = "Пользователь уже существует"
    USER_IS_REGISTERED = "Пользователь зарегистрирован"
    USER_NOT_FOUND = "Пользователь не найден"


@dataclass(slots=True)
class NameWidget:
    """ Список названий виджетов приложения """
    APP = "Glucose"
    BUTTON_OK = "Далее"
    BUTTON_CLOSE = "Закрыть ❌"
    PLACEHOLDER_LOGIN = "введите логин"
    PLACEHOLDER_PASSWORD = "введите пароль"
    PLACEHOLDER_REPEAT_PASSWORD = "введите пароль повторно"
    AUTHORIZATION = "Авторизация"
    REGISTRATION = "Регистрация"
