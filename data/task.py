import datetime as dt
import os
import sqlite3
from typing import Union

from PyQt5.QtWidgets import QTextEdit

if os.getcwd().split('\\')[-1] != 'data':
    from data.baseField import BaseField
else:
    from baseField import BaseField


class Task(BaseField):  # Класс, отвечающий за инкапсуляцию данных о задачах
    def __init__(self, db_name: str, text: QTextEdit, task_id: int,
                 title: str, body: str, user_id: int, date: str, deadline: dt.datetime, closed: bool):
        super(Task, self).__init__(db_name, text, task_id, title, body, user_id, date)
        self.deadline = self.convert_str_to_dt(deadline)  # Объект даты дедлайна
        self.closed = closed  # Статус выполнения задачи
        self.table = 'tasks'  # Переменная, отвечающая за название таблицы в БД. Используется для полиморфизма

    def get_deadline_dt(self, with_time=True) -> Union[dt.date, dt.datetime]:  # Возвращает дедлайн в виде объекта даты
        return (self.deadline if with_time else dt.date(self.deadline.year,
                                                        self.deadline.month,
                                                        self.deadline.day))

    def get_deadline_str(self) -> str:  # Возвращает дедлайн в виде строки
        return self.convert_dt_to_str(self.deadline)

    def close(self) -> bool:  # Отмечает задачу выполненной
        if not self.is_expired():
            self.closed = True
            with sqlite3.connect(self.db_name) as con:
                cur = con.cursor()
                cur.execute('UPDATE tasks SET closed = True WHERE id = ?', (self.obj_id,))
                con.commit()
            return True
        return False

    def is_closed(self) -> bool:  # Возвращает статус выполнения задачи
        return self.closed

    def is_expired(self) -> bool:  # Возвращает статус выхода из дедлайна задачи
        return self.deadline < dt.datetime.now() and not self.is_closed()
