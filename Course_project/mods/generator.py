import random

from mods.models import ViewDate


EMAIL_DOMAINS = [
    "mail.ru",
    "gmail.com",
    "yandex.ru",
    "bk.ru",
    "outlook.com"
]

SUBSCRIPTIONS = [
    "Basic",
    "Premium",
    "VIP"
]

FILMS = [
    "Интерстеллар",
    "Дюна",
    "Начало",
    "Матрица",
    "Оппенгеймер",
    "Барби",
    "Джокер",
    "Аватар",
    "Титаник",
    "Довод",
    "Гладиатор",
    "Форрест Гамп",
    "Побег из Шоушенка",
    "Бойцовский клуб",
    "Зеленая миля"
]

STATUSES = [
    "Просмотрен",
    "В процессе",
    "Запланирован",
    "Брошен"
]


def generate_users(filename, count):
    with open(filename, "w", encoding="utf-8") as file:
        for i in range(1, count + 1):
            user_id = i
            email = f"user{i}@{random.choice(EMAIL_DOMAINS)}"
            subscription = random.choice(SUBSCRIPTIONS)

            file.write(f"{user_id};{email};{subscription}\n")


def _random_release_date():
    year = random.randint(1990, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    return ViewDate.create(day, month, year)


def generate_views(filename, users_count, views_count):
    with open(filename, "w", encoding="utf-8") as file:
        for _ in range(views_count):
            user_id = random.randint(1, users_count)
            film = random.choice(FILMS)
            status = random.choice(STATUSES)
            release_date = _random_release_date()

            file.write(f"{user_id};{film};{release_date.to_string()};{status}\n")