from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QPushButton, QHBoxLayout, QComboBox
)


class ViewDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавление просмотра")
        self.resize(400, 180)

        self.user_id_input = QSpinBox()
        self.user_id_input.setMinimum(1)
        self.user_id_input.setMaximum(999999)

        self.film_input = QLineEdit()

        self.year_input = QSpinBox()
        self.year_input.setMinimum(1900)
        self.year_input.setMaximum(2100)

        self.status_input = QComboBox()
        self.status_input.addItems([
            "Просмотрен",
            "В процессе",
            "Запланирован",
            "Брошен"
        ])

        form = QFormLayout()
        form.addRow("ID пользователя:", self.user_id_input)
        form.addRow("Фильм:", self.film_input)
        form.addRow("Год выпуска:", self.year_input)
        form.addRow("Статус:", self.status_input)

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Отмена")

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(buttons)

        self.setLayout(layout)

    def get_data(self):
        return (
            self.user_id_input.value(),
            self.film_input.text(),
            self.year_input.value(),
            self.status_input.currentText()
        )