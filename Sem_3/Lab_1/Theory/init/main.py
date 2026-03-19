class Point:
    x = 0
    y = 0
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def set_coords(self, x, y):
        self.x = x
        self.y = y
    def get_coords(self):
        print((self.x, self.y))
    def __del__(self):
        print("вызвался деструктор")
def main():
    a = Point(10,19)
    a.get_coords()

if __name__ == '__main__':
    main()