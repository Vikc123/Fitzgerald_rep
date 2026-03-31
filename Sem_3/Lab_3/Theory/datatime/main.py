import datetime
def main():
    my_time = datetime.time(10, 33, 23, 3)
    print(my_time) #time подкласс класса datatime и через него можно обращаться к его атрибутам

    day = datetime.date(1830, 3, 2)
    print(day)

if __name__ == "__main__":
    main()