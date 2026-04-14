import sys
from dataclasses import dataclass
from typing import Type, TypeVar, Iterator, List, Optional
from functools import total_ordering


# --- Классы данных ---

@total_ordering
@dataclass
class Date:
    day: int
    month: int
    year: int

    @classmethod
    def set(cls, string: str) -> "Date":
        day, month, year = map(int, string.split('.'))
        return cls(day, month, year)

    def __lt__(self, other: "Date") -> bool:
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        return self.day < other.day

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Date):
            return False
        return (self.year, self.month, self.day) == (other.year, other.month, other.day)

    def get(self) -> str:
        return f"{self.day:02d}.{self.month:02d}.{self.year}"


@dataclass
class Name:
    last: str
    first: str
    middle: str

    @classmethod
    def set(cls, string: str) -> "Name":
        last, first, middle = string.split()
        return cls(last, first, middle)

    def get(self) -> str:
        return f"{self.last} {self.first} {self.middle}"


@total_ordering
@dataclass
class Data:
    name: Name
    date: Date
    number: int
    discrip: str
    @classmethod
    def set(cls, string: str) -> "Data":
        name, date, num, dis = string.split(";")
        return cls(
            name=Name.set(name),
            date=Date.set(date),
            number=int(num),
            discrip=dis
        )

    def __lt__(self, other: "Data") -> bool:
        # Сначала сравниваем даты
        if self.date != other.date:
            return self.date < other.date
        # Если даты равны, сравниваем по номеру заявки
        return self.number < other.number

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Data):
            return False
        return self.date == other.date and self.number == other.number


# --- Красно-черное дерево ---

TNode = TypeVar('TNode', bound='Node')


class Node:
    def __init__(self, key: Data) -> None:
        self._key = key  # Объект Data выступает ключом
        self.value: List[Data] = [key]  # Список объектов для обработки полных совпадений
        self.parent: Optional[Node] = None
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self._color = 1  # 1 - Red, 0 - Black

    def get_color(self) -> str:
        return "black" if self._color == 0 else "red"

    def set_color(self, color: str) -> None:
        self._color = 0 if color == "black" else 1

    def get_key(self) -> Data:
        return self._key

    def is_red(self) -> bool:
        return self._color == 1

    def is_black(self) -> bool:
        return self._color == 0

    def is_null(self) -> bool:
        return self._key is None

    @classmethod
    def null(cls: Type[TNode]) -> TNode:
        # Создаем пустой узел-страж
        node = cls(None)  # type: ignore
        node._color = 0
        return node


TTree = TypeVar('TTree', bound='RedBlackTree')


class RedBlackTree:
    def __init__(self) -> None:
        self.TNULL = Node.null()
        self.root = self.TNULL
        self.size = 0

    def search(self, key_data: Data) -> Node:
        return self._search_helper(self.root, key_data)

    def _search_helper(self, node: Node, key: Data) -> Node:
        if node.is_null() or key == node.get_key():
            return node
        if key < node.get_key():
            return self._search_helper(node.left, key)
        return self._search_helper(node.right, key)

    def left_rotate(self, x: Node) -> None:
        y = x.right
        x.right = y.left
        if not y.left.is_null():
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x: Node) -> None:
        y = x.left
        x.left = y.right
        if not y.right.is_null():
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fix_insert(self, k: Node) -> None:
        while k.parent.is_red():
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.is_red():
                    u.set_color("black")
                    k.parent.set_color("black")
                    k.parent.parent.set_color("red")
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.set_color("black")
                    k.parent.parent.set_color("red")
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.is_red():
                    u.set_color("black")
                    k.parent.set_color("black")
                    k.parent.parent.set_color("red")
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.set_color("black")
                    k.parent.parent.set_color("red")
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.set_color("black")

    def insert(self, data: Data) -> None:
        # Проверяем на наличие узла с таким же ключом (Дата + Номер)
        existing_node = self.search(data)
        if not existing_node.is_null():
            existing_node.value.append(data)
            return

        # Если ключа нет, создаем новый узел
        node = Node(data)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.set_color("red")

        y = None
        x = self.root

        while not x.is_null():
            y = x
            if node.get_key() < x.get_key():
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.get_key() < y.get_key():
            y.left = node
        else:
            y.right = node

        self.size += 1
        if node.parent is None:
            node.set_color("black")
            return
        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def print_tree(self) -> None:
        self._print_helper(self.root, "", True)

    def _print_helper(self, node: Node, indent: str, last: bool) -> None:
        if not node.is_null():
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R---- ")
                indent += "     "
            else:
                sys.stdout.write("L---- ")
                indent += "|    "

            s_color = node.get_color().upper()
            # Выводим ключ и количество элементов в списке value
            key = node.get_key()
            print(f"{key.date.get()} #{key.number} ({s_color}) [Записей: {len(node.value)}]")

            self._print_helper(node.left, indent, False)
            self._print_helper(node.right, indent, True)

    def delete(self, key_data: Data) -> None:
        """Публичный метод для удаления всех записей по ключу"""
        self.delete_node_helper(self.root, key_data)

    def delete_node_helper(self, node: Node, key: Data) -> None:
        z = self.TNULL
        # Ищем узел с таким ключом
        while not node.is_null():
            if node.get_key() == key:
                z = node
                break
            if key < node.get_key():
                node = node.left
            else:
                node = node.right

        if z.is_null():
            print(f"Ключ {key.date.get()} #{key.number} не найден для удаления.")
            return

        # Если мы нашли узел, мы удаляем его целиком (весь список записей)
        y = z
        y_original_color = y.get_color()
        if z.left.is_null():
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right.is_null():
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.get_color()
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.set_color(z.get_color())

        if y_original_color == "black":
            self.delete_fix(x)

        self.size -= 1

    def delete_specific_record(self, record: Data) -> None:
        """Удаляет только один конкретный экземпляр Data из списка в узле"""
        node = self.search(record)
        if not node.is_null():
            if record in node.value:
                node.value.remove(record)
                # Если после удаления экземпляра список стал пустым — удаляем весь узел
                if not node.value:
                    self.delete(record)

# --- Пример использования ---

def main():
    bst = RedBlackTree()

    # Входные данные в формате строки
    raw_data = [
        "Иванов Иван Иванович;10.05.2023;101;Заявка на ремонт",
        "Петров Петр Петрович;10.05.2023;102;Заявка на отпуск",
        "Сидоров Сидор Сидорович;05.05.2023;101;Срочный вызов",
        "Иванов Иван Иванович;10.05.2023;101;Дубликат заявки с другим описанием",  # Полное совпадение ключа
        "Алексеев Алексей Алексеевич;12.12.2022;50;Старая запись"
    ]

    for s in raw_data:
        bst.insert(Data.set(s))

    print("Структура дерева (Ключ = Дата + Номер):")
    bst.print_tree()

    # Поиск
    search_key = Data.set("Тестов Тест Тестович;10.05.2023;101;Поиск")
    result_node = bst.search(search_key)

    if not result_node.is_null():
        print(f"\nНайдено записей по ключу {search_key.date.get()} #{search_key.number}:")
        for i, item in enumerate(result_node.value, 1):
            print(f"{i}. {item.name.get()} - {item.discrip}")


if __name__ == "__main__":
    main()