from mods.models import ViewRecord
from mods.array_storage import ArrayStorage
from mods.hash_table import HashTable


class ViewsManager:
    def __init__(self, initial_capacity=17):
        self.storage = ArrayStorage()
        self.hash_table = HashTable(capacity=initial_capacity)

    def add_view(self, user_id, film, year, status):
        view = ViewRecord(user_id, film, year, status)

        self.storage.add(view)
        self.hash_table.insert(year, view)

        return view

    def find_by_year(self, year):
        records, steps = self.hash_table.search(year)
        return records, steps

    def delete_view(self, view):
        deleted_from_hash, steps = self.hash_table.delete_record(view.year, view)

        if not deleted_from_hash:
            return False, steps

        deleted_from_storage = self.storage.remove(view)

        return deleted_from_storage, steps

    def get_all_views(self):
        return self.storage.get_active_items()

    def debug_hash_table(self):
        return self.hash_table.debug_print()

    def clear(self):
        self.storage.clear()
        self.hash_table.clear()

    def load_from_file(self, filename):
        self.clear()

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

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            for view in self.get_all_views():
                file.write(view.to_line() + "\n")