import random

def random_int():
    x = random.randint(1, 10)
    print(x)

def random_float():
    x = random.uniform(1, 10)
    print(x)

def random_of_collection():
    names = ["Ivan", "Petr", "Alex"]
    name = random.choice(names)
    print(name)

def main():
    random_int()
    random_float()
    random_of_collection()
    

if __name__ == "__main__":
    main()


