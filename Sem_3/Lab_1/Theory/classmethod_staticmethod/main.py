class Vector:
    MIN_VALUE = 0
    MAX_VALUE = 100
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @classmethod
    def validate(cls, arg):
        return cls.MIN_VALUE <= arg <= cls.MAX_VALUE

    def get_coord(self):
        return self.x, self.y

def main():
    v = Vector(1,2)
    print(Vector.validate(5))
    res = v.get_coord()
    print(res)

if __name__ == "__main__":
    main()
