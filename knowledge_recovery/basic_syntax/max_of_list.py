def max_of_list(collection: list[int])-> None:
    max = collection[0]
    for i in collection:
        if i >= max:
            max = i
        else:
            continue
    print(max)

def main():
    max_of_list([2, 20, 3, 40, 5])

if __name__ == '__main__':
    main()