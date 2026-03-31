def simple(digs: list[int]):
    for i in range(len(digs)):
        if 10 <= digs[i] <= 99:
            digs[i] = 0
    print(digs)

def enum(digs: list[int]):
    for i, d in enumerate(digs):
        if 10 <= d <= 99:
            digs[i] = 0
    print(digs)
def main():
    digs = [4,3,100,-53,-30,1,34,-8]
    simple(digs)
    enum(digs)
if __name__ == "__main__":
    main()