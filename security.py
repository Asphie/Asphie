import sys
import sqlite3 as sq
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QRadioButton, QMessageBox
from PyQt6.QtCore import QTimer
from datetime import datetime
import pandas as pd

with sq.connect("employees.db") as db:
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS employees(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        id_number INTEGER,
        e_firstname TEXT,
        e_name TEXT,
        e_lastname TEXT,
        enter DATETIME,
        exit DATETIME
        );
        """)
    db.commit()

with sq.connect("guests.db") as db2:
    sql2 = db2.cursor()
    sql2.execute("""CREATE TABLE IF NOT EXISTS guests(
        firstname TEXT,
        name TEXT,
        lastname TEXT,
        duration TEXT,
        enter DATETIME,
        exit DATETIME
        );
        """)
    db2.commit()

class PassControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.employees = pd.read_excel('employees.xlsx')

        global sql
        global db

    def initUI(self):


        self.button_enter = QPushButton('Выдать пропуск')
        self.button_enter.clicked.connect(self.ENTER)

        self.button_exit = QPushButton('Выход')
        self.button_exit.clicked.connect(self.EXIT)

        self.button_guest = QPushButton('Меню гостя')
        self.button_guest.clicked.connect(self.GST_ENTRY)

        self.emp_id_label = QLabel('id')
        self.ID = QLineEdit()

        self.emp_first_label = QLabel('Фамилия')
        self.firstname = QLineEdit()

        self.emp_name_label = QLabel('Имя')
        self.name = QLineEdit()

        self.emp_last_label = QLabel('Отчество')
        self.lastname = QLineEdit()
        self.RadioButton = QRadioButton('Вам нужна парковка?')

        layout = QVBoxLayout()
        layout.addWidget((self.emp_id_label))
        layout.addWidget(self.ID)
        layout.addWidget((self.emp_first_label))
        layout.addWidget(self.firstname)
        layout.addWidget((self.emp_name_label))
        layout.addWidget(self.name)
        layout.addWidget((self.emp_last_label))
        layout.addWidget(self.lastname)

        layout.addWidget(self.button_enter)
        layout.addWidget(self.button_exit)
        layout.addWidget(self.button_guest)
        layout.addWidget(self.RadioButton)


        self.setLayout(layout)
        self.setWindowTitle('Терминал Охраны')

    def parking_e(self):
        self.e_park = 2
        self.g_park = 1
        self.const = self.g_park+self.e_park

        if self.button_enter.clicked.connect() and const > 0:
            self.do_park('есть свободное парковочное место')
            const -= 1
        else:
            self.do_not_park('парковочные места заняты')
        if self.exit.button.clicked.connect():
            const += 1
        

    def do_not_park(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setText(message)
        error_box.setWindowTitle('Парковка')
        error_box.exec()

    def do_park(self, message):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setText(message)
        message_box.setWindowTitle('Парковка')
        message_box.exec()

    def show_deny(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setText(message)
        error_box.setWindowTitle('Ошибка')
        error_box.exec()

    def show_acces(self, message):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setText(message)
        message_box.setWindowTitle('Выполнение')
        message_box.exec()

    def GST_ENTRY(self):
        pass1.show()

    def ENTER(self):
        if self.RadioButton.toggle:
            self.parking_e
        else:
            pass
        e_id = self.ID.text()
        e_firstname = self.firstname.text()
        e_name = self.name.text()
        e_lastname = self.lastname.text()

        if not e_id or not e_firstname or not e_name or not e_lastname:
            self.show_deny('Все поля должны быть заполнены.')
            return
        if not self.employees['Фамилия'].str.strip().str.lower().eq(e_firstname.lower()).any() and not \
            self.employees['Имя'].str.strip().str.lower().eq(e_name.lower()).any() and not \
            self.employees['Отчество'].str.strip().str.lower().eq(e_lastname.lower()).any():
            self.show_deny('Вас нет в базе данных')
            return
        if not e_id.isdigit():
            self.show_deny('Неподходящие символы - пропуск должен содержать только цифры')

        if len(e_id) > 10:
            self.show_deny('Cлишком длинный номер пропуска')
            return
        if not all(map(str.isalpha, [e_firstname, e_name, e_lastname])):
            self.show_deny('Персональные данные пользователя должны содержать только буквы')
            return
        

        enter_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql.execute('INSERT INTO employees (id_number, e_firstname, e_name, e_lastname, enter) VALUES (?, ?, ?, ? ,  ?)',
                    (e_id, e_firstname, e_name, e_lastname, enter_time))
        db.commit()

        self.show_acces(' Вход успешно зарегистрирован.')

    def EXIT(self):
        if self.RadioButton.toggle:
            self.parking_e
        else:
            pass
        e_id = self.ID.text()
        e_firstname = self.firstname.text()
        e_name = self.name.text()
        e_lastname = self.lastname.text()

        if not e_id.isdigit():
            self.show_acces('Неподходящие символы - пропуск должен содержать только цифры')
            return
        if len(e_id) > 10:
            self.show_deny('Слишком длинный номер пропуска')
            return
        if not all(map(str.isalpha, [e_firstname,e_name, e_lastname])):
            self.show_deny('Персональные данные пользователя должны содержать только буквы')
            return
        if not e_id or not e_firstname or not e_name or not e_lastname:
            self.show_deny('Все поля должны быть заполнены.')
            return
        exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql.execute('UPDATE employees SET exit = ? WHERE id_number = ? AND exit IS NULL',
                    (exit_time, e_id))
        db.commit()

        self.show_acces('Выход успешно зарегистрирован.')

class gst_term(QWidget):
    def __init__(self):

        super().__init__()
        global sql2
        global db2
        

        self.guest_first_label = QLabel('Фамилия')
        self.firstname = QLineEdit()

        self.guest_name_label = QLabel('Имя')
        self.name = QLineEdit()

        self.guest_last_label = QLabel('Отчество')
        self.lastname = QLineEdit()

        self.guest_time_label = QLabel('Время пребывания')
        self.duration = QLineEdit()

        self.RadioButton_guest = QRadioButton('Вам нужна Парковка')

        layout = QVBoxLayout()

        self.issue_pass_button2 = QPushButton('Выход')
        self.issue_pass_button = QPushButton('Вход')
        self.guest_timer = QTimer(self)

        self.issue_pass_button.clicked.connect(self.gostevoy_vxod)
        self.issue_pass_button2.clicked.connect(self.gostevoy_vblxod)

        layout.addWidget(self.guest_first_label)
        layout.addWidget(self.firstname)

        layout.addWidget(self.guest_name_label)
        layout.addWidget(self.name)

        layout.addWidget(self.guest_last_label)
        layout.addWidget(self.lastname)

        layout.addWidget(self.guest_time_label)
        layout.addWidget(self.duration)
        layout.addWidget(self.issue_pass_button)
        layout.addWidget(self.issue_pass_button2)
        layout.addWidget(self.RadioButton_guest)


        self.setLayout(layout)
        self.setWindowTitle('Гостевой Терминал')

    def parking_g(self):
        self.g_park = 1
        self.const = self.g_park

        if self.button_enter.clicked.connect() and const > 0:
            self.do_park('есть свободное парковочное место')
            const -= 1
        else:
            self.do_not_park('парковочные места заняты')
        if self.exit.button.clicked.connect():
            const += 1
        

    def do_not_park(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setText(message)
        error_box.setWindowTitle('Парковка')
        error_box.exec()

    def do_park(self, message):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setText(message)
        message_box.setWindowTitle('Парковка')
        message_box.exec()

    def show_deny(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setText(message)
        error_box.setWindowTitle('Ошибка')
        error_box.exec()

    def show_acces(self, message):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setText(message)
        message_box.setWindowTitle('Успех')
        message_box.exec()

    def gostevoy_vxod(self):
        if self.RadioButton_guest.toggle:
            self.parking_g
        else:
            pass
        ent_time = datetime.now()
        g_firstname = self.firstname.text()
        g_name = self.name.text()
        g_lastname = self.lastname.text()
        dur = int(self.duration.text())

        if not all(map(str.isalpha, [g_name, g_firstname, g_lastname])):
            self.show_deny('Имя и фамилия должны содержать только буквы.')
            return
        if not g_firstname or not g_name or not g_lastname or not dur:
            self.show_deny('Все поля должны быть заполнены.')
            return

        ent_time = datetime.now()
        sql2.execute(
            'INSERT INTO guests (firstname, name, lastname, duration, enter) VALUES (?, ?, ?, ?, ?)',
            (g_firstname, g_name, g_lastname, dur, ent_time))
        db2.commit()

        self.show_acces('Гостевой вход успешно зарегистрирован.')
        self.guest_timer.start(1000 * 60 * dur)

    def gostevoy_vblxod(self):
        if self.RadioButton_guest.toggle:
            self.parking_g
        else:
            pass
        ext_time = datetime.now()
        g_firstname = self.firstname.text()
        g_name = self.name.text()
        g_lastname = self.lastname.text()
        dur = int(self.duration.text())

        if not all(map(str.isalpha, [g_name, g_firstname, g_lastname])):
            self.show_deny('Имя и фамилия должны содержать только буквы.')
            return
        if not g_firstname or not g_name or not g_lastname or not dur:
            self.show_deny('Все поля должны быть заполнены.')
            return
        ext_time = datetime.now()
        sql2.execute('UPDATE guests SET exit = ? WHERE firstname = ? AND name = ? AND lastname = ? AND duration = ? AND exit IS NULL',
         (ext_time,g_firstname,g_name, g_lastname, dur))
        db2.commit()

        self.show_acces('Гостевой выход успешно зарегистрирован.')
        self.guest_timer.stop


def time_control(self):
    current_time = datetime.now()
    sql2.execute(
        'SELECT * FROM guests WHERE exit IS NULL AND strftime("%s", ?) > strftime("%s", enter) + duration',
        (current_time,))
    dummy = sql2.fetchall()

    if dummy:
        message = 'ЩА МЕНТОВ ВЫЗОВУ!.'
        self.show_error(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pass_control = PassControlApp()
    pass1 = gst_term()
    pass_control.show()
    sys.exit(app.exec())