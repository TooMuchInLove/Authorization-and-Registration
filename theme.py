# -*- coding: utf-8 -*-

from config import FontFamily as FF
from config import FontSize as FS
from config import Pallete as PL


# Светлая тема приложения
LIGHT_THEME = f"""
QWidget {{\n
    font-family: {FF.VERDANA.value};\n
    font-size: {FS.SIZE_15.value}px;\n
    background: {PL.WHITE.value};\n
    color: {PL.DARK_BLUE.value};\n
    margin: 0 {FS.SIZE_20.value}px;\n
}}\n

QPushButton {{\n
    background: {PL.DARK_BLUE.value};\n
    color: {PL.WHITE.value};\n
}}\n

QPushButton:hover {{\n
    background: {PL.LIGHT_BLUE.value};\n
}}\n

QPushButton#pbCheck, QPushButton#pbVisible {{\n
    background: none;\n
}}\n

QPushButton#pbCheck {{\n
    color: {PL.ORANGE.value};\n
    text-decoration: underline;
}}\n

QLabel, QPushButton {{\n
    padding: 0 {FS.SIZE_5.value}px;\n
}}\n

QLabel#lbLogin {{\n
    font-weight: bold;\n
    font-size: {FS.SIZE_30.value}px;\n
}}\n

QPushButton, QLineEdit, QLabel#lbNotification {{\n
    border-radius: {FS.SIZE_5.value}px;\n
}}\n

QLineEdit {{\n
    border: {FS.SIZE_1.value}px solid {PL.LIGHT_GREY.value};\n
    padding: 0 {FS.SIZE_20.value}px;\n
    margin: 0 {FS.SIZE_40.value}px 0 {FS.SIZE_20.value}px;\n
}}\n

QLineEdit:focus {{\n
    border-color: {PL.ORANGE.value};\n
}}\n
"""

# Стиль всплывающей ошибки
STYLE_ERROR = f"""
background: {PL.WHITE.value};\n
color: {PL.DARK_RED.value};\n
border: {FS.SIZE_1.value}px solid {PL.DARK_RED.value};\n
"""

# Стиль всплывающего уведомления
STYLE_NOTIFICATION = f"""
background: {PL.DARK_BLUE.value};\n
color: {PL.WHITE.value};\n
border: {FS.SIZE_1.value}px solid {PL.WHITE.value};\n
"""
