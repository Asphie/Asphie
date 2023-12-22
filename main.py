import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class count_app(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Угадай число')
        self.setGeometry(200,200,200,200)

        self.rng_num = random.randint(1, 100)
        self.attempts = 8

        layout = QVBoxLayout()

        self.label = QLabel('Угадай число 1 до 100:')
        layout.addWidget(self.label)

        self.input = QLineEdit()
        layout.addWidget(self.input)

        self.button = QPushButton('Ввести')
        self.button.clicked.connect(self.gss)
        layout.addWidget(self.button)

        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def gss(self):
        guess = int(self.input.text())
        if guess < self.rng_num:
            self.result_label.setText('Загаданное число больше')
        elif guess > self.rng_num:
            self.result_label.setText('Загаданное число меньше')
        else:
            self.result_label.setText('Вы угадали!')
        self.attempts -= 1
        if self.attempts == 0:
            self.result_label.setText('Вы проиграли. Было загадано число: ' + str(self.rng_num))
            self.button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = count_app()
    window.show()
    sys.exit(app.exec())
