import os

from PyQt5.QtWidgets import QTextEdit

if os.getcwd().split('\\')[-1] != 'data':
    from data.baseField import BaseField
else:
    from baseField import BaseField


class Note(BaseField):  # Класс, отвечающий за инкапсуляцию данных о заметках
    def __init__(self, db_name: str, text: QTextEdit, note_id: int,
                 title: str, body: str, user_id: int, date: str):
        super(Note, self).__init__(db_name, text, note_id, title, body, user_id, date)
        self.table = 'notes'  # Объявление переменной столбца в БД, обеспечивает полиморфизм с BaseField
