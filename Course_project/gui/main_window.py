from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)

from gui.views_panel import ViewsPanel
from gui.users_panel import UsersPanel
from gui.report_dialog import ReportDialog
from mods.models import ViewDate


class MainWindow(QMainWindow):
    def __init__(self, service):
        super().__init__()

        self.service = service

        self.setWindowTitle("Онлайн-кинотеатр")
        self.resize(1400, 600)

        self.views_panel = ViewsPanel(service)
        self.users_panel = UsersPanel(service)

        central_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.views_panel)
        layout.addWidget(self.users_panel)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self._create_menu()

    def _create_menu(self):
        menu_bar = self.menuBar()

        views_menu = menu_bar.addMenu("Просмотры")
        views_menu.addAction("Загрузить", self.views_panel.load_views)
        views_menu.addAction("Сохранить", self.views_panel.save_views)
        views_menu.addAction("Добавить", self.views_panel.add_view)
        views_menu.addAction("Удалить", self.views_panel.delete_view)
        views_menu.addAction("Найти по дате выпуска", self.views_panel.search_views)
        views_menu.addAction("Показать все", self.views_panel.refresh_table)
        views_menu.addAction("Печать КЧД", self.views_panel.show_tree)

        users_menu = menu_bar.addMenu("Пользователи")
        users_menu.addAction("Загрузить", self.users_panel.load_users)
        users_menu.addAction("Сохранить", self.users_panel.save_users)
        users_menu.addAction("Добавить", self.users_panel.add_user)
        users_menu.addAction("Удалить", self.users_panel.delete_user)
        users_menu.addAction("Найти", self.users_panel.search_user)
        users_menu.addAction("Показать все", self.users_panel.refresh_table)
        users_menu.addAction("Печать ХТ", self.users_panel.show_hash_table)

        report_menu = menu_bar.addMenu("Отчёт")
        report_menu.addAction("Сформировать отчёт", self.show_report)

    def show_report(self):
        dialog = ReportDialog(self)

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        email, release_day, release_month, release_year, status = dialog.get_data()

        try:
            release_date = ViewDate.create(release_day, release_month, release_year)
        except ValueError as error:
            QMessageBox.warning(self, "Ошибка", str(error))
            return

        rows, steps = self.service.build_report(email, release_date, status)

        self._show_report_result(rows, steps)

    def _show_report_result(self, rows, steps):
        window = QMainWindow(self)
        window.setWindowTitle(f"Отчёт (найдено: {len(rows)}, шагов поиска: {steps})")
        window.resize(1000, 400)

        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "ID (Пользователь)",
            "Email",
            "Подписка",
            "ID (Просмотр)",
            "Фильм",
            "Дата выпуска",
            "Статус"
        ])

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        table.setRowCount(len(rows))

        for row, values in enumerate(rows):
            for col, value in enumerate(values):
                table.setItem(row, col, QTableWidgetItem(str(value)))

        window.setCentralWidget(table)
        window.show()

        self.report_window = window

        if not rows:
            QMessageBox.information(self, "Отчёт", "По заданным условиям ничего не найдено")
