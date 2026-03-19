class Point:
    x = 0
    y = 0
    def set_coords(self, x, y):
        self.x = x
        self.y = y
    def get_coords(self):
        return (self.x, self.y)
def main():
    a = Point()
    a.set_coords(10, 10)
    print(a.__dict__)
    print(a.get_coords())

if __name__ == '__main__':
    main()