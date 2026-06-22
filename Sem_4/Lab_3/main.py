from dataclasses import dataclass as ds
from typing import Optional
from functools import total_ordering
from mods import generator

@total_ordering
@ds
class Date:
    day: int
    month: int
    year: int

    def __lt__(self, other: "Date") -> bool:
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        return self.day < other.day

    def __le__(self, other: "Date") -> bool:
        return (self.year, self.month, self.day) <= (other.year, other.month, other.day)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Date):
            return False
        return (self.year, self.month, self.day) == (other.year, other.month, other.day)

    @classmethod
    def set(cls, string: str) -> "Date":
        day, month, year = map(int, string.split('.'))
        return cls(day, month, year)

    def get(self) -> "str":
        return f"{self.day}.{self.month}.{self.year}"

    def validate(self):
        if self.day < 1 or self.month < 1 or self.year < 1:
            raise ValueError(f"Дата не может содержать отрицательные числа или нули: {self.get()}")

        if self.month > 12:
            raise ValueError(f"Месяц не может быть больше 12: {self.month}")

        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0):
            days_in_month[2] = 29

        if self.day > days_in_month[self.month]:
            raise ValueError(f"В выбранном месяце/году нет столько дней ({self.day}): {self.get()}")


@ds
class Name:
    last: str
    first: str
    middle: str

    @classmethod
    def set(cls, string: str) -> "Name":
        last, first, middle = string.split()
        return cls(last, first, middle)

    def get(self) -> "str":
        return f"{self.last} {self.first} {self.middle}"

    def validate(self):
        for part, label in [(self.last, "Фамилия"), (self.first, "Имя"), (self.middle, "Отчество")]:
            if not part.strip():
                raise ValueError(f"Поле {label} не может быть пустым")
            if any(char.isdigit() for char in part):
                raise ValueError(f"В ФИО обнаружены цифры: {part}")


@total_ordering
@ds
class Data:
    name: Name
    date: Date
    number: int
    discrip: str

    def __lt__(self, other: "Data") -> bool:
        if self.date != other.date:
            return self.date < other.date
        return self.number < other.number

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Data):
            return False
        return self.date == other.date and self.number == other.number

    def __le__(self, other: "Data") -> bool:
        if self.date < other.date:
            return True
        if self.date == other.date:
            return self.number <= other.number
        return False

    @classmethod
    def set(cls, string: str) -> "Data":
        if not string or not string.strip():
            raise ValueError("Пустая строка данных")

        parts = [s.strip() for s in string.split(";")]
        if len(parts) < 4:
            raise ValueError("Недостаточно данных в строке (должно быть 4 раздела через ';')")

        fio_str, date_str, num_str, dis = parts

        fio_parts = fio_str.split()
        if len(fio_parts) != 3:
            raise ValueError(f"ФИО должно состоять из 3 слов, получено: {len(fio_parts)}")

        try:
            number = int(num_str)
        except ValueError:
            raise ValueError(f"Номер заявки должен быть числом, получено: '{num_str}'")

        if number < 0:
            raise ValueError(f"Номер заявки не может быть отрицательным: {number}")

        name_obj = Name(*fio_parts)
        date_obj = Date.set(date_str)

        name_obj.validate()
        date_obj.validate()

        if not dis:
            raise ValueError("Описание не может быть пустым")

        return cls(name=name_obj, date=date_obj, number=number, discrip=dis)

    def get(self):
        return f"{self.name.get()};{self.date.get()};{self.number};{self.discrip}"



@ds
class Slot:
    data: Optional[Data] = None
    status: int = 0


