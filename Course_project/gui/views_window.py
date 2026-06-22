from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QToolBar, QMessageBox, QInputDialog,
    QTextEdit, QFileDialog, QHeaderView, QAbstractItemView
)

from gui.view_dialog import ViewDialog

class ViewsWindow(QMainWindow):
    def __init__(self, service):
        super().__init__()

        self.service = service

        self.setWindowTitle("Справочник просмотров")
        self.resize(900, 500)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID пользователя",
            "Фильм",
            "Год выпуска",
            "Статус"
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
        action_search = toolbar.addAction("Найти по году")
        action_show_all = toolbar.addAction("Показать все")
        action_debug = toolbar.addAction("Печать ХТ")

        action_load.triggered.connect(self.load_views)
        action_save.triggered.connect(self.save_views)
        action_add.triggered.connect(self.add_view)
        action_delete.triggered.connect(self.delete_view)
        action_search.triggered.connect(self.search_views)
        action_show_all.triggered.connect(self.refresh_table)
        action_debug.triggered.connect(self.show_hash_table)

    def refresh_table(self):
        data = self.service.get_views_table()

        self.table.setRowCount(len(data))

        for row, view in enumerate(data):
            for col, value in enumerate(view):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.statusBar().showMessage(f"Записей: {len(data)}")

    def load_views(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Загрузить просмотры",
            "",
            "Text files (*.txt);;All files (*.*)"
        )

        if not filename:
            return

        try:
            self.service.load_views_from_file(filename)
            self.refresh_table()
            QMessageBox.information(self, "Загрузка", "Просмотры загружены")
        except Exception as error:
            QMessageBox.warning(self, "Ошибка", str(error))

    def save_views(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить просмотры",
            "",
            "Text files (*.txt);;All files (*.*)"
        )

        if not filename:
            return

        try:
            self.service.save_views_to_file(filename)
            QMessageBox.information(self, "Сохранение", "Просмотры сохранены")
        except Exception as error:
            QMessageBox.warning(self, "Ошибка", str(error))

    def add_view(self):
        dialog = ViewDialog(self)

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        user_id, film, year, status = dialog.get_data()

        try:
            self.service.add_view(user_id, film, year, status)
            self.refresh_table()
        except ValueError as error:
            QMessageBox.warning(self, "Ошибка", str(error))

    def delete_view(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите просмотр в таблице")
            return

        user_id = int(self.table.item(row, 0).text())
        film = self.table.item(row, 1).text()
        year = int(self.table.item(row, 2).text())
        status = self.table.item(row, 3).text()

        deleted, steps = self.service.delete_view_by_fields(
            user_id,
            film,
            year,
            status
        )

        if deleted:
            QMessageBox.information(
                self,
                "Удаление",
                f"Просмотр удалён\nШагов поиска: {steps}"
            )
            self.refresh_table()
        else:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Просмотр не найден"
            )

    def search_views(self):
        year, ok = QInputDialog.getInt(
            self,
            "Поиск просмотров",
            "Введите год выпуска:"
        )

        if not ok:
            return

        data, steps = self.service.find_views_table_by_year(year)

        self.table.setRowCount(len(data))

        for row, view in enumerate(data):
            for col, value in enumerate(view):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.statusBar().showMessage(f"Найдено: {len(data)} | Шагов поиска: {steps}")

        QMessageBox.information(
            self,
            "Поиск",
            f"Найдено записей: {len(data)}\nШагов поиска: {steps}"
        )

    def show_hash_table(self):
        hash_text = self.service.debug_views_hash_table()

        window = QMainWindow(self)
        window.setWindowTitle("Отладка: хеш-таблица")
        window.resize(900, 500)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(hash_text)

        window.setCentralWidget(text_edit)
        window.show()

        self.debug_window = window