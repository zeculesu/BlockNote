import datetime as dt
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit

if os.getcwd().split('\\')[-1] != 'data':
    from data.exceptions import InvalidDateFormat
else:
    from exceptions import InvalidDateFormat


class DateFunctions:  # Класс, в который вынесены основные функции преобразования объектов datetime и str
    @staticmethod
    def convert_str_to_dt(raw_string: str) -> dt.datetime:  # Перевод строки в объект даты
        if len(raw_string.split('.')) == 3 and len(raw_string.split(':')) == 2:  # При вызове из добавления дедлайна
            day, month, year = map(int, raw_string.split()[0].split('.'))
            hours, minutes = map(int, raw_string.split()[1].split(':'))
        elif len(raw_string.split('.')) == 3 and len(raw_string.split(':')) == 3:  # При вызове из атрибутов заметок
            day, month, year = map(int, raw_string.split()[0].split('.'))
            hours, minutes, _ = map(int, raw_string.split()[1].split(':'))
        elif len(raw_string.split('-')) == 3 and len(raw_string.split(':')) == 3:  # При преобразования из БД
            year, month, day = map(int, raw_string.split()[0].split('-'))
            hours, minutes, _ = map(int, raw_string.split()[1].split(':'))
        else:
            raise InvalidDateFormat('Неверный формат дедлайна')
        return dt.datetime(year, month, day, hours, minutes)

    @staticmethod
    def convert_dt_to_str(date: dt.datetime) -> str:  # Перевод объекта даты в строку
        date = str(date)
        date = ('.'.join(date.split('.')[0].split()[0].split('-')[::-1])
                + ' ' + date.split()[-1].split('.')[0])
        return date


class FocusGradedText(QTextEdit):  # Переопределяемый класс QTextEdit, использующийся для автосохранения
    def __init__(self, parent: QMainWindow):
        super(FocusGradedText, self).__init__(parent)
        self.parent_wdg = parent  # Определение ссылки на виджета-родителя (MainWindow)

    def focusInEvent(self, _) -> None:
        self.setFocusPolicy(Qt.NoFocus)
        self.setEnabled(True)
        self.setCursorWidth(1)

    def focusOutEvent(self, _) -> None:
        self.parent_wdg.save_object()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCursorWidth(0)
