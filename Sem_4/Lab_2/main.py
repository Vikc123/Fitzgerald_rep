from mods import generator, RBT


def main():
    filename = "data/input/10_dataset.csv"
    # generator.generate_file(filename, 10)
    bst = RBT.RedBlackTree()
    bst.read_and_create(filename)
    bst.print_tree()
    print("ddd")

if __name__ == "__main__":
    main()