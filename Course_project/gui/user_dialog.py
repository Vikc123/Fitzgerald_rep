from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QPushButton, QHBoxLayout
)


class UserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавление пользователя")
        self.resize(350, 150)

        self.id_input = QSpinBox()
        self.id_input.setMinimum(1)
        self.id_input.setMaximum(999999)

        self.email_input = QLineEdit()
        self.subscription_input = QLineEdit()

        form = QFormLayout()
        form.addRow("ID пользователя:", self.id_input)
        form.addRow("Email:", self.email_input)
        form.addRow("Вид подписки:", self.subscription_input)

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
            self.id_input.value(),
            self.email_input.text(),
            self.subscription_input.text()
        )