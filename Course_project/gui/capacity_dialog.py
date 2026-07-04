from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QSpinBox,
    QPushButton, QHBoxLayout
)


class CapacityDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Начальный размер хеш-таблицы")
        self.resize(320, 120)

        self.capacity_input = QSpinBox()
        self.capacity_input.setMinimum(5)
        self.capacity_input.setMaximum(1000)
        self.capacity_input.setValue(17)

        form = QFormLayout()
        form.addRow("Размер ХТ пользователей:", self.capacity_input)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)

        buttons = QHBoxLayout()
        buttons.addWidget(ok_button)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(buttons)

        self.setLayout(layout)

    def get_capacity(self):
        return self.capacity_input.value()
