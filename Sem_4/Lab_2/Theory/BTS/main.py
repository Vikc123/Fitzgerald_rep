from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Date:
    day: int
    month: int
    year: int
    @classmethod
    def set(cls, data: str) -> "Date":
        day, month, year = map(int, data.split('.'))
        return cls(day, month, year)
    def to_num(self) -> "int":
        return self.year * 1000 + self.month * 100 + self.day

@dataclass
class Name:
    last: str
    first: str
    middle: str
    @classmethod
    def set(cls, data: str) -> "Name":
        last, first, middle = data.split()
        return cls(last, first, middle)

@dataclass
class Data:
    name: Name
    date: Date
    num: int
    discription: str
    @classmethod
    def set(cls, data: str):
        name, date, num, discript = data.split(';')
        return cls(
            Name.set(name),
            Date.set(date),
            int(num),
            discript
        )

@dataclass
class Node:
    data: list[Data] = field(default_factory=list[Data])
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    @classmethod
    def set(cls, data: str):
        return cls([Data.set(data)])


class BST:
    root: Node = None
    def _insert(self, current_root: Node, data: Data):
        key = (data.date.year, data.date.month, data.date.day, data.num)

        current_key = (
            current_root.data[0].date.year,
            current_root.data[0].date.month,
            current_root.data[0].date.day,
            current_root.data[0].num
        )

        if key < current_key:
            if current_root.left is None:
                current_root.left = Node([data])
            else:
                self._insert(current_root.left, data)

        elif key > current_key:
            if current_root.right is None:
                current_root.right = Node([data])
            else:
                self._insert(current_root.right, data)

        else:
            current_root.data.append(data)
    def insert(self, data: str):
        if self.root == None:
            self.root = Node.set(data)
            return
        else:
            self._insert(self.root, Data.set(data))

    def get_key(data: Data) -> tuple:
        return (data.date.year, data.date.month, data.date.day, data.num)
    def node_key(node: Node):
        return get_key(node.data[0])

    def _delete(self, node: Node, key: tuple):
        if node is None:
            return None

        if key < node.key():
            node.left = self._delete(node.left, key)

        elif key > node.key():
            node.right = self._delete(node.right, key)

        else:
            if len(node.data) > 1:
                node.data.pop()
                return node

            if node.left is None and node.right is None:
                return None

            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            min_larger_node = self._min_node(node.right)

            node.data = min_larger_node.data

            node.right = self._delete(node.right, min_larger_node.key())

        return node

    def delete(self, data: Data):
        key = (
            data.date.year,
            data.date.month,
            data.date.day,
            data.num
        )
        self.root = self._delete(self.root, key)

def main():
    a = Data.set("Петровa Мария Владимировна;30.07.1985;2;ЯдЮжйВЯЛкЖ")
    bst = BST()
    bst.insert("Петровa Мария Владимировна;30.07.1985;2;ЯдЮжйВЯЛкЖ")
    bst.insert("Петровa Ясиль Владимировна;30.07.1985;2;ЯдЮжйВЯЛкЖ")
    bst.insert("Сидоровa Наталья Владимировна;07.08.2006;0;ЙДкМЙщРдБЬ")
    bst.insert("Морозовa Елена Александровна;28.12.1990;3;АхкИщЩУЩъЭ")
    bst.insert("Федоров Борис Алексеевич;19.01.2007;4;МрМъчёУыФШ")
    bst.insert("Петровa Мария Владимировна;30.07.1985;1;ЯдЮжйВЯЛкЖ")
    bst.delete(a)

    print("dsds")
if __name__ == "__main__":
    main()
