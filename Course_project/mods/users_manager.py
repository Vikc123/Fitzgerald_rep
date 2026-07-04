from mods.models import UserRecord
from mods.array_storage import ArrayStorage
from mods.hash_table import HashTable


class UsersManager:
    def __init__(self, initial_capacity=17):
        self.storage = ArrayStorage()
        self.hash_table = HashTable(capacity=initial_capacity)
        self.id_index = HashTable(capacity=17)

    def add_user(self, user_id, email, subscription):
        user = UserRecord.create(user_id, email, subscription)

        if self.find_by_id(user.user_id)[0] is not None:
            raise ValueError(f"Пользователь с ID {user.user_id} уже существует")

        if self.find_by_email(user.email)[0] is not None:
            raise ValueError(f"Пользователь с email '{user.email}' уже существует")

        self.storage.add(user)
        self.hash_table.insert(user.email, user)
        self.id_index.insert(user.user_id, user)

        return user

    def find_by_email(self, email):
        records, steps = self.hash_table.search(email)

        for user in records:
            return user, steps

        return None, steps

    def find_by_id(self, user_id):
        records, steps = self.id_index.search(user_id)

        for user in records:
            return user, steps

        return None, steps

    def delete_user(self, email):
        user, steps = self.find_by_email(email)

        if user is None:
            return False, steps

        deleted_from_hash, _ = self.hash_table.delete_record(email, user)

        if not deleted_from_hash:
            return False, steps

        self.id_index.delete_record(user.user_id, user)

        deleted_from_storage = self.storage.remove(user)

        return deleted_from_storage, steps

    def get_all_users(self):
        return self.storage.get_active_items()

    def debug_hash_table(self):
        return self.hash_table.debug_print()

    def clear(self):
        self.storage.clear()
        self.hash_table.clear()
        self.id_index.clear()

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