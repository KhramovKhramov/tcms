from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

from apps.user.models import Coach, User


class CoachWithUserCreateService:
    """
    Сервис создания роли тренера
    вместе с новым для системы пользователем.
    """

    def __init__(self, user_data: dict, **coach_data: dict) -> None:
        """
        :param user_data: Данные для создания пользователя.
        :param coach_data: Данные для создания роли тренера.
        """

        self._user_data = user_data
        self._coach_data = coach_data

    def execute(self) -> Coach:
        """Создание пользователя и роли тренера."""

        user = self._create_user()

        return self._create_coach(user)

    def _create_user(self) -> User:
        """Создание пользователя."""

        return User.objects.create(
            **self._user_data, password=make_password(str(uuid4()))
        )

    def _create_coach(self, user: User) -> Coach:
        """
        Создание роли тренера.

        :param user: Пользователь, которому назначается роль спортсмена.
        """

        return Coach.objects.create(
            user=user,
            date_from=now().date(),
            **self._coach_data,
        )
