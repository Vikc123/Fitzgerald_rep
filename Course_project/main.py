import sys
from PyQt6.QtWidgets import QApplication

from mods.movie_service import MovieService
from mods.generator import generate_users, generate_views

from gui.users_window import UsersWindow
from gui.views_window import ViewsWindow


def main():
    generate_users("data/users.txt", 15)
    generate_views("data/views.txt", users_count=15, views_count=30)

    service = MovieService()
    service.load_users_from_file("data/users.txt")
    service.load_views_from_file("data/views.txt")

    app = QApplication(sys.argv)

    users_window = UsersWindow(service)
    views_window = ViewsWindow(service)

    users_window.move(100, 100)
    views_window.move(1050, 100)

    users_window.show()
    views_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()