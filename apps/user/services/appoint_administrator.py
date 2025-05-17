from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from apps.user.models import Administrator, User


class UserAppointAdministratorService:
    """Сервис назначения пользователю роли администратора."""

    def __init__(self, user: User) -> None:
        """
        :param user: Пользователь.
        """

        self._user = user

    def execute(self) -> Administrator:
        self._validate()

        return self._create_administrator()

    def _validate(self) -> None:
        """Валидация."""

        self._validate_administrator_already_exists()

    def _validate_administrator_already_exists(self) -> None:
        """
        Проверка на существование у пользователя
        действующей роли администратора.
        """

        administrator = Administrator.objects.filter(
            user=self._user, date_to__isnull=True
        ).exists()
        if administrator:
            raise ValidationError(
                'У пользователя уже есть действующая роль администратора'
            )

    def _create_administrator(self) -> Administrator:
        """Создание сущности администратора."""

        return Administrator.objects.create(
            user=self._user,
            date_from=now().date(),
        )
