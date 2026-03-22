import random
def quick_sort(mass):
    if mass.__len__() > 1:
        pivot = mass[random.randint(0, mass.__len__()-1)]
        less = [i for i in mass if i < pivot]
        eq = [i for i in mass if i == pivot]
        hight = [i for i in mass if i > pivot]
        mass = quick_sort(less) + eq + quick_sort(hight)
    return mass

def main():
    data = [6,2,7,3,1,8,5,4]
    print(quick_sort(data))

if __name__ == "__main__":
    main()