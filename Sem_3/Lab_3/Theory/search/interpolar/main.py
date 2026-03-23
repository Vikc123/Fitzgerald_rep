def interpolation_search(data: list[int], target: int) -> int:
    l = 0
    r = data.__len__()-1
    while data[l] < target and data[r] > target:
        if data[l] == data[r]:
            break
        index = (target - data[l])*(l-r)//(data[l] - data[r]) + l
        if data[index] > target:
            r = index-1
        elif data[index] < target:
            l = index+1
        else:
            return index
    if data[l] == target:
        return l
    if data[r] == target:
        return r
    return -1

def main():
    data = [1,2,3,4,5,6,7,8,9]
    print(interpolation_search(data, 5))


if __name__ == "__main__":
    main()