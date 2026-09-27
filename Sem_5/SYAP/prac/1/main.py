import random

class A:
    def _generate_first(self, count_of_generation):
        first = []
        for i in range(count_of_generation):
            first.append(random.randint(i, 100))
        return first

    def _generate_second(self, count_of_generation):
        second = []
        for i in range(count_of_generation):
            second.append(random.randint(i, 100))
        return second

    def generate_file(self, count_of_generate: int):

        first = A._generate_first(self, count_of_generate)
        second = A._generate_second(self, count_of_generate)

        with open("data/test.txt", "w") as f:
            for i in range(count_of_generate):
                f.write(f"{first[i]}_{second[i]}\n")

    def _rewrite(self, data: list):
        if data.__len__()%2 == 0:
            for i in range(1, data.__len__(), 2):
                buff = data[i-1]
                data[i-1] = data[i]
                data[i] = buff
        else:
            for i in range(1, data.__len__()-1, 2):
                buff = data[i-1]
                data[i-1] = data[i]
                data[i] = buff
        return data

    def rewrite(self):
        data = []
        with open("data/test.txt", 'r') as f:
            for i in f:
                data.append(i)
        rdata = A._rewrite(self, data)
        with open("data/test.txt", 'w') as f:
            for i in range(rdata.__len__()):
                f.write(rdata[i])


#работа с файлами и 3 принципа ооп
def main():
    a = A()
    # a.generate_file(7)
    a.rewrite()
    pass

if __name__ == "__main__":
    main()