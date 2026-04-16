from mods import generator, RBT


def main():
    filename = "data/input/test.csv"
    # generator.generate_file(filename, 10)
    bst = RBT.RedBlackTree()
    bst.read_and_create(filename)
    bst.delete_exact_helper('Петровa Ольга Владимировна;13.01.2012;9;ЛМккЗЭБюлЩ')
    bst.print_tree()
    bst.postorder("data/output/post.txt")
    bst.clear()
    print("ddd")

if __name__ == "__main__":
    main()