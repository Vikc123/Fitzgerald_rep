from mods import linked_list as ll

def main():
    List = ll.LinList()
    a = [1,3,3]
    for i in a:
        List.append(i)
    List.del_before(1)
    a = 2
    print("done")

if __name__ == "__main__":
    main()