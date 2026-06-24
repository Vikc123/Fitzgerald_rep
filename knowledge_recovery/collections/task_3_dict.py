def add(collection: dict, user, key) -> None:
    collection[key] = user
    print(collection)

def rm(collection: dict, key) -> None:
    collection.pop(key)
    print(collection)

def get(collection: dict, key) -> None :
    print(collection.get(key))

def check(collection: dict, target) -> bool:
    values = list(collection.values())
    for i in values:
        if target == i:
            return True
        else:
            continue
    return False

def main():
    user = "your_username@gmail.com"
    key = "your_key"
    users = {
        1: "ivan@mail.com",
        2: "petr@mail.com",
        3: "anna@mail.com"
    }
    add(users, user, key)
    print("\n")
    rm(users, key)
    print("\n")
    get(users, 1)
    print("\n")
    check(users, 1)
    print(f"\n {check(users, "anna@mail.com")} ")

if __name__ == "__main__":
    main()