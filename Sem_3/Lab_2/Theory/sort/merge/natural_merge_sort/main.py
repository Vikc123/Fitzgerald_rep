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
        il+=1
    while ir < right.__len__():
        merged.append(right[ir])
        ir+=1
    return merged

def natural_merge_sort(data):
    runs = []
    start_of_run = 0
    for i in range(1, data.__len__()):
        if data[i-1] < data[i]:
            continue
        else:
            runs.append(data[start_of_run: i])
            start_of_run = i
    runs.append(data[start_of_run:])

    while runs.__len__()>1:
        new_runs = []
        for i in range(0, runs.__len__(), 2):
            if i+1 < runs.__len__():
                new_runs.append(merge(runs[i], runs[i+1]))
            else:
                new_runs.append(runs[i])
        runs = new_runs
    return runs[0]

def main():
    data = [2, 6, 7, 1, 3, 8, 4, 5]
    print(natural_merge_sort(data))

if __name__ == "__main__":
    main()