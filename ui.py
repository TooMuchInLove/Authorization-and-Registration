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

from config import NameWidget as NW
from config import WIDTH
from config import HEIGHT_MIN
from config import HEIGHT_MAX
from config import HEIGHT_WIDGETS
from config import MAX_LEN_FIELD

from theme import LIGHT_THEME


class Ui_Application(QWidget):
    """ Набор визуальных компонентов приложения """
    def __init__(self):
        super(Ui_Application, self).__init__()
        # Размер окна приложения
        self.setMinimumSize(QSize(WIDTH, HEIGHT_MIN))
        self.setMaximumSize(QSize(WIDTH, HEIGHT_MAX))
        # Стиль приложения и виджетов
        self.setStyleSheet(LIGHT_THEME)
        # Отображение формы
        self.show()
        # Определяем параметры приложения
        self.setupUi()
        # Устанавливаем названия виджетам
        self.setupText()
        # Устанавливаем имена некоторым переменным
        self.setupObjectName()
        # Компоненты для авторизации
        self.goAuthorizator()
        # Скрываем пароль
        self.goPasswordEchoMode()

    def setupUi(self):
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

    def setupText(self):
        """ Устанавливаем текст для виджетов """
        self.setWindowTitle(NW.APP.value)
        self.leLogin.setPlaceholderText(NW.PLACEHOLDER_LOGIN.value)
        self.lePassword.setPlaceholderText(NW.PLACEHOLDER_PASSWORD.value)
        self.leRepeatPassword.setPlaceholderText(NW.PLACEHOLDER_REPEAT_PASSWORD.value)
        self.pbOk.setText(NW.BUTTON_OK.value)
        self.pbClose.setText(NW.BUTTON_CLOSE.value)

    def setupObjectName(self):
        """ Задаём некоторым виджетам имена для css (theme.py) """
        self.lbLogin.setObjectName("lbLogin")
        self.pbCheck.setObjectName("pbCheck")
        self.pbVisible.setObjectName("pbVisible")
        self.lbNotification.setObjectName("lbNotification")

    def setFocusInLoginField(self):
        """ Установить фокус на поле с логином """
        self.leLogin.setFocus()

    def setFocusInPasswordField(self):
        """ Установить фокус на поле с паролем """
        self.lePassword.setFocus()

    def setFocusInRepeatPasswordField(self):
        """ Установить фокус на поле с паролем (повторно) """
        self.leRepeatPassword.setFocus()

    def goAuthorizator(self):
        """ Пройдите авторизацию """
        self.leRepeatPassword.setVisible(False)
        self.pbCheck.setText(NW.REGISTRATION.value)
        self.lbLogin.setText(NW.AUTHORIZATION.value)

    def goRegistration(self):
        """ Пройдите регистрацию """
        self.leRepeatPassword.setVisible(True)
        self.pbCheck.setText(NW.AUTHORIZATION.value)
        self.lbLogin.setText(NW.REGISTRATION.value)

    def gotoResetPasswordInField(self):
        """ Перейдите к сбросу пароля в поле ввода """
        self.lePassword.setText("")
        self.leRepeatPassword.setText("")

    def goNormalEchoMode(self):
        """ Перейти в нормальный режим в поле """
        self.lePassword.setEchoMode(QLineEdit.EchoMode.Normal)
        self.leRepeatPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        self.pbVisible.setIcon(QIcon("img/hidden.png"))
        self.pbVisible.setIconSize(QSize(HEIGHT_WIDGETS-10, HEIGHT_WIDGETS-10))

    def goPasswordEchoMode(self):
        """ Перейти в режим пароля в поле """
        self.lePassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.leRepeatPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.pbVisible.setIcon(QIcon("img/view.png"))
        self.pbVisible.setIconSize(QSize(HEIGHT_WIDGETS-10, HEIGHT_WIDGETS-10))

    def deleteAllWidgetsForRA(self):
        """ Удаление всех виджетов для регистрации и авторизации """
        # self.lbLogin.deleteLater()
        self.leLogin.deleteLater()
        self.lePassword.deleteLater()
        self.leRepeatPassword.deleteLater()
        self.pbCheck.deleteLater()
        self.pbVisible.deleteLater()
        self.pbOk.deleteLater()
        self.pbClose.deleteLater()

    def createNewComp(self, _login):
        """ ... """
        self.lbLogin.setText(f"Добро пожаловать, {_login}!")
        self.lbLogin.setWordWrap(True)
        # self.pbClose.setText("qwe")
