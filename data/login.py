import os
import sqlite3

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget

if os.getcwd().split('\\')[-1] != 'data':
    from data.ui.loginUi import UiLoginForm
    from data.baseApplicationForm import BaseApplicationForm
else:
    from ui.loginUi import UiLoginForm
    from baseApplicationForm import BaseApplicationForm


class LoginForm(QWidget, UiLoginForm, BaseApplicationForm):
    def __init__(self, db_name, parent):
        super(LoginForm, self).__init__()
        self.setupUi(self)
        self.setFixedSize(320, 400)
        self.verticalLayout.setGeometry(QRect(82, 118, 164, 165))
        self.pushButton.clicked.connect(self.entry)
        self.pushButton_2.clicked.connect(self.registration)

        self.db_name = db_name  # Переменная названия БД
        self.parent = parent  # Ссылка на объект окна-родителя

        self.sequences = [  # Последовательности на клавиатуре
            'qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop',
            'asd', 'sdf', 'dfg', 'fgh', 'ghj', 'hjk', 'jkl',
            'zxc', 'xcv', 'cvb', 'vbn', 'bnm',
            'йцу', 'цук', 'уке', 'кен', 'енг', 'нгш', 'гшщ', 'шщз', 'щзх', 'зхъ',
            'фыв', 'ыва', 'вап', 'апр', 'про', 'рол', 'олд', 'лдж', 'джэ',
            'ячс', 'чсм', 'сми', 'мит', 'ить', 'тьб', 'ьбю', 'жэё'
        ]

    def get_data(self) -> tuple:  # Получить логин и пароль из полей для ввода
        return self.login_field.text(), self.password_field.text()

    # Проверяет, заполнены ли оба поля для ввода
    def check_fields(self, login: str, password: str, error_window_title: str):
        if not login or not password:
            self.show_message('Поля должны быть заполнены', error_window_title)
            return False
        return True

    def entry(self):  # Функция входа
        error_window_title = 'Ошибка авторизации'
        with sqlite3.connect(self.db_name) as con:
            login, password = self.get_data()
            if not self.check_fields(login, password, error_window_title):
                return
            cur = con.cursor()
            result = cur.execute('SELECT password FROM users WHERE login = ?', (login,)).fetchone()
            if not result:
                self.show_message('Такого логина не существует', error_window_title)
                return False
            elif password != result[0]:
                self.show_message('Неверный логин или пароль', error_window_title)
            else:
                self.parent.proceed(login)  # Переход к основному окну
                self.destroy()  # Самоуничтожение

    def registration(self):  # Функция регистрации
        error_window_title = 'Ошибка регистрации'
        login, password = self.get_data()
        if not self.check_fields(login, password, error_window_title):
            return
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            if cur.execute('SELECT id FROM users WHERE login = ?', (login,)).fetchone():
                self.show_message('Такой логин уже существует', error_window_title)
                return
            messages = []  # Далее - проверка на надёжность пароля
            if len(password) <= 8:
                messages.append('Слишком короткий пароль')
            if password.lower() == password or password.upper() == password:
                messages.append('Буквы должны быть разного регистра')
            if not any([i in password for i in list('0123456789')]):
                messages.append('В пароле должны присутствовать цифры')
            if any([i in password.lower() for i in self.sequences]):
                messages.append('Слишком простой')
            if messages:
                self.show_message('• ' + '\n• '.join(messages), error_window_title)
            else:
                cur.execute('INSERT INTO users (login, password) VALUES (?, ?)',
                            (login, password))
                con.commit()
                self.parent.proceed(login)  # -/-
                self.destroy()  # -/-
