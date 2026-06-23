def even_numbers_counter(numbers: list) -> None:
    counter = 0
    for i in numbers:
        if i % 2 == 0:
            counter += 1
        else:
            continue
    print(counter)



def main():
    even_numbers_counter([2,3,4,5,6,7,8,9])

if __name__ == "__main__":
    main()