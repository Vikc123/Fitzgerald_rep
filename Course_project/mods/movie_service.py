from mods.users_manager import UsersManager
from mods.views_manager import ViewsManager
from mods.models import ViewRecord

class MovieService:
    def __init__(self):
        self.users = UsersManager()
        self.views = ViewsManager(initial_capacity=17)

    def add_user(self, user_id, email, subscription):
        existing_user = self.find_user_by_id(user_id)

        if existing_user is not None:
            raise ValueError(f"Пользователь с ID {user_id} уже существует")

        return self.users.add_user(user_id, email, subscription)

    def add_view(self, user_id, film, year, status):
        user = self.find_user_by_id(user_id)

        if user is None:
            raise ValueError(f"Нельзя добавить просмотр: пользователя с ID {user_id} нет")

        return self.views.add_view(user_id, film, year, status)

    def find_user_by_email(self, email):
        return self.users.find_by_email(email)

    def find_views_by_year(self, year):
        return self.views.find_by_year(year)

    def find_user_by_id(self, user_id):
        for user in self.users.get_all_users():
            if user.user_id == user_id:
                return user

        return None

    def has_views_for_user(self, user_id):
        for view in self.views.get_all_views():
            if view.user_id == user_id:
                return True

        return False

    def delete_user_by_email(self, email):
        user, steps = self.users.find_by_email(email)

        if user is None:
            return False, steps, "Пользователь не найден"

        if self.has_views_for_user(user.user_id):
            return False, steps, "Нельзя удалить пользователя: у него есть просмотры"

        deleted, _ = self.users.delete_user(email)

        if deleted:
            return True, steps, "Пользователь удалён"

        return False, steps, "Ошибка удаления"

    def delete_view(self, view):
        return self.views.delete_view(view)

    def debug_users_tree(self):
        return self.users.debug_tree()

    def debug_views_hash_table(self):
        return self.views.debug_hash_table()

    def load_users_from_file(self, filename):
        self.users.load_from_file(filename)

    def save_users_to_file(self, filename):
        self.users.save_to_file(filename)

    def load_views_from_file(self, filename):
        self.views.clear()

        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    view = ViewRecord.from_line(line)
                    self.add_view(
                        view.user_id,
                        view.film,
                        view.year,
                        view.status
                    )
                except ValueError as error:
                    print(f"Ошибка в строке {line_number}: {error}")

    def save_views_to_file(self, filename):
        self.views.save_to_file(filename)

    def get_users_table(self):
        result = []

        for user in self.users.get_all_users():
            result.append([
                user.user_id,
                user.email,
                user.subscription
            ])

        return result

    def get_views_table(self):
        result = []

        for view in self.views.get_all_views():
            result.append([
                view.user_id,
                view.film,
                view.year,
                view.status
            ])

        return result

    def delete_view_by_fields(self, user_id, film, year, status):
        for view in self.views.get_all_views():
            if (
                view.user_id == user_id and
                view.film == film and
                view.year == year and
                view.status == status
            ):
                return self.views.delete_view(view)

        return False, 0

    def find_views_table_by_year(self, year):
        records, steps = self.views.find_by_year(year)

        result = []

        for view in records:
            result.append([
                view.user_id,
                view.film,
                view.year,
                view.status
            ])

        return result, steps

    def find_user_table_by_email(self, email):
        user, steps = self.users.find_by_email(email)

        if user is None:
            return [], steps

        return [[
            user.user_id,
            user.email,
            user.subscription
        ]], steps