from dataclasses import dataclass as ds
import sys
from typing import Type, TypeVar, Iterator, List, Optional
from functools import total_ordering

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
        return f"{self.name};{self.date};{self.number};{self.discrip}"

TNode = TypeVar('TNode', bound='Node')

class Node():
    def __init__(self: TNode, data: Optional[Data]) -> None:
        self._data = data
        self.value: List[Data] = [data] if data is not None else []
        self.parent: Optional['Node'] = None
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None
        self._color = 1

    def __repr__(self: TNode) -> str:
        return "Key: " + str(self._data) + " Value: " + str(self.value)

    def get_color(self: TNode) -> str:
        return "black" if self._color == 0 else "red"

    def set_color(self: TNode, color: str) -> None:
        if color == "black":
            self._color = 0
        elif color == "red":
            self._color = 1
        else:
            raise Exception("Unknown color")

    def get_data(self: TNode) -> Data:
        return self._data

    def is_red(self: TNode) -> bool:
        return self._color == 1

    def is_black(self: TNode) -> bool:
        return self._color == 0

    def is_null(self: TNode) -> bool:
        return self._data is None

    def depth(self: TNode) -> int:
        return 0 if self.parent is None else self.parent.depth() + 1

    @classmethod
    def null(cls: Type[TNode]) -> TNode:
        node = cls(None)
        node.set_color("black")
        return node

T = TypeVar('T', bound='RedBlackTree')

