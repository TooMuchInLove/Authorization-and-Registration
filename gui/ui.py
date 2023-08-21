# -*- coding: utf-8 -*-

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from core.config.config import NameWidget as NW
from core.config.config import WIDTH
from core.config.config import HEIGHT_MIN
from core.config.config import HEIGHT_MAX
from core.config.config import HEIGHT_WIDGETS
from core.config.config import MAX_LEN_FIELD

from theme import LIGHT_THEME


class Ui_Application(QWidget):
    """ Набор визуальных компонентов приложения """
    def __init__(self) -> None:
        super(Ui_Application, self).__init__()
        # Размер окна приложения
        self.setMinimumSize(QSize(WIDTH, HEIGHT_MIN))
        self.setMaximumSize(QSize(WIDTH, HEIGHT_MAX))
        # Стиль приложения и виджетов
        self.setStyleSheet(LIGHT_THEME)
        # Отображение формы
        self.show()
        # Определяем параметры приложения
        self.setup_ui()
        # Устанавливаем названия виджетам
        self.setup_text()
        # Устанавливаем имена некоторым переменным
        self.setup_object_name()
        # Компоненты для авторизации
        self.go_authorizator()
        # Скрываем пароль
        self.go_password_echo_mode()

    def setup_ui(self) -> None:
        """ Виджеты приложения: регистрация или авторизация """
        self.lbLogin = QLabel()
        self.leLogin = QLineEdit()
        self.lePassword = QLineEdit()
        self.leRepeatPassword = QLineEdit()
        self.pbCheck = QPushButton()
        self.pbVisible = QPushButton()
        self.pbOk = QPushButton()
        self.pbClose = QPushButton()
        # Таймер, уделённый под сообщения
        self.Timer = QTimer()
        # Размер виджетов
        self.leLogin.setMinimumSize(QSize(WIDTH, HEIGHT_WIDGETS))
        self.leLogin.setMaxLength(MAX_LEN_FIELD)
        self.lePassword.setMinimumSize(QSize(WIDTH, HEIGHT_WIDGETS))
        self.lePassword.setMaxLength(MAX_LEN_FIELD)
        self.leRepeatPassword.setMinimumSize(QSize(WIDTH, HEIGHT_WIDGETS))
        self.leRepeatPassword.setMaxLength(MAX_LEN_FIELD)
        self.pbCheck.setMinimumSize(QSize(0, HEIGHT_WIDGETS))
        self.pbVisible.setMinimumSize(QSize(HEIGHT_WIDGETS, HEIGHT_WIDGETS))
        self.pbOk.setMinimumSize(QSize(int(WIDTH/2), HEIGHT_WIDGETS))
        self.pbClose.setMinimumSize(QSize(int(WIDTH/2), HEIGHT_WIDGETS))
        # Разметка виджетов приложения
        self.gridlayout = QGridLayout(self)
        self.gridlayout.addWidget(self.pbCheck, 0, 0, alignment=Qt.AlignRight | Qt.AlignTop)
        self.gridlayout.addWidget(self.lbLogin, 1, 0, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.gridlayout.addWidget(self.leLogin, 2, 0, alignment=Qt.AlignCenter | Qt.AlignBottom)
        self.gridlayout.addWidget(self.lePassword, 3, 0, alignment=Qt.AlignCenter | Qt.AlignCenter)
        self.gridlayout.addWidget(self.pbVisible, 3, 0, alignment=Qt.AlignRight | Qt.AlignCenter)
        self.gridlayout.addWidget(self.leRepeatPassword, 4, 0, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.gridlayout.addWidget(self.pbOk, 5, 0, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.gridlayout.addWidget(self.pbClose, 5, 0, alignment=Qt.AlignRight | Qt.AlignBottom)
        # Лэйбл для отображения ошибок или уведомлений
        self.lbNotification = QLabel(self)
        self.lbNotification.setGeometry(QRect(0, 5, WIDTH, HEIGHT_WIDGETS*2))
        self.lbNotification.setVisible(False)

    def setup_text(self) -> None:
        """ Устанавливаем текст для виджетов """
        self.setWindowTitle(NW.APP.value)
        self.leLogin.setPlaceholderText(NW.PLACEHOLDER_LOGIN.value)
        self.lePassword.setPlaceholderText(NW.PLACEHOLDER_PASSWORD.value)
        self.leRepeatPassword.setPlaceholderText(NW.PLACEHOLDER_REPEAT_PASSWORD.value)
        self.pbOk.setText(NW.BUTTON_OK.value)
        self.pbClose.setText(NW.BUTTON_CLOSE.value)

    def setup_object_name(self) -> None:
        """ Задаём некоторым виджетам имена для css (theme.py) """
        self.lbLogin.setObjectName("lbLogin")
        self.pbCheck.setObjectName("pbCheck")
        self.pbVisible.setObjectName("pbVisible")
        self.lbNotification.setObjectName("lbNotification")

    def set_focus_in_login_field(self) -> None:
        """ Установить фокус на поле с логином """
        self.leLogin.setFocus()

    def set_focus_in_password_field(self) -> None:
        """ Установить фокус на поле с паролем """
        self.lePassword.setFocus()

    def set_focus_in_repeat_password_field(self) -> None:
        """ Установить фокус на поле с паролем (повторно) """
        self.leRepeatPassword.setFocus()

    def go_authorizator(self) -> None:
        """ Пройдите авторизацию """
        self.leRepeatPassword.setVisible(False)
        self.pbCheck.setText(NW.REGISTRATION.value)
        self.lbLogin.setText(NW.AUTHORIZATION.value)

    def go_registration(self) -> None:
        """ Пройдите регистрацию """
        self.leRepeatPassword.setVisible(True)
        self.pbCheck.setText(NW.AUTHORIZATION.value)
        self.lbLogin.setText(NW.REGISTRATION.value)

    def goto_reset_password_in_field(self) -> None:
        """ Перейдите к сбросу пароля в поле ввода """
        self.lePassword.setText("")
        self.leRepeatPassword.setText("")

    def go_normal_echo_mode(self) -> None:
        """ Перейти в нормальный режим в поле """
        self.lePassword.setEchoMode(QLineEdit.EchoMode.Normal)
        self.leRepeatPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        self.pbVisible.setIcon(QIcon("../img/hidden.png"))
        self.pbVisible.setIconSize(QSize(HEIGHT_WIDGETS-10, HEIGHT_WIDGETS-10))

    def go_password_echo_mode(self) -> None:
        """ Перейти в режим пароля в поле """
        self.lePassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.leRepeatPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.pbVisible.setIcon(QIcon("../img/view.png"))
        self.pbVisible.setIconSize(QSize(HEIGHT_WIDGETS-10, HEIGHT_WIDGETS-10))

    def delete_all_widgets(self) -> None:
        """ Удаление всех виджетов для регистрации и авторизации """
        # self.lbLogin.deleteLater()
        self.leLogin.deleteLater()
        self.lePassword.deleteLater()
        self.leRepeatPassword.deleteLater()
        self.pbCheck.deleteLater()
        self.pbVisible.deleteLater()
        self.pbOk.deleteLater()
        self.pbClose.deleteLater()

    def create_new_comp(self, _login) -> None:
        """ ... """
        self.lbLogin.setText(f"Добро пожаловать, {_login}!")
        self.lbLogin.setWordWrap(True)
        # self.pbClose.setText("qwe")
