from __future__ import annotations
class A:
    def __init__(self, data ,a: A | None = None):
        self.data = data
        self.a = a


def main():
    pt = A(10)
    print(pt.data)
    print(pt.a)

if __name__ == "__main__":
    main()