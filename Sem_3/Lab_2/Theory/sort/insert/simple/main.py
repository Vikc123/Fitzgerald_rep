def insert(data):
    for i in range(0, data.__len__()):
        for j in range(i, 0, -1):
            if data[j] <= data[j-1]:
                buff = data[j]
                data[j] = data[j-1]
                data[j-1] = buff
            else:
                break
    return data

def main():
    data = [6,2,7,3,1,8,5,4]
    print(insert(data))

if __name__ == "__main__":
    main()