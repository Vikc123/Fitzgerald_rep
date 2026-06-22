from dataclasses import dataclass


@dataclass
class UserRecord:
    user_id: int
    email: str
    subscription: str

    @classmethod
    def from_line(cls, line: str) -> "UserRecord":
        parts = [p.strip() for p in line.split(";")]

        if len(parts) != 3:
            raise ValueError("Пользователь должен иметь 3 поля: ID;Email;Вид подписки")

        user_id_str, email, subscription = parts

        if not user_id_str.isdigit():
            raise ValueError("ID пользователя должен быть числом")

        if not email:
            raise ValueError("Email не может быть пустым")

        if not subscription:
            raise ValueError("Вид подписки не может быть пустым")

        return cls(
            user_id=int(user_id_str),
            email=email,
            subscription=subscription
        )

    def to_line(self) -> str:
        return f"{self.user_id};{self.email};{self.subscription}"


@dataclass
class ViewRecord:
    user_id: int
    film: str
    year: int
    status: str

    @classmethod
    def from_line(cls, line: str) -> "ViewRecord":
        parts = [p.strip() for p in line.split(";")]

        if len(parts) != 4:
            raise ValueError("Просмотр должен иметь 4 поля: ID;Фильм;Год;Статус")

        user_id_str, film, year_str, status = parts

        if not user_id_str.isdigit():
            raise ValueError("ID пользователя должен быть числом")

        if not film:
            raise ValueError("Название фильма не может быть пустым")

        if not year_str.isdigit():
            raise ValueError("Год выпуска должен быть числом")

        if not status:
            raise ValueError("Статус не может быть пустым")

        return cls(
            user_id=int(user_id_str),
            film=film,
            year=int(year_str),
            status=status
        )

    def to_line(self) -> str:
        return f"{self.user_id};{self.film};{self.year};{self.status}"