from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

from apps.user.models import Administrator, User


class AdministratorWithUserCreateService:
    """
    Сервис создания роли администратора
    вместе с новым для системы пользователем.
    """

    def __init__(self, user_data: dict) -> None:
        """
        :param user_data: Данные для создания пользователя.
        """

        self._user_data = user_data

    def execute(self) -> Administrator:
        """Создание пользователя и роли администратора."""

        user = self._create_user()

        return self._create_administrator(user)

    def _create_user(self) -> User:
        """Создание пользователя."""

        return User.objects.create(
            **self._user_data, password=make_password(str(uuid4()))
        )

    @staticmethod
    def _create_administrator(user: User) -> Administrator:
        """
        Создание роли администратора.

        :param user: Пользователь, которому назначается роль администратора.
        """

        return Administrator.objects.create(
            user=user,
            date_from=now().date(),
        )