class HashTable:
    def __init__(self, initial_capacity: int = 8, load_factor_threshold: float = 0.7):
        self.capacity = initial_capacity
        self.size = 0
        self.threshold = load_factor_threshold
        self.table = [Slot() for _ in range(self.capacity)]

    def _date_to_num(self, date: Date) -> int:
        return date.year * 10000 + date.month * 100 + date.day

    def _hash(self, date: Date) -> int:
        date_val = self._date_to_num(date)
        squared = date_val ** 2
        sq_str = str(squared)

        if len(sq_str) <= 4:
            mid_val = int(sq_str)
        else:
            mid_idx = len(sq_str) // 2
            mid_val = int(sq_str[mid_idx - 2: mid_idx + 2])

        return mid_val % self.capacity

    def _resize(self):
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [Slot() for _ in range(self.capacity)]

        for slot in old_table:
            if slot.status == 1 and slot.data is not None:
                self.insert(slot.data)

    def insert(self, item: Data):
        if self.size / self.capacity >= self.threshold:
            self._resize()

        idx = self._hash(item.date)
        first_deleted_idx = -1
        count = 0

        while self.table[idx].status != 0 and count < self.capacity:
            if self.table[idx].status == 1:
                current = self.table[idx].data
                if (current.date == item.date and current.number == item.number and
                        current.name == item.name and current.discrip == item.discrip):
                    return

            elif self.table[idx].status == 2 and first_deleted_idx == -1:
                first_deleted_idx = idx

            idx = (idx + 1) % self.capacity
            count += 1

        insert_idx = first_deleted_idx if first_deleted_idx != -1 else idx

        self.table[insert_idx].data = item
        self.table[insert_idx].status = 1
        self.size += 1

    def search(self, date: Date, number: int) -> Optional[Data]:
        idx = self._hash(date)
        count = 0

        while self.table[idx].status != 0 and count < self.capacity:
            if self.table[idx].status == 1:
                current = self.table[idx].data
                if current.date == date and current.number == number:
                    return current
            idx = (idx + 1) % self.capacity
            count += 1
        return None

    def delete(self, item: Data) -> bool:
        idx = self._hash(item.date)
        count = 0
        while self.table[idx].status != 0 and count < self.capacity:
            if self.table[idx].status == 1:
                current = self.table[idx].data
                if current.date == item.date and current.number == item.number:
                    self.table[idx].status = 2
                    self.table[idx].data = None
                    self.size -= 1
                    return True
            idx = (idx + 1) % self.capacity
            count += 1
        return False

    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                header = file.readline()

                line_count = 1
                for line in file:
                    line_count += 1
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        item = Data.set(line)
                        self.insert(item)
                    except ValueError as ve:
                        print(f"Ошибка в строке {line_count}: {ve}")
                    except Exception as e:
                        print(f"Непредвиденная ошибка в строке {line_count}: {e}")

            print(f"Загрузка завершена. Успешно добавлено элементов: {self.size}")

        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден.")

    def display(self):
        print("\n" + "=" * 80)
        print(f"{'Index':<7} | {'Status':<8} | {'Data (Key: Date + Num)':<40}")
        print("-" * 80)

        for i, slot in enumerate(self.table):
            status_map = {0: "Empty", 1: "Occupied", 2: "Deleted"}
            status_str = status_map[slot.status]

            if slot.status == 1 and slot.data:
                data_info = f"[{slot.data.date.get()} | #{slot.data.number}] {slot.data.name.last}..."
            else:
                data_info = "---"

            print(f"{i:<7} | {status_str:<8} | {data_info}")
        print("=" * 80 + "\n")

    def __del__(self):
        self.table.clear()
        # print("Хэш-таблица была успешно удалена из памяти.")

def main():
    # generator.generate_file("data/input.csv", 10)
    ht = HashTable(initial_capacity=19, load_factor_threshold=1.0)
    ht.load_from_file("data/input.csv")
    ht.display()
    target_data = Data.set("Волков Юлия Вдимовн;21.03.2003;0;чПмбаШЧФшЩ")
    if ht.delete(target_data):
        print(f"Запись {target_data.name.last} удалена.")
    ht.insert(Data.set("Волков Юлия Вадимовн;22.03.2003;1;чПмбаШЧФшЩ"))
    ht.display()
    target_data_1 = Data.set("В Ю В;01.01.2000;0;ч")
    if ht.delete(target_data_1):
        print(f"Запись {target_data.name.last} удалена.")

if __name__ == '__main__':
    main()