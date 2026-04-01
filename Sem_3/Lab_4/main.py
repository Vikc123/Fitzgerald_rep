from modules import sort, search, generator as g
def main():
    filename = "data/input/10_dataset.csv"
    # g.generate_file(filename, 10)
    sort.sort_by_merge(filename, "name")
    sort.sort_by_binary_inserts(filename, "name")
    search.search_by_linear("data/output/sorted_by_merge.csv", "Попов Виктор Борисович", "name")
    search.serch_by_boyer_moore_horspul("data/output/sorted_by_merge.csv", "Попов Виктор Борисович", "name")
if __name__ == "__main__":
    main()