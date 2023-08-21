# -*- coding: utf-8 -*-

from typing import Callable
from hashlib import pbkdf2_hmac
from datetime import datetime

from gui.ui import Ui_Application

from storage import DataBaseSQLite3
from storage import saver
from storage import reader

from core.config.config import Notification as Ntf
from core.config.config import UTF8
from core.config.config import TIMEOUT
from core.config.config import SALT

from gui.theme import STYLE_ERROR
from gui.theme import STYLE_NOTIFICATION


class ServiceGlucose:
    """ Бизнес-логика главного приложения """
    def __init__(self) -> None:
        # Пользовательский интерфейс и компоненты
        self.__app = Ui_Application()
        # Флаг для проверки формы: регистрация или авторизация
        self.__isRA = False
        # Флаг для проверки режима видимости пароля
        self.__isEchoMode = False
        # События кнопок
        self.__app.pbCheck.clicked.connect(self.__event_check_form_registration)
        self.__app.pbVisible.clicked.connect(self.__event_check_echo_mode)
        self.__app.pbOk.clicked.connect(self.__event_check_registration_or_authorization)
        self.__app.pbClose.clicked.connect(self.__event_close_window)
        # Запуск таймера, после установка метода .start()
        self.__app.Timer.timeout.connect(self.__event_tick_timer)

    def __event_tick_timer(self) -> None:
        """ Запуск таймера в приложении """
        self.__app.Timer.stop()
        # Убираем уведомление с экрана
        self.__app.lbNotification.setVisible(False)

    def __popup_notification(self, _text: str, _style: str) -> None:
        """ Устанавливаем текст/стиль/видимость для уведомления """
        self.__app.lbNotification.setText(_text)
        self.__app.lbNotification.setStyleSheet(_style)
        self.__app.lbNotification.setVisible(True)
        # Запуск таймера для отображения уведомлений
        self.__app.Timer.start(TIMEOUT)

    def __event_check_form_registration(self) -> None:
        """ Проверяем форму: регистрация или авторизация """
        self.__app.go_authorizator() if self.__isRA else self.__app.go_registration()
        self.set_flag_registration_or_authorization()

    def __event_check_echo_mode(self) -> None:
        """ Проверяем форму: режим видимости пароля """
        self.__app.go_password_echo_mode() if self.__isEchoMode else self.__app.go_normal_echo_mode()
        self.__isEchoMode = -self.__isEchoMode+1

    def __event_check_registration_or_authorization(self) -> None:
        """ Проверяем пользователя: регистрация или авторизация """
        # Введённый логин
        login = self.get_login()
        # Введённый пароль
        password = self.get_password()
        # Проверяем содержимое поля (логин пользователя)
        if self.__go_check_field(self.__app.set_focus_in_login_field,
                                 Ntf.EMPTY.value, login): return None
        # Данные из БД
        response_data = reader(DataBaseSQLite3())
        if self.__isRA:
            # Работа с формой регистрации
            self.__go_user_registration(login, password, response_data)
            return None
        # Работа с формой авторизации
        self.__go_user_authorization(login, password, response_data)

    def __event_close_window(self) -> None:
        """ Закрытие приложения """
        self.__app.close()

    def __go_user_registration(self, _login: str, _password: str,
                               _response_db: list) -> None:
        """ Перейти к регистрации пользователя """
        for user, _ in _response_db:
            if _login == user:
                self.__popup_notification(Ntf.USER_ALREADY_EXISTS.value, STYLE_NOTIFICATION)
                self.__app.goto_reset_password_in_field()
                return None
        if self.__go_check_field(self.__app.set_focus_in_password_field,
                                 Ntf.EMPTY.value, _password): return None
        # Введённый пароль (повторно)
        repeat_password = self.get_repeat_password()
        if self.__go_check_field(self.__app.set_focus_in_repeat_password_field,
                                 Ntf.REPEAT_PASSWORD.value, repeat_password): return None
        if self.__go_check_fields(self.__app.set_focus_in_repeat_password_field,
                                  Ntf.INVALID_PASSWORD.value, repeat_password, _password): return None
        # Сохранение пользователя
        saver([_login, get_hash_password(_password), get_datetime_now()], DataBaseSQLite3())
        self.__popup_notification(Ntf.USER_IS_REGISTERED.value, STYLE_NOTIFICATION)
        self.__app.goto_reset_password_in_field()
        self.__app.go_authorizator()
        self.set_flag_registration_or_authorization()

    def __go_user_authorization(self, _login: str, _password: str,
                                _response_db: list) -> None:
        """ Перейти к авторизации пользователя """
        if self.__go_check_field(self.__app.set_focus_in_password_field,
                                 Ntf.EMPTY.value, _password): return None
        for user, passw in _response_db:
            if _login == user:
                if self.__go_check_fields(self.__app.set_focus_in_password_field,
                                          Ntf.INVALID_PASSWORD.value,
                                          get_hash_password(_password), passw): return None
                self.__popup_notification(Ntf.AUTHORIZATION_SUCCESSFUL.value, STYLE_NOTIFICATION)
                self.__app.delete_all_widgets()
                self.__app.create_new_comp(_login)
                return None
        self.__popup_notification(Ntf.USER_NOT_FOUND.value, STYLE_ERROR)
        self.__app.goto_reset_password_in_field()
        self.__app.set_focus_in_login_field()

    def __go_check_field(self, _function: Callable, _message: str,
                         _field0: str) -> bool:
        """ Проверяем значение поля на пустоту, если пустое - возвращаем сообщение """
        if not _field0:
            _function()
            self.__popup_notification(_message, STYLE_ERROR)
            return True
        return False

    def __go_check_fields(self, _function: Callable, _message: str,
                           _field0: str, _field1: str) -> bool:
        """ Проверяем поля на схожесть (сравниваем их) """
        if _field0 != _field1:
            _function()
            self.__popup_notification(_message, STYLE_ERROR)
            return True
        return False

    def set_flag_registration_or_authorization(self) -> None:
        """ Устанавливаем флаг для проверки формы: регистрация или авторизация """
        self.__isRA = -self.__isRA + 1

    def get_login(self) -> str:
        """ Получить текст (логин) из поля """
        return self.__app.leLogin.text().strip()

    def get_password(self) -> str:
        """ Получить текст (пароль) из поля """
        return self.__app.lePassword.text().strip()

    def get_repeat_password(self) -> str:
        """ Получить текст (повторяющийся пароль) из поля """
        return self.__app.leRepeatPassword.text().strip()


def get_datetime_now() -> str:
    """ Получаем текущую дату и время в формате <<20.04.2023 01:52:00>> """
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def get_hash_password(_password: str) -> bytes:
    """ Хешируем пароль пользователя (алгоритм sha256) """
    return pbkdf2_hmac( # 32 байта
        "sha256", # Используемый алгоритм хеширования
        _password.encode(UTF8), # Конвертируется пароль в байты
        SALT, # Предоставляется соль
        100000, # Рекомендуется использоваться по крайней мере 100000 итераций SHA-256
        dklen=32, # Получает ключ 32 байта
    )
