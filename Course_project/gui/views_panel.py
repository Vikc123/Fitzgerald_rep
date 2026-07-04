from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QMessageBox,
    QTextEdit, QFileDialog, QHeaderView, QAbstractItemView,
    QMainWindow
)

from gui.view_dialog import ViewDialog
from gui.date_search_dialog import DateSearchDialog
from mods.models import ViewDate

class ViewsPanel(QWidget):
    def __init__(self, service):
        super().__init__()

        self.service = service

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID пользователя",
            "Фильм",
            "Дата выпуска",
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

        self.status_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Просмотры (красно-чёрное дерево)"))
        layout.addWidget(self.table)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        self.refresh_table()

    def refresh_table(self):
        self.current_views = self.service.get_all_views()
        self._fill_table(self.current_views)

        self.status_label.setText(f"Записей: {len(self.current_views)}")

    def _fill_table(self, views):
        self.table.setRowCount(len(views))

        for row, view in enumerate(views):
            values = [
                view.user_id,
                view.film,
                view.release_date.to_string(),
                view.status
            ]

            for col, value in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

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

        user_id, film, status, release_day, release_month, release_year = dialog.get_data()

        try:
            self.service.add_view(
                user_id, film, status,
                release_day, release_month, release_year
            )
            self.refresh_table()
        except ValueError as error:
            QMessageBox.warning(self, "Ошибка", str(error))

    def delete_view(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите просмотр в таблице")
            return

        view = self.current_views[row]
        deleted, steps = self.service.delete_view(view)

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
        dialog = DateSearchDialog(self, title="Поиск просмотров по дате выпуска")

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        day, month, year = dialog.get_data()

        try:
            release_date = ViewDate.create(day, month, year)
        except ValueError as error:
            QMessageBox.warning(self, "Ошибка", str(error))
            return

        records, steps = self.service.find_views_by_date(release_date)
        self.current_views = list(records)
        self._fill_table(self.current_views)

        self.status_label.setText(f"Найдено: {len(self.current_views)} | Шагов поиска: {steps}")

        QMessageBox.information(
            self,
            "Поиск",
            f"Найдено записей: {len(self.current_views)}\nШагов поиска: {steps}"
        )

    def show_tree(self):
        tree_text = self.service.debug_views_tree()

        window = QMainWindow(self)
        window.setWindowTitle("Отладка: красно-чёрное дерево (просмотры)")
        window.resize(900, 500)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(tree_text)

        window.setCentralWidget(text_edit)
        window.show()

        self.debug_window = window
