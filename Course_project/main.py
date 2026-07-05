import sys
from PyQt6.QtWidgets import QApplication

from mods.movie_service import MovieService
from mods.generator import generate_users, generate_views

from gui.main_window import MainWindow
from gui.capacity_dialog import CapacityDialog


def main():
    generate_users("data/users.txt", 10)
    generate_views("data/views.txt", users_count=10, views_count=10)

    app = QApplication(sys.argv)

    capacity_dialog = CapacityDialog()
    users_capacity = 17

    if capacity_dialog.exec() == capacity_dialog.DialogCode.Accepted:
        users_capacity = capacity_dialog.get_capacity()

    service = MovieService(users_capacity=users_capacity)
    service.load_users_from_file("data/users_e.txt")
    service.load_views_from_file("data/views_e.txt")

    window = MainWindow(service)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()