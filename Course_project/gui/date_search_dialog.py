from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QSpinBox,
    QComboBox, QPushButton, QHBoxLayout
)

from mods.models import MIN_YEAR, MAX_YEAR, MONTH_NAMES_RU


class DateSearchDialog(QDialog):
    def __init__(self, parent=None, title="Поиск по дате выпуска"):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.resize(300, 150)

        self.day_input = QSpinBox()
        self.day_input.setMinimum(1)
        self.day_input.setMaximum(31)

        self.month_input = QComboBox()
        self.month_input.addItems(MONTH_NAMES_RU)

        self.year_input = QSpinBox()
        self.year_input.setMinimum(MIN_YEAR)
        self.year_input.setMaximum(MAX_YEAR)

        form = QFormLayout()
        form.addRow("День:", self.day_input)
        form.addRow("Месяц:", self.month_input)
        form.addRow("Год:", self.year_input)

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
            self.day_input.value(),
            self.month_input.currentIndex() + 1,
            self.year_input.value()
        )
