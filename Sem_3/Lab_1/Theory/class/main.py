# class Point:
#     pass #залушка можно так же использовать и в других конструкциях

class Point:
    color = "red" #поля называем атрибутами
    circle = 2

def main():
    print(Point.color)
    print(Point.circle)
    print(Point.__dict__) #вывод всех атрибутов класса
    a = Point()
    b = Point()
    # print(a.__dict__) #ничего не выводится так как не был вызван конструктор класса, а просто был присвоен тип переменной
    # print(b.__dict__)
    print(type(a))
    a.color = 'black'#присвоили собственное значение атрибуту экземпляра а
    print(a.__dict__)
    setattr(Point, 'prop', 1) #создали новый атрибут в классе
    print(getattr(Point, 'prop'))#получили значение атрибута
    del Point.prop#удалили атрибут
    print(Point.__dict__)

if __name__ == "__main__":
    main()