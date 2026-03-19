# from accessify import private
class Point:
    def __init__(self, x, y):
        self.__x = self.__y = 0
        if self.__check(x) and self.__check(y):
            self.__x = x
            self.__y = y
    # @private#нормальная инкапсуляция
    @classmethod
    def __check(cls, x):
        return type(x) in (int, float)

    def set_coord(self, x, y):
        if  self.__check(x) and self.__check(y):
            self.__x = x
            self.__y = y
    def get_coord(self):
        return self.__x, self.__y

def main():
    x = Point(1,2)
    # print(x.__x) ## не можем обратиться так как объект инкапсулирован
    print()
    print(x.get_coord())

if __name__ == '__main__':
    main()