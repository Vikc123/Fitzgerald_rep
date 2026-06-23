def print_more_than(collection: list, target: int) -> None:
    print(f"Больше чем {target}: ")
    for i in collection:
        if i > target:
            print(i)
        else:
            continue


def summ(collection: list) -> None:
    print("Сумма: ")
    sum = 0
    for i in collection:
        sum+=i
    print(sum)

def max(collection: list) -> None:
    print("Максимум: ")
    max = 0
    for i in collection:
        if i > max:
            max = i
        else:
            continue
    print(max)

def rm_less_than(collection: list, target: int) -> None:
    print(f"После удаления всех меньше {target}:")
    for i in collection:
        if i <= target:
            collection.remove(i)
        else:
            continue
    print(collection)

def main():
    print_more_than([1200, 500, 3400, 800, 150, 2200], 1000)
    summ([1200, 500, 3400, 800, 150, 2200])
    max([1200, 500, 3400, 800, 150, 2200])
    rm_less_than([1200, 500, 3400, 800, 150, 2200], 500)

if __name__ == "__main__":
    main()