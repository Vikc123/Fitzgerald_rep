from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QMessageBox, QInputDialog,
    QTextEdit, QFileDialog, QHeaderView, QAbstractItemView,
    QMainWindow
)
from gui.user_dialog import UserDialog

class UsersPanel(QWidget):
    def __init__(self, service):
        super().__init__()

        self.service = service

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "ID пользователя",
            "Email",
            "Вид подписки"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.status_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Пользователи (хеш-таблица)"))
        layout.addWidget(self.table)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        self.refresh_table()

    def refresh_table(self):
        data = self.service.get_users_table()

        self.table.setRowCount(len(data))

        for row, user in enumerate(data):
            for col, value in enumerate(user):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.status_label.setText(f"Записей: {len(data)}")

    def load_users(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Загрузить пользователей",
            "",
            "Text files (*.txt);;All files (*.*)"
        )

        if not filename:
            return

        try:
            self.service.load_users_from_file(filename)
            self.refresh_table()
            QMessageBox.information(self, "Загрузка", "Пользователи загружены")
        except Exception as error:
            QMessageBox.warning(self, "Ошибка", str(error))

    def save_users(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить пользователей",
            "",
            "Text files (*.txt);;All files (*.*)"
        )

        if not filename:
            return

        try:
            self.service.save_users_to_file(filename)
            QMessageBox.information(self, "Сохранение", "Пользователи сохранены")
        except Exception as error:
            QMessageBox.warning(self, "Ошибка", str(error))

    def add_user(self):
        dialog = UserDialog(self)

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        user_id, email, subscription = dialog.get_data()

        try:
            self.service.add_user(user_id, email, subscription)
            self.refresh_table()
        except ValueError as error:
            QMessageBox.warning(self, "Ошибка", str(error))

    def delete_user(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя в таблице")
            return

        email = self.table.item(row, 1).text()

        deleted, steps, message = self.service.delete_user_by_email(email)

        QMessageBox.information(
            self,
            "Удаление",
            f"{message}\nШагов поиска: {steps}"
        )

        if deleted:
            self.refresh_table()

    def search_user(self):
        email, ok = QInputDialog.getText(
            self,
            "Поиск пользователя",
            "Введите Email:"
        )

        if not ok:
            return

        data, steps = self.service.find_user_table_by_email(email)

        self.table.setRowCount(len(data))

        for row, user in enumerate(data):
            for col, value in enumerate(user):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.status_label.setText(f"Найдено: {len(data)} | Шагов поиска: {steps}")

        QMessageBox.information(
            self,
            "Поиск",
            f"Найдено записей: {len(data)}\nШагов поиска: {steps}"
        )

    def show_hash_table(self):
        hash_text = self.service.debug_users_hash_table()

        window = QMainWindow(self)
        window.setWindowTitle("Отладка: хеш-таблица (пользователи)")
        window.resize(800, 500)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(hash_text)

        window.setCentralWidget(text_edit)
        window.show()

        self.debug_window = window
