import datetime as dt
import os
import sqlite3

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QImage, QFont, QTextDocument, QTextCharFormat
from PyQt5.QtWidgets import QTextEdit

if os.getcwd().split('\\')[-1] != 'data':
    from data.utils import DateFunctions
else:
    from utils import DateFunctions


class BaseField(DateFunctions):  # Основной класс, от которого наследуются классы заметок и задач
    def __init__(self, db_name: str, text: QTextEdit, obj_id: int,
                 title: str, body: str, user_id: int, date: str):
        self.db_name = db_name  # Переменная названия БД
        self.text = text  # Переменная, содержащая в себе ссылку на поле для ввода текста
        self.obj_id = obj_id  # Переменная, отвечающая за ID объекта в его таблице
        self.title = title  # Переменная названия объекта
        self.body = body  # Переменная HTML, содержащегося в теле заметки
        self.user_id = user_id  # Переменная ID пользователя
        self.date = date  # Переменная даты создания в виде строки

        self.field_opened = False  # Отвечает за скрытие поля для ввода текста

        self.cursor = QTextEdit.textCursor(text)  # Курсор поля для ввода текста
        self.fmt = QTextCharFormat()  # Действующий формат последнего знака в тексте
        self.orig_font = QFont('Consolas', 12)  # Шрифт по умолчанию, используется при откате изменений
        self.font = QFont('Consolas', 12)  # Действующий шрифт

    def change_font(self, font: QFont) -> None:  # Изменяет действующий шрифт
        self.font = font
        cursor = self.text.textCursor()
        self.commit(cursor)

    def set_text_field(self, text_field) -> None:  # Изменяет действующее поле для ввода текста
        self.text = text_field

    def set_format(self, fmt: QTextCharFormat) -> None:  # Изменяет действующее форматирование знаков
        self.fmt = fmt

    def is_opened(self) -> bool:  # Возвращает статус того, открыто ли поля для ввода текста на действующий момент
        return self.field_opened

    def change_open(self, change: bool) -> None:  # Изменяет статус того, показывать ли поле для ввода текста
        self.field_opened = change

    def show(self) -> None:  # Наполняет действующее поле для текста HTML-данными
        self.text.setHtml(self.body)

    def delete(self):  # Самоуничтожение
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('DELETE FROM %s WHERE id = ?' % self.table, (self.obj_id,))
            con.commit()

    def save(self) -> None:  # Сохраняет изменения в объекте в БД
        html = self.text.toHtml()
        self.body = html
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('UPDATE %s SET body = ? WHERE id = ?' % self.table,
                        (html, self.obj_id))
            con.commit()

    def edit_title(self, title: str) -> None:  # Изменяет название объекта
        self.title = title
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('UPDATE %s SET title = ? WHERE id = ?' % self.table,
                        (title, self.obj_id))
            con.commit()
        self.text.show()

    def insert_picture(self, filename: str) -> None:  # Вставляет изображение в поле для ввода текста
        image = QImage(filename)
        img_height = image.height()
        image = image.scaled(760, img_height, Qt.KeepAspectRatio)
        filename = 'data/img/%s' % filename.split('/')[-1]
        image.save(filename)
        url = QUrl(filename)
        text_document = self.text.document()
        text_document.addResource(QTextDocument.ImageResource, url, image)
        self.cursor.insertImage(filename)

    def get_title(self) -> str:  # Возвращает название объекта
        return self.title

    def get_date_str(self) -> str:  # Возвращает дату создания в виде строки
        return self.date

    def get_date_dt(self) -> dt.date:  # Возвращает дату без времени в виде объекта datetime
        full_date = self.convert_str_to_dt(self.date)
        return dt.date(full_date.year, full_date.month, full_date.day)

    def commit(self, cursor) -> None:  # Применяет изменения в форматировании
        self.fmt.setFont(self.font)
        self.cursor = cursor
        self.cursor.mergeCharFormat(self.fmt)
        self.cursor.setCharFormat(self.fmt)
        self.text.setTextCursor(self.cursor)

    def align_right(self):  # Выравнивает по правому краю
        self.text.setAlignment(Qt.AlignRight)

    def align_center(self):  # Выравнивает по центру
        self.text.setAlignment(Qt.AlignCenter)

    def align_left(self):  # Выравнивает по левому краю
        self.text.setAlignment(Qt.AlignLeft)

    def make_italic(self) -> None:  # Делает текущее форматирование курсивом
        self.font.setItalic(True)
        cursor = self.text.textCursor()
        if cursor.charFormat().font().italic():
            self.font.setItalic(False)
        self.commit(cursor)

    def is_italic(self) -> bool:  # Возвращает статус того, имеется ли в форматировании курсив
        return self.text.textCursor().charFormat().font().italic()

    def make_overline(self) -> None:  # Добавляет к текущему форматированию линию сверху
        self.font.setOverline(True)
        cursor = self.text.textCursor()
        if cursor.charFormat().font().overline():
            self.font.setOverline(False)
        self.commit(cursor)

    def is_overlined(self) -> bool:  # Возвращает статус того, имеется ли в форматировании линия сверху
        return self.text.textCursor().charFormat().font().overline()

    def make_underline(self) -> None:  # Добавляет к текущему форматированию нижнее подчеркивание
        self.font.setUnderline(True)
        cursor = self.text.textCursor()
        if cursor.charFormat().font().underline():
            self.font.setUnderline(False)
        self.commit(cursor)

    def is_underlined(self) -> bool:  # Возвращает статус того, имеется ли в форматировании нижнее подчеркивание
        return self.text.textCursor().charFormat().font().underline()

    def make_strike_out(self) -> None:  # Добавляет к текущему форматированию зачеркивание
        self.font.setStrikeOut(True)
        cursor = self.text.textCursor()
        if cursor.charFormat().font().strikeOut():
            self.font.setStrikeOut(False)
        self.commit(cursor)

    def is_striked_out(self) -> bool:  # Возвращает статус того, имеется ли в форматировании зачеркивание
        return self.text.textCursor().charFormat().font().strikeOut()

    def make_bold(self) -> None:  # Делает текущее форматирование полужирным
        self.font.setBold(True)
        cursor = self.text.textCursor()
        if cursor.charFormat().font().bold():
            self.font.setBold(False)
        self.commit(cursor)

    def is_bold(self) -> bool:  # Возвращает статус того, является ли форматирование полужирным
        return self.text.textCursor().charFormat().font().bold()

    def make_regular(self) -> None:  # Сбрасывает форматирование
        cursor = self.text.textCursor()
        self.fmt.setFont(self.orig_font)
        self.font.setItalic(False)
        self.font.setStrikeOut(False)
        self.font.setBold(False)
        self.font.setUnderline(False)
        self.font.setOverline(False)
        self.commit(cursor)
