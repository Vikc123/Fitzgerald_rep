def my_set(collection: list) -> set:
    return set(collection)

def my_count(collection: set) -> int:
    return len(collection)

def my_find(collection: set, target) -> bool:
    return target in collection

def my_insert(collection: set, target) -> set:
    collection.add(target)
    return collection

def main():
    emails = [
        "ivan@mail.com",
        "petr@mail.com",
        "ivan@mail.com",
        "anna@mail.com",
        "petr@mail.com"
    ]
    collection = my_set(emails)
    print(my_count(collection))
    print(my_find(collection, "anna@mail.com"))
    print(my_insert(collection, "yoj30900@gmail.com"))



if __name__ == '__main__':
    main()