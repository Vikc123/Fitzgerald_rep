from mods.models import UserRecord
from mods.array_storage import ArrayStorage
from mods.red_black_tree import RedBlackTree


class UsersManager:
    def __init__(self):
        self.storage = ArrayStorage()
        self.tree = RedBlackTree()

    def add_user(self, user_id, email, subscription):
        if self.find_by_email(email)[0] is not None:
            raise ValueError(f"Пользователь с email '{email}' уже существует")

        user = UserRecord(user_id, email, subscription)

        self.storage.add(user)
        self.tree.insert(email, user)

        return user

    def find_by_email(self, email):
        records, steps = self.tree.search(email)

        for user in records:
            return user, steps

        return None, steps

    def delete_user(self, email):
        user, steps = self.find_by_email(email)

        if user is None:
            return False, steps

        deleted_from_tree = self.tree.delete_record(email, user)

        if not deleted_from_tree:
            return False, steps

        deleted_from_storage = self.storage.remove(user)

        return deleted_from_storage, steps

    def get_all_users(self):
        return self.storage.get_active_items()

    def debug_tree(self):
        return self.tree.debug_print()

    def clear(self):
        self.storage.clear()
        self.tree.clear()

    def load_from_file(self, filename):
        self.clear()

        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    user = UserRecord.from_line(line)
                    self.add_user(user.user_id, user.email, user.subscription)
                except ValueError as error:
                    print(f"Ошибка в строке {line_number}: {error}")

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            for user in self.get_all_users():
                file.write(user.to_line() + "\n")