from dataclasses import dataclass


MIN_YEAR = 1900
MAX_YEAR = 2100

MONTH_NAMES_RU = [
    "янв", "фев", "мар", "апр", "май", "июн",
    "июл", "авг", "сен", "окт", "ноя", "дек"
]

_DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _max_day(month, year):
    if month == 2 and _is_leap_year(year):
        return 29

    return _DAYS_IN_MONTH[month - 1]


@dataclass
class ViewDate:
    day: int
    month: int
    year: int

    @classmethod
    def create(cls, day, month, year) -> "ViewDate":
        if not isinstance(month, int) or not (1 <= month <= 12):
            raise ValueError("Месяц должен быть от 1 до 12")

        if not isinstance(year, int) or not (MIN_YEAR <= year <= MAX_YEAR):
            raise ValueError(f"Год должен быть от {MIN_YEAR} до {MAX_YEAR}")

        max_day = _max_day(month, year)

        if not isinstance(day, int) or not (1 <= day <= max_day):
            raise ValueError(
                f"В месяце {MONTH_NAMES_RU[month - 1]}.{year} не может быть дня {day}"
            )

        return cls(day=day, month=month, year=year)

    def to_string(self) -> str:
        return f"{self.day:02d} {MONTH_NAMES_RU[self.month - 1]} {self.year}"

    def to_number(self) -> int:
        return self.year * 10000 + self.month * 100 + self.day

    @classmethod
    def from_string(cls, text: str) -> "ViewDate":
        parts = text.strip().split()

        if len(parts) != 3:
            raise ValueError(f"Дата должна быть в формате 'DD мес YYYY', получено: '{text}'")

        day_str, month_str, year_str = parts

        if not day_str.isdigit():
            raise ValueError("День в дате должен быть числом")

        if month_str not in MONTH_NAMES_RU:
            raise ValueError(f"Неизвестное название месяца в дате: '{month_str}'")

        if not year_str.isdigit():
            raise ValueError("Год в дате должен быть числом")

        month = MONTH_NAMES_RU.index(month_str) + 1

        return cls.create(int(day_str), month, int(year_str))


@dataclass
class UserRecord:
    user_id: int
    email: str
    subscription: str

    @classmethod
    def create(cls, user_id, email, subscription) -> "UserRecord":
        email = email.strip()
        subscription = subscription.strip()

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("ID пользователя должен быть положительным числом")

        if not email:
            raise ValueError("Email не может быть пустым")

        if not subscription:
            raise ValueError("Вид подписки не может быть пустым")

        return cls(user_id=user_id, email=email, subscription=subscription)

    @classmethod
    def from_line(cls, line: str) -> "UserRecord":
        parts = [p.strip() for p in line.split(";")]

        if len(parts) != 3:
            raise ValueError("Пользователь должен иметь 3 поля: ID;Email;Вид подписки")

        user_id_str, email, subscription = parts

        if not user_id_str.isdigit():
            raise ValueError("ID пользователя должен быть числом")

        return cls.create(int(user_id_str), email, subscription)

    def to_line(self) -> str:
        return f"{self.user_id};{self.email};{self.subscription}"


@dataclass
class ViewRecord:
    user_id: int
    film: str
    release_date: ViewDate
    status: str

    @classmethod
    def create(cls, user_id, film, release_date, status) -> "ViewRecord":
        film = film.strip()
        status = status.strip()

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("ID пользователя должен быть положительным числом")

        if not film:
            raise ValueError("Название фильма не может быть пустым")

        if not isinstance(release_date, ViewDate):
            raise ValueError("Дата выпуска должна быть указана")

        if not status:
            raise ValueError("Статус не может быть пустым")

        return cls(user_id=user_id, film=film, release_date=release_date, status=status)

    @classmethod
    def from_line(cls, line: str) -> "ViewRecord":
        parts = [p.strip() for p in line.split(";")]

        if len(parts) != 4:
            raise ValueError("Просмотр должен иметь 4 поля: ID;Фильм;Дата выпуска;Статус")

        user_id_str, film, date_str, status = parts

        if not user_id_str.isdigit():
            raise ValueError("ID пользователя должен быть числом")

        release_date = ViewDate.from_string(date_str)

        return cls.create(int(user_id_str), film, release_date, status)

    def to_line(self) -> str:
        return f"{self.user_id};{self.film};{self.release_date.to_string()};{self.status}"