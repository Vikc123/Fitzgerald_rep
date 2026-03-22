def sheyker(mass):
    low = 1
    up = len(mass)
    last = 0
    k = 0
    while (low < up):
        for i in range(low, up):
            if (mass[i] > mass[i - 1]):
                buff = mass[i]
                mass[i] = mass[i - 1]
                mass[i - 1] = buff
                last = i
            else:
                continue
        up = last
        last = 0
        for i in range(up, low, -1):
            if (mass[i] > mass[i - 1]):
                buff = mass[i]
                mass[i] = mass[i - 1]
                mass[i - 1] = buff
                last = i
            else:
                continue
        low = last
        last = 0
        k += 1
    return mass
def main():
    mass = [32, 4, 12, 43, 17, 9, 25, 21]
    print(sheyker(mass))

if __name__ == "__main__":
    main()