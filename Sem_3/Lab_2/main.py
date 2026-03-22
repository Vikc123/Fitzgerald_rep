import generator
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
@ds
class Name:
    last: str
    first: str
    middle: str
    @classmethod
    def set(cls, string: str) -> "Name":
        last, first, middle = string.split()
        return cls(last, first, middle)
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

def little_than(obj1: Data, obj2: Data, key: str) -> "bool":
    if key == "name":
        return (obj1.name.last, obj1.name.first, obj1.name.middle) < (obj2.name.last, obj2.name.first, obj2.name.middle)
    elif key == "date":
        return (obj1.date.year, obj1.date.month, obj1.date.day) < (obj2.date.year, obj2.date.month, obj2.date.day)
    elif key == "number":
        return obj1.number < obj2.number
    else:
        raise ValueError("Unknown sort key")
def less_than(obj1: Data, obj2: Data, key: str) -> "bool":
    if key == "name":
        return (obj1.name.last, obj1.name.first, obj1.name.middle) <= (obj2.name.last, obj2.name.first, obj2.name.middle)
    elif key == "date":
        return (obj1.date.year, obj1.date.month, obj1.date.day) <= (obj2.date.year, obj2.date.month, obj2.date.day)
    elif key == "number":
        return obj1.number <= obj2.number
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

def sort_by_merge(filename: str, key: str):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            data.append(Data.set(line))
    with open("data/output/sorted_by_merge", "w") as f:
        for d in natural_merge_sort(data, key):
            line = f"{d.name.last} {d.name.first} {d.name.middle};{d.date.day}.{d.date.month}.{d.date.year};{d.number}\n"
            f.write(line)



def main():
    generator.generate_file("data/input/10_dataset.csv", 10)
    sort_by_merge("data/input/10_dataset.csv", "name")

if __name__ == "__main__":
    main()