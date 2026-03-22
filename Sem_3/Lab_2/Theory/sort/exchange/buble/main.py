def buble(mass):
    for i in range(0, len(mass)):
        for j in range(1, len(mass)):
            if(mass[j] < mass[j-1]):
                buff = mass[j-1]
                mass[j-1] = mass[j]
                mass[j] = buff
            else:
                continue
    return mass
def main():
    mass = [32, 4, 12, 43, 17, 9, 25, 21]
    print(buble(mass))
if __name__ == "__main__":
    main()