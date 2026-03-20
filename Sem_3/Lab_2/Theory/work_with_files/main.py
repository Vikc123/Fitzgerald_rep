# f = open("data/input.txt", 'w')
# f.write("Hello") #w - запись, знак переноса не ставится
# f.write("!!!")

# f = open("data/input.txt", 'a')
# f.write("Hello") #a - дозапись, знак переноса не ставится
# f.write("!!!")

# f = open("data/input.txt", "r")
# print(f.read()) #выводит все содержимое входного файла

# for line in f: # line - каждая строка
#     print(line)


# f.close()



#ключевое слово with...as

with open("data/input.txt", "a") as f:
    for i in range(4):
        f.write("hello\n")

