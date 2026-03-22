def merge(left, right):
    merged = []
    il = 0
    ir = 0
    while il < left.__len__() and ir < right.__len__():
        if left[il] <= right[ir]:
            merged.append(left[il])
            il+=1
        else:
            merged.append(right[ir])
            ir+=1

    while il < left.__len__():
        merged.append(left[il])
        il += 1
    while ir < right.__len__():
        merged.append(right[ir])
        ir += 1
    return merged

def merge_sort(data):
    if len(data) <= 1:
        return data
    else:
        left = []
        right = []
        for i in range(0, len(data)//2):
            left.append(data[i])
        for i in range(len(data)//2, len(data)):
            right.append(data[i])
        return merge(merge_sort(left), merge_sort(right))

def main():
    data = [6,2,7,3,1,8,5,4]
    print(merge_sort(data))
if __name__ == "__main__":
    main()