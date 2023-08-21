#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from sys import argv, exit
# Графический интерфейс
from PyQt5.QtWidgets import QApplication

# Графический интерфейс и логика приложения
from core.services import ServiceGlucose


def main():
    # Создание приложения
    app = QApplication(argv)
    # Пользовательский интерфейс и логика
    ui = ServiceGlucose()
    # Закрытие приложения по кнопке
    exit(app.exec_())


if __name__ == "__main__":
    main()
