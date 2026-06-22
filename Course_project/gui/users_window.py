from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QToolBar, QMessageBox, QInputDialog,
    QTextEdit, QFileDialog, QHeaderView, QAbstractItemView
)
from gui.user_dialog import UserDialog

class UsersWindow(QMainWindow):
    def __init__(self, service):
        super().__init__()

        self.service = service

        self.setWindowTitle("Справочник пользователей")
        self.resize(900, 500)

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

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.create_toolbar()
        self.refresh_table()

    def create_toolbar(self):
        toolbar = QToolBar("ToolStrip")
        self.addToolBar(toolbar)

        action_load = toolbar.addAction("Загрузить")
        action_save = toolbar.addAction("Сохранить")
        action_add = toolbar.addAction("Добавить")
        action_delete = toolbar.addAction("Удалить")
        action_search = toolbar.addAction("Найти")
        action_show_all = toolbar.addAction("Показать все")
        action_debug = toolbar.addAction("Печать КЧД")

        action_load.triggered.connect(self.load_users)
        action_save.triggered.connect(self.save_users)
        action_add.triggered.connect(self.add_user)
        action_delete.triggered.connect(self.delete_user)
        action_search.triggered.connect(self.search_user)
        action_show_all.triggered.connect(self.refresh_table)
        action_debug.triggered.connect(self.show_tree)

    def refresh_table(self):
        data = self.service.get_users_table()

        self.table.setRowCount(len(data))

        for row, user in enumerate(data):
            for col, value in enumerate(user):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.statusBar().showMessage(f"Записей: {len(data)}")

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

        self.statusBar().showMessage(f"Найдено: {len(data)} | Шагов поиска: {steps}")

        QMessageBox.information(
            self,
            "Поиск",
            f"Найдено записей: {len(data)}\nШагов поиска: {steps}"
        )

    def show_tree(self):
        tree_text = self.service.debug_users_tree()

        window = QMainWindow(self)
        window.setWindowTitle("Отладка: красно-чёрное дерево")
        window.resize(800, 500)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(tree_text)

        window.setCentralWidget(text_edit)
        window.show()

        self.debug_window = window