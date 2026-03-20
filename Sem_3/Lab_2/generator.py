import random
from datetime import datetime, timedelta

def generate_russian_names(count):
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
            first = random.choice(first_names_m)
            last = random.choice(last_names)
            middle = random.choice(middle_names_m)
        else:
            first = random.choice(first_names_f)
            last = random.choice(last_names) + 'a'
            middle = random.choice(middle_names_f)
        names.append(f"{last} {first} {middle}")
    return names

def generate_dates(count):
    start_date = datetime(1990, 1, 1)
    end_date = datetime(2026, 12, 31)

    dates = []

    for i in range(count):
        random_date = start_date + timedelta(
            days = random.randint(0, (end_date - start_date).days)
        )
        dates.append(random_date.strftime("%d.%m.%Y"))
    return dates

def generate_file(filename, count):
    with open(filename, "a") as f:
        f.write("fio;date;num")
    dates = generate_dates(count)
    names = generate_russian_names(count)
    with open(filename,'a', encoding= 'utf-8') as f:
        for i in range(count):
            f.write(f"{names[i]};{dates[i]};{i}\n")

def main():
    print(generate_russian_names(3))
    print(generate_dates(3))
    generate_file("data/input/10k_dataset.csv", 10000)

if __name__ == "__main__":
    main()