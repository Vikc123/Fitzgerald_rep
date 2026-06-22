from mods import generator, RBT


def main():
    filename = "data/input/test.csv"
    # generator.generate_file(filename, 10)
    bst = RBT.RedBlackTree()
    for i in range(6):
        bst.insert(RBT.Data.set(f"Петров Алексей Вадимович;05.07.2018;{i};ЗъщщуФгвРи"))
    bst.insert(RBT.Data.set(f"Петров Алексей Вадимович;05.07.2018;6;ЗъщщуФгвРи"))
    bst.print_tree()
    bst.clear()

    print("ddd")

if __name__ == "__main__":
    main()