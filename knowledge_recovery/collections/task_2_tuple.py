from cmath import sqrt


def print_coords(collection: list) -> None:
    for i in collection:
        print(f"x = {i[0]}, y = {i[1]}")

def max(collection: list) -> None:
    maximum = collection[0]
    for i in collection:
        if i[0] > maximum[0]:
            maximum = i
        else:
            continue
    print(maximum)

def distance(collection: list, target: tuple) -> None:
    for i in collection:
        print(f"расстояние между точкой а({i}) и точкой в({target}) = {sqrt((i[0]-target[0])**2 + (i[1]-target[1])**2)}")

def main():
    collection = [(1,2), (3,4), (5,6), (7,8)]
    print_coords(collection)
    max(collection)
    distance(collection, (0, 0))
if __name__ == "__main__":
    main()