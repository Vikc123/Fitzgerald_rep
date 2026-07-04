from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QComboBox, QPushButton, QHBoxLayout
)

from mods.models import MIN_YEAR, MAX_YEAR, MONTH_NAMES_RU


class ReportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Формирование отчёта")
        self.resize(350, 220)

        self.email_input = QLineEdit()

        self.release_day_input = QSpinBox()
        self.release_day_input.setMinimum(1)
        self.release_day_input.setMaximum(31)

        self.release_month_input = QComboBox()
        self.release_month_input.addItems(MONTH_NAMES_RU)

        self.release_year_input = QSpinBox()
        self.release_year_input.setMinimum(MIN_YEAR)
        self.release_year_input.setMaximum(MAX_YEAR)

        self.status_input = QComboBox()
        self.status_input.addItems([
            "Просмотрен",
            "В процессе",
            "Запланирован",
            "Брошен"
        ])

        form = QFormLayout()
        form.addRow("Email пользователя:", self.email_input)
        form.addRow("День выпуска:", self.release_day_input)
        form.addRow("Месяц выпуска:", self.release_month_input)
        form.addRow("Год выпуска:", self.release_year_input)
        form.addRow("Статус:", self.status_input)

        ok_button = QPushButton("Сформировать")
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
            self.email_input.text(),
            self.release_day_input.value(),
            self.release_month_input.currentIndex() + 1,
            self.release_year_input.value(),
            self.status_input.currentText()
        )
