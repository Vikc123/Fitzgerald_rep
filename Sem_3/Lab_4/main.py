from modules import sort, my_class, generator as g


def main():
    filename = "data/input/10_dataset.csv"
    g.generate_file(filename, 10)
    filename_to = "data/output/sorted_by_merge.csv"
    sort.sort_by_merge(filename_to, "name")
if __name__ == "__main__":
    main()