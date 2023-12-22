import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton
from random import randint

class kubiki(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Кубики')
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.dice_count_input = QLineEdit()
        self.summa_input = QLineEdit()
        self.result_label = QLabel()
        count_button = QPushButton("Посчитать вероятность")
        count_button.clicked.connect(self.calculatePercentages)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Число кубиков:"))
        layout.addWidget(self.dice_count_input)
        layout.addWidget(count_button)
        layout.addWidget(self.result_label)
        central_widget.setLayout(layout)

    def calculatePercentages(self):
        result = {}
        lst = []
        summa = 0
        procent = 0
        dice_count = int(self.dice_count_input.text())

        for _ in range(0, 1000000):
            dice_num = 0
            summa = 0
            for j in range(dice_count):
                dice_num = randint(1, 6)
                summa = summa + dice_num
            lst.append(summa)

        for i in range(dice_count, (dice_count * 6) + 1):
            procent = (lst.count(i)) / 10**6 * 100
            result[i] = procent
        self.result_label.setText(str(result))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = kubiki()
    window.show()
    sys.exit(app.exec())