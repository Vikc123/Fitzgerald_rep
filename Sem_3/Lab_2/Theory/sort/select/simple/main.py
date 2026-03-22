def simple(data):
    for i in range(0, data.__len__() - 2):
        min = i
        for j in range(i+1, data.__len__()-1):
            if data[j] < data[min]:
                min = j
        if min != i:
            buff = data[i]
            data[i] = data[min]
            data[min] = buff
    return data
def main():
    data = [32, 4, 12, 43, 17, 9, 25, 21]
    print(simple(data))

if __name__ == "__main__":
    main()