from dataclasses import dataclass as ds

@ds
class Date:
    day: int
    month: int
    year: int
    @classmethod
    def set(cls, string: str) -> "Date":
        day, month, year = map(int, string.split('.'))
        return cls(day, month, year)
    def to_num(self)-> "int":
        return self.year * 1000 + self.month * 100 + self.day

    def get(self) -> "str":
        return f"{self.day}.{self.month}.{self.year}"
@ds
class Name:
    last: str
    first: str
    middle: str
    @classmethod
    def set(cls, string: str) -> "Name":
        last, first, middle = string.split()
        return cls(last, first, middle)
    def to_num(self) -> "int":
        fio = (self.last + self.first + self.middle).upper()
        res = 0
        for i, char in enumerate(fio[:12]):
            res += ord(char) * (1100 ** (12 - i))
        return res
    def get(self) -> "str":
        return f"{self.last} {self.first} {self.middle}"
@ds
class Data:
    name: Name
    date: Date
    number: int
    discrip: str
    @classmethod
    def set(cls, string: str) -> "Data":
        name, date, num, dis= string.split(";")
        return cls(
            name = Name.set(name),
            date = Date.set(date),
            number = int(num),
            discrip = dis
        )
    def to_num(self, mode: str) -> "int":
        if mode == "name":
            return self.name.to_num()
        elif mode == "date":
            return self.date.to_num()
        elif mode == "num":
            return self.number
        elif mode == "full":
            return self.name.to_num() + self.date.to_num() + self.number
        else:
            raise ValueError("Unknown sort key")