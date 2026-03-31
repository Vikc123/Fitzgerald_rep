import random
import datetime as dt
def generate_names(count: int)->"list[str]":
    last_names = ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Попов',
                  'Васильев', 'Смирнов', 'Новиков', 'Федоров', 'Морозов',
                  'Волков', 'Алексеев', 'Лебедев', 'Семенов', 'Егоров']

    first_names_m = ['Александр', 'Алексей', 'Андрей', 'Артем', 'Борис',
                     'Вадим', 'Василий', 'Виктор', 'Владимир', 'Дмитрий']

    first_names_f = ['Анна', 'Елена', 'Ольга', 'Ирина', 'Наталья',
                     'Мария', 'Светлана', 'Юлия', 'Татьяна', 'Екатерина']

    middle_names_m = ['Александрович', 'Алексеевич', 'Андреевич', 'Борисович',
                      'Вадимович', 'Васильевич', 'Викторович', 'Владимирович']

    middle_names_f = ['Александровна', 'Алексеевна', 'Андреевна', 'Борисовна',
                      'Вадимовна', 'Васильевна', 'Викторовна', 'Владимировна']
    names = []
    for i in range(count):
        if random.choice([True, False]):
            last = random.choice(last_names)
            first = random.choice(first_names_m)
            middle = random.choice(middle_names_m)
            names.append(f"{last} {first} {middle}")
        else:
            last = random.choice(last_names)+"a"
            first = random.choice(first_names_f)
            middle = random.choice(middle_names_f)
            names.append(f"{last} {first} {middle}")
    return names

def generate_dates(count: int) -> "list[str]":
    start = dt.date(1981, 1, 1)
    end = dt.date(2026, 3, 31)
    dates = []
    for i in range(count):
        day = start + dt.timedelta(days = random.randint(0, (end - start).days))
        dates.append(day.strftime("%d.%m.%Y"))
    return dates

def generate_discrip(count: int) -> list[str]:
        russian_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        russian_letters += russian_letters.upper()
        discription = []
        for i in range(count):
            discription.append(''.join(random.choice(russian_letters) for _ in range(10)))
        return discription

def generate_file(filename: str, count: int) -> None:
    names = generate_names(count)
    dates = generate_dates(count)
    discrips = generate_discrip(count)
    with open(filename, "w") as f:
        f.write("fio; date; num; discp\n")
        for i in range(count):
            f.write(f"{names[i]};{dates[i]};{i};{discrips[i]}\n")
