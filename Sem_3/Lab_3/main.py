import generator
import time
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
@ds
class Data:
    name: Name
    date: Date
    number: int
    @classmethod
    def set(cls, string: str) -> "Data":
        name, date, num = string.split(";")
        return cls(
            name = Name.set(name),
            date = Date.set(date),
            number = int(num)
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

def less_than(obj1: Data, obj2: Data, key: str) -> "bool":
    if key == "name":
        return (obj1.name.last, obj1.name.first, obj1.name.middle) < (obj2.name.last, obj2.name.first, obj2.name.middle)
    elif key == "date":
        return (obj1.date.year, obj1.date.month, obj1.date.day) < (obj2.date.year, obj2.date.month, obj2.date.day)
    elif key == "number":
        return obj1.number < obj2.number
    else:
        raise ValueError("Unknown sort key")
def little_than(obj1: Data, obj2: Data, key: str) -> "bool":
    if key == "name":
        return (obj1.name.last, obj1.name.first, obj1.name.middle) <= (obj2.name.last, obj2.name.first, obj2.name.middle)
    elif key == "date":
        return (obj1.date.year, obj1.date.month, obj1.date.day) <= (obj2.date.year, obj2.date.month, obj2.date.day)
    elif key == "number":
        return obj1.number <= obj2.number
    else:
        raise ValueError("Unknown sort key")
def more_than(obj1: Data, obj2: Data, key: str) -> "bool":
    if key == "name":
        return (obj1.name.last, obj1.name.first, obj1.name.middle) > (obj2.name.last, obj2.name.first, obj2.name.middle)
    elif key == "date":
        return (obj1.date.year, obj1.date.month, obj1.date.day) > (obj2.date.year, obj2.date.month, obj2.date.day)
    elif key == "number":
        return obj1.number > obj2.number
    else:
        raise ValueError("Unknown sort key")

def is_stable(test_data: list[Data], key: str, sort_func) -> "bool":
    sorted_data = sort_func(test_data, key)
    for i in range(len(sorted_data) - 1):
        curr = sorted_data[i]
        nxt = sorted_data[i + 1]
        if curr.number == nxt.number:
            idx_curr_original = test_data.index(curr)
            idx_nxt_original = test_data.index(nxt)
            if idx_curr_original > idx_nxt_original:
                return False
    return True

def target_conv(target, mode: str) -> "int":
    if mode == "name" and type(target) == str:
        last, first, middle = target.split()
        fio = (last + first + middle).upper()
        res = 0
        for i, char in enumerate(fio[:12]):
            res += ord(char) * (1100 ** (12 - i))
        return res
    elif mode == "date" and type(target) == str:
        day, month, year = map(int, target.split('.'))
        return year * 1000 + month * 100 + day
    elif mode == "num" and type(target) == int:
        return target
    elif mode == "full" and type(target) == str:
        name, date, num = target.split(";")
        last, first, middle = name.split()
        day, month, year = map(int, date.split('.'))
        fio = (last + first + middle).upper()
        date_hash = year * 1000 + month * 100 + day
        fio_hash = 0
        for i, char in enumerate(fio[:12]):
            fio_hash += ord(char) * (1100 ** (12 - i))
        return fio_hash + date_hash + int(num)
    else:
        raise ValueError("Unknown sort key")


def merge(left: list[Data], right: list[Data], key: str) -> list[Data]:
    merged = []
    il = 0
    ir = 0
    while il < left.__len__() and ir < right.__len__():
        if little_than(left[il],right[ir], key):
            merged.append(left[il])
            il+=1
        else:
            merged.append(right[ir])
            ir+=1
    while il < left.__len__():
        merged.append(left[il])
        il+=1
    while ir < right.__len__():
        merged.append(right[ir])
        ir+=1
    return merged

def natural_merge_sort(data: list[Data], key: str) -> "list[Data]":
    runs = []
    start_of_run = 0
    for i in range(1, data.__len__()):
        if less_than(data[i-1],data[i], key):
            continue
        else:
            runs.append(data[start_of_run: i])
            start_of_run = i
    runs.append(data[start_of_run:])

    while runs.__len__()>1:
        new_runs = []
        for i in range(0, runs.__len__(), 2):
            if i+1 < runs.__len__():
                new_runs.append(merge(runs[i], runs[i+1], key))
            else:
                new_runs.append(runs[i])
        runs = new_runs
    return runs[0]

def binary_insertion_sort(data: list[Data], key: str) -> "list[Data]":
    for i in range(1, len(data)):
        compared = data[i]

        left, right = 0, i - 1
        while left <= right:
            mid = (left + right) // 2
            if more_than(data[mid], compared, key):
                right = mid - 1
            else:
                left = mid + 1

        for j in range(i, left, -1):
            data[j] = data[j - 1]

        data[left] = compared

    return data

def sort_by_merge(filename: str, key: str):
    data = []
    with open(filename, 'r') as f:
        next(f)
        for line in f:
            data.append(Data.set(line))
    start = time.time()
    sorted = natural_merge_sort(data, key)
    end = time.time()
    with open("data/output/sorted_by_merge.csv", "w") as f:
        f.write("fio;date;num\n")
        for d in sorted:
            line = f"{d.name.last} {d.name.first} {d.name.middle};{d.date.day}.{d.date.month}.{d.date.year};{d.number}\n"
            f.write(line)
        f.write(f"сортировка выполнена за {end - start} секунд\n")
        if is_stable(data, key, natural_merge_sort):
            f.write("устойчива")
        else:
            f.write("неустойчива")

def sort_by_binary_inserts(filename: str, key: str):
    data = []
    with open(filename, 'r') as f:
        next(f)
        for line in f:
            data.append(Data.set(line))
    start = time.time()
    sorted = binary_insertion_sort(data, key)
    end = time.time()

    with open("data/output/sorted_by_binary_inserts.csv.csv", "w") as f:
        f.write("fio;date;num\n")
        for d in sorted:
            line = f"{d.name.last} {d.name.first} {d.name.middle};{d.date.day}.{d.date.month}.{d.date.year};{d.number}\n"
            f.write(line)
        f.write(f"сортировка выполнена за {end - start} секунд\n")
        if is_stable(data, key, binary_insertion_sort):
            f.write("устойчива")
        else:
            f.write("неустойчива")

def linear_search(data: list[Data], target, mode: str) -> "int":
    for i in range(data.__len__()):
        if data[i].to_num(mode) == target_conv(target, mode):
            return i
        else:
            continue

def search_by_linear(filename: str, target, mode: str) -> None:
    data = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines[1:-2]:
            data.append(Data.set(line))
    print(f"заданное вхождение находится на строке под номером {linear_search(data, target, mode)}")

def interpolation_search(data: list[Data], target, mode: str) -> "int":
    l = 0
    r = data.__len__()-1
    while data[l].to_num(mode) < target_conv(target, mode) and data[r].to_num(mode) > target_conv(target, mode):
        if data[l].to_num(mode) == data[r].to_num(mode):
            break
        index = (target_conv(target, mode) - data[l].to_num(mode))*(l-r)//(data[l].to_num(mode) - data[r].to_num(mode)) + l
        if data[index].to_num(mode) > target_conv(mode):
            r = index-1
        elif data[index].to_num(mode) < target_conv(target, mode):
            l = index+1
        else:
            return index
    if data[l].to_num(mode) == target_conv(target, mode):
        return l
    if data[r].to_num(mode) == target_conv(target, mode):
        return r
    return -1

def search_by_interpolation(filename: str, target, mode: str) -> None:
    data = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines[1:-2]:
            data.append(Data.set(line))
    print(f"заданное вхождение находится на строке под номером {interpolation_search(data, target, mode)}\n")


def main():
    # filename = "data/input/10_dataset.csv"
    # generator.generate_file(filename, 10)
    # sort_by_merge(filename, "name")
    # sort_by_binary_inserts(filename, "name")
    search_filename = "data/output/sorted_by_binary_inserts.csv"
    search_by_linear(search_filename, "10.4.2016", "date")
    search_by_linear(search_filename, "10.4.2016", "date")

if __name__ == "__main__":
    main()