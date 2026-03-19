# class Point:
#     def __new__(cls, *args, **kwargs):
#         print("Вызван метод __new__ для объекта: " + str(cls))
#         return super().__new__(cls)
#     def __init__(self, x = 0, y = 0):
#         print("Вызван конструктор")
#         self.x = x
#         self.y = y
class DataBase:
    __instans = None
    def __new__(cls, *args, **kwargs):
        if cls.__instans is None:
            cls.__instans = super().__new__(cls)
        return cls.__instans
    def __del__(self):
        DataBase.__instans = None
    def init(self, user, psw, port):
        self.user = user
        self.psw = psw
        self.port = port
    def conect(self):
        print(f"соединение с БД: {self.user}, {self.port}, {self.psw}")
    def close(self):
        print("Закрытие соединения с БД")
    def read(self):
        print("Данные из БД")
    def write(self, data):
        print(f"запись данных в БД {data}")
def main():
    db = DataBase('root', '80', '1234')
    db2 = DataBase('root2', '40', '5678')
    print(id(db), id(db))

    # pt = Point()
    # print(pt)

if __name__ == "__main__":
    main()