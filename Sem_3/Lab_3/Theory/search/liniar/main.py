def linear_search(data: list[int], target: int) -> "int":
    for i in range(data.__len__()):
        if data[i] == target:
            return i
        else:
            continue

def main():
    data = [1,2,3,4,5,6,7,8,9]
    print(linear_search(data, 3))

if __name__ == '__main__':
    main()