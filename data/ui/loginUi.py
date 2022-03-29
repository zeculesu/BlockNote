from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class UiLoginForm:
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 400)
        font = QFont()
        font.setPointSize(9)
        Form.setFont(font)
        Form.setStyleSheet('background-color:"#ffe5b4"')
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QRect(80, 110, 160, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.login_field = QLineEdit(self.verticalLayoutWidget)
        self.login_field.setStyleSheet('background-color: "#fcfaed"; color:"#000000";border: 1px solid;'
                                       'border-radius: 3px;')
        self.login_field.setFont(QFont('Segoe UI Historic', 9))
        self.login_field.setObjectName("login_field")
        self.verticalLayout_2.addWidget(self.login_field)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.password_field = QLineEdit(self.verticalLayoutWidget)
        self.password_field.setObjectName("password_field")
        self.password_field.setStyleSheet('background-color: "#fcfaed"; color:"#000000";border: 1px solid;'
                                          'border-radius: 3px;')
        self.password_field.setEchoMode(QLineEdit.Password)
        self.verticalLayout_3.addWidget(self.password_field)
        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet('background-color: "#ffb399"; color:"#000000";border: 1px solid;'
                                      'border-radius: 3px;')
        self.pushButton.setFont(QFont('Segoe UI Historic', 9))
        self.verticalLayout_3.addWidget(self.pushButton)
        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet('background-color: "#ffb399"; color:"#000000";border: 1px solid;'
                                        'border-radius: 3px;')
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Авторизация"))
        self.label.setText(_translate("Form", '<h4 style="color: #000000;">Имя пользователя</h4>'))
        self.label_2.setText(_translate("Form", '<h4 style="color: #000000;">Пароль</h4>'))
        self.pushButton.setText(_translate("Form", "Войти"))
        self.pushButton_2.setText(_translate("Form", "Зарегистрироваться"))
