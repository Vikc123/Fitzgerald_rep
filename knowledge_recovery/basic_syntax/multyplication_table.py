def print_multyplication_table():
    for i in range(1, 9):
        for j in range(1, 9):
            print(f"{i} * {j} = {i * j} ")
        print("\n")

def main():
    print_multyplication_table()

if __name__ == '__main__':
    main()