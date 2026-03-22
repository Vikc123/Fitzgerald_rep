def binary_insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]

        left, right = 0, i - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] > key:
                right = mid - 1
            else:
                left = mid + 1

        for j in range(i, left, -1):
            arr[j] = arr[j - 1]

        arr[left] = key

    return arr

def main():
    data = [6,2,7,3,1,8,5,4]
    print(binary_insertion_sort(data))

if __name__ == "__main__":
    main()