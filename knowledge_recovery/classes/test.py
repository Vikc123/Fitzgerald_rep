# from __future__ import annotations
# class A:
#     def __init__(self, data ,a: A | None = None):
#         self.data = data
#         self.a = a
class A:
    def __init__(self, value):
        self.value = value

class B:
    def __init__(self, value):
        self.value = value


def main():
    a = A(5)
    b = B(6)
    print(a < b)
    # pt = A(10)
    # print(pt.data)
    # print(pt.a)

if __name__ == "__main__":
    main()