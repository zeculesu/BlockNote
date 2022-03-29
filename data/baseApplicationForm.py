from PyQt5.QtWidgets import QMessageBox


class BaseApplicationForm:
    @staticmethod
    def show_message(error, window_title):
        msg = QMessageBox()
        msg.setStyleSheet('background-color:#4caf50')
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)
        msg.setWindowTitle(window_title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