class RedBlackTree():
    def __init__(self: T) -> None:
        self.TNULL = Node.null()
        self.root = self.TNULL
        self.size = 0
        self._iter_format = 0

    def __iter__(self: T) -> Iterator:
        if self._iter_format == 0:
            return iter(self.preorder())
        if self._iter_format == 1:
            return iter(self.inorder())
        if self._iter_format == 2:
            return iter(self.postorder())

    def __getitem__(self, data: Data) -> List[Data]:
        node = self.search(data)
        if node.is_null():
            return []
        return node.value

    def __setitem__(self, data: Data, value: Data) -> None:

        node = self.search(data)
        if not node.is_null():
            node.value.append(value)
        else:
            self.insert(value)

    def get_root(self: T) -> Node:
        return self.root

    def set_iteration_style(self: T, style: str) -> None:
        if style == "pre":
            self._iter_format = 0
        elif style == "in":
            self._iter_format = 1
        elif style == "post":
            self._iter_format = 2
        else:
            raise Exception("Unknown style.")

    def inorder(self: T, filename: str) -> None:
        nodes = self.in_order_helper(self.root)
        self._write_to_file(nodes, filename)

    def preorder(self: T, filename: str) -> None:
        nodes = self.pre_order_helper(self.root)
        self._write_to_file(nodes, filename)

    def postorder(self: T, filename: str) -> None:
        nodes = self.post_order_helper(self.root)
        self._write_to_file(nodes, filename)

    def _write_to_file(self, nodes: List[Node], filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            for node in nodes:
                for item in node.value:
                    f.write(f"{item.name.get()};{item.date.get()};{item.number};{item.discrip}\n")

    def pre_order_helper(self: T, node: Node) -> list:
        if node.is_null():
            return []

        output = [node]
        output.extend(self.pre_order_helper(node.left))
        output.extend(self.pre_order_helper(node.right))
        return output

    def in_order_helper(self: T, node: Node) -> list:
        if node.is_null():
            return []

        output = []
        output.extend(self.in_order_helper(node.left))
        output.extend([node])
        output.extend(self.in_order_helper(node.right))
        return output

    def post_order_helper(self: T, node: Node) -> list:
        if node.is_null():
            return []

        output = []
        output.extend(self.post_order_helper(node.left))
        output.extend(self.post_order_helper(node.right))
        output.extend([node])
        return output

    def search_tree_helper(self: T, node: Node, data: Data) -> Node:
        if node.is_null() or data == node.get_data():
            return node

        if data < node.get_data():
            return self.search_tree_helper(node.left, data)
        return self.search_tree_helper(node.right, data)

    def delete_exact_helper(self, data: str) -> None:
        target = Data.set(data)
        node = self.search(target)

        if node.is_null():
            print(f"Узел с ключом {target.date.get()} #{target.number} не найден.")
            return

        found_idx = -1
        for i, item in enumerate(node.value):
            if (item.date == target.date and
                    item.number == target.number and
                    item.name == target.name and
                    item.discrip == target.discrip):
                found_idx = i
                break

        if found_idx != -1:
            node.value.pop(found_idx)
            if not node.value:
                self.delete_node_helper(self.root, target)
        else:
            print("Запись с полным совпадением всех полей не найдена в списке.")

    def delete_fix(self: T, x: Node) -> None:
        while x != self.root and x.is_black():
            if x == x.parent.left:
                s = x.parent.right
                if s.is_red():
                    s.set_color("black")
                    x.parent.set_color("red")
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.is_black() and s.right.is_black():
                    s.set_color("red")
                    x = x.parent
                else:
                    if s.right.is_black():
                        s.left.set_color("black")
                        s.set_color("red")
                        self.right_rotate(s)
                        s = x.parent.right

                    s.set_color(x.parent.get_color())
                    x.parent.set_color("black")
                    s.right.set_color("black")
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.is_red():
                    s.set_color("black")
                    x.parent.set_color("red")
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.is_black() and s.right.is_black():
                    s.set_color("red")
                    x = x.parent
                else:
                    if s.left.is_black():
                        s.right.set_color("black")
                        s.set_color("red")
                        self.left_rotate(s)
                        s = x.parent.left

                    s.set_color(x.parent.get_color())
                    x.parent.set_color("black")
                    s.left.set_color("black")
                    self.right_rotate(x.parent)
                    x = self.root
        x.set_color("black")

    def __rb_transplant(self: T, u: Node, v: Node) -> None:
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_node_helper(self: T, node: Node, data: Data) -> None:
        z = self.TNULL
        while not node.is_null():
            if node.get_data() == data:
                z = node
                break #????

            if data < node.get_data():
                node = node.left
            else:
                node = node.right

        if z.is_null():
            print(f"Ключ {data.date.get()} #{data.number} не найден для удаления.")
            return

        y = z
        y_original_color = y.get_color()
        if z.left.is_null():
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right.is_null()):
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

    def fix_insert(self: T, node: Node) -> None:
        while node.parent.is_red():
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left
                if u.is_red():
                    u.set_color("black")
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    self.left_rotate(node.parent.parent)
            else:
                u = node.parent.parent.right

                if u.is_red():
                    u.set_color("black")
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    self.right_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.set_color("black")

    def __print_helper(self: T, node: Node, indent: str, last: bool) -> None:
        if not node.is_null():
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----  ")
                indent += "     "
            else:
                sys.stdout.write("L----   ")
                indent += "|    "

            s_color = "RED" if node.is_red() else "BLACK"
            key = node.get_data()
            print(f"{key.date.get()} #{key.number} ({s_color}) [Записей: {len(node.value)}]")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def search(self: T, data: Data) -> Node:
        return self.search_tree_helper(self.root, data)

    def minimum(self: T, node: Node = None) -> Node:
        if node is None:
            node = self.root
        if node.is_null():
            return self.TNULL
        while not node.left.is_null():
            node = node.left
        return node

    def maximum(self: T, node: Node = None) -> Node:
        if node is None:
            node = self.root
        if node.is_null():
            return self.TNULL
        while not node.right.is_null():
            node = node.right
        return node

    def successor(self: T, x: Node) -> Node:
        if not x.right.is_null():
            return self.minimum(x.right)

        y = x.parent
        while not y.is_null() and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self: T,  x: Node) -> Node:
        if (not x.left.is_null()):
            return self.maximum(x.left)

        y = x.parent
        while not y.is_null() and x == y.left:
            x = y
            y = y.parent

        return y

    def left_rotate(self: T, x: Node) -> None:
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

    def right_rotate(self: T, x: Node) -> None:
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

    def insert(self: T, data: Data) -> None:
        existing_node = self.search(data)
        if not existing_node.is_null():
            existing_node.value.append(data)
            return
        node = Node(data)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.set_color("red")

        y = None
        x = self.root

        while not x.is_null():
            y = x
            if node.get_data() < x.get_data():
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.get_data() < y.get_data():
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

    def delete(self: T, data: Data) -> None:
        self.delete_node_helper(self.root, data)

    def print_tree(self: T) -> None:
        self.__print_helper(self.root, "", True)

    def read_and_create(self, filename: str) -> None:
        try:
            with open(filename, "r", encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[1:], 1):
                    try:
                        self.insert(Data.set(line))
                    except ValueError as e:
                        print(f"Ошибка в строке {i}: {e}. Пропускаю...")
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")

    def clear(self: T) -> None:
        self.root = self.TNULL
        self.size = 0
        import gc
        gc.collect()
        print("Дерево полностью очищено.")