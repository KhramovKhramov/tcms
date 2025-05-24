from typing import Any

from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from apps.user.models import Coach, User


class UserAppointCoachService:
    """Сервис назначения пользователю роли тренера."""

    def __init__(self, user: User, data: dict[str, Any]) -> None:
        """
        :param user: Пользователь.
        :param data: Данные для роли тренера.
        """

        self._user = user
        self._data = data

    def execute(self) -> Coach:
        self._validate()

        return self._create_coach()

    def _validate(self) -> None:
        """Валидация."""

        self._validate_coach_already_exists()

    def _validate_coach_already_exists(self) -> None:
        """
        Проверка на существование у пользователя
        действующей роли тренера.
        """

        coach = Coach.objects.filter(
            user=self._user, date_to__isnull=True
        ).exists()
        if coach:
            raise ValidationError(
                'У пользователя уже есть действующая роль тренера'
            )

    def _create_coach(self) -> Coach:
        """Создание сущности тренера."""

        return Coach.objects.create(
            user=self._user,
            date_from=now().date(),
            **self._data,
        )
