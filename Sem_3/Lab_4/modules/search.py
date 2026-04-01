from .my_class import Data

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
        if data[index].to_num(mode) > target_conv(target, mode):
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

def shift(pattern: str) -> "dict":
    table = {}
    for i in range(len(pattern)):
        table[pattern[i]] = len(pattern) - 1 - i
    return table

def boyer_moore_horspul(text: str, pattern: str) -> "bool":
    t = len(text)
    p = len(pattern)
    shift_tabl = shift(pattern)
    i = 0
    while i <= t - p:
        j = p-1
        while j >= 0 and pattern[j] == text[i+j]:
            j -= 1
        if j < 0:
            return True
        i += shift_tabl.get(text[i+j], p)
    return False

def serch_by_boyer_moore_horspul(filename: str, pattern: str, mode: str) -> None:
    data = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines[1:-2]:
            data.append(Data.set(line))
    if mode == "name":
        for i in range(len(data)):
            if boyer_moore_horspul(data[i].name.get(), pattern) >= 0:
                print(data[i])
                return
            else:
                print("Данное вхождение не найдено(")
                return
    elif mode == "disc":
        for i in range(len(data)):
            if boyer_moore_horspul(data[i].discrip, pattern) >= 0:
                print(data[i])
                return
            else:
                print("Данное вхождение не найдено(")
                return
    else:
        raise ValueError("Unknown sort key")