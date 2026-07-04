from mods.users_manager import UsersManager
from mods.views_manager import ViewsManager
from mods.models import ViewRecord, ViewDate

class MovieService:
    def __init__(self, users_capacity=17):
        self.users = UsersManager(initial_capacity=users_capacity)
        self.views = ViewsManager()

    def add_user(self, user_id, email, subscription):
        return self.users.add_user(user_id, email, subscription)

    def add_view(self, user_id, film, status, release_day, release_month, release_year):
        user = self.find_user_by_id(user_id)

        if user is None:
            raise ValueError(f"Нельзя добавить просмотр: пользователя с ID {user_id} нет")

        release_date = ViewDate.create(release_day, release_month, release_year)

        return self.views.add_view(user_id, film, release_date, status)

    def find_user_by_email(self, email):
        return self.users.find_by_email(email)

    def find_views_by_date(self, release_date):
        return self.views.find_by_date(release_date)

    def find_user_by_id(self, user_id):
        user, steps = self.users.find_by_id(user_id)
        return user

    def has_views_for_user(self, user_id):
        return self.views.has_views_for_user(user_id)

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

    def debug_users_hash_table(self):
        return self.users.debug_hash_table()

    def debug_views_tree(self):
        return self.views.debug_tree()

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
                        view.status,
                        view.release_date.day,
                        view.release_date.month,
                        view.release_date.year
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

    def get_all_views(self):
        return self.views.get_all_views()

    def find_user_table_by_email(self, email):
        user, steps = self.users.find_by_email(email)

        if user is None:
            return [], steps

        return [[
            user.user_id,
            user.email,
            user.subscription
        ]], steps

    def build_report(self, email, release_date, status):
        user, user_steps = self.users.find_by_email(email)

        if user is None:
            return [], user_steps

        views, views_steps = self.views.find_by_user(user.user_id)
        steps = user_steps + views_steps

        result = []

        for view in views:
            if view.release_date == release_date and view.status == status:
                result.append([
                    user.user_id,
                    user.email,
                    user.subscription,
                    view.user_id,
                    view.film,
                    view.release_date.to_string(),
                    view.status
                ])

        return result, steps