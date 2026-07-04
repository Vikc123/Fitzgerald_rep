from mods.models import ViewRecord
from mods.array_storage import ArrayStorage
from mods.red_black_tree import RedBlackTree
from mods.hash_table import HashTable


class ViewsManager:
    def __init__(self):
        self.storage = ArrayStorage()
        self.tree = RedBlackTree()
        self.user_index = HashTable(capacity=17)

    def add_view(self, user_id, film, release_date, status):
        view = ViewRecord.create(user_id, film, release_date, status)

        existing_records, _ = self.user_index.search(view.user_id)

        for existing in existing_records:
            if (
                existing.film == view.film and
                existing.release_date == view.release_date and
                existing.status == view.status
            ):
                raise ValueError(
                    f"Такой просмотр уже существует: пользователь {view.user_id}, "
                    f"«{view.film}», {view.release_date.to_string()}, {view.status}"
                )

        self.storage.add(view)
        self.tree.insert(view.release_date.to_number(), view)
        self.user_index.insert(view.user_id, view)

        return view

    def find_by_date(self, release_date):
        records, steps = self.tree.search(release_date.to_number())
        return records, steps

    def has_views_for_user(self, user_id):
        records, steps = self.user_index.search(user_id)
        return not records.is_empty()

    def find_by_user(self, user_id):
        records, steps = self.user_index.search(user_id)
        return records, steps

    def delete_view(self, view):
        _, steps = self.tree.search(view.release_date.to_number())

        deleted_from_tree = self.tree.delete_record(view.release_date.to_number(), view)

        if not deleted_from_tree:
            return False, steps

        self.user_index.delete_record(view.user_id, view)

        deleted_from_storage = self.storage.remove(view)

        return deleted_from_storage, steps

    def get_all_views(self):
        return self.storage.get_active_items()

    def debug_tree(self):
        return self.tree.debug_print()

    def clear(self):
        self.storage.clear()
        self.tree.clear()
        self.user_index.clear()

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            for view in self.get_all_views():
                file.write(view.to_line() + "\n")