from uuid import uuid4

from common.choices import PlayingLevel
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

from apps.user.models import Athlete, User


class AthleteWithUserCreateService:
    """
    Сервис создания роли спортсмена
    вместе с новым для системы пользователем.
    """

    def __init__(self, user_data: dict, playing_level: PlayingLevel) -> None:
        """
        :param user_data: Данные для создания пользователя.
        :param playing_level: Уровень спортсмена.
        """

        self._user_data = user_data
        self._playing_level = playing_level

    def execute(self) -> Athlete:
        """Создание пользователя и роли спортсмена."""

        user = self._create_user()

        return self._create_athlete(user)

    def _create_user(self) -> User:
        """Создание пользователя."""

        return User.objects.create(
            **self._user_data, password=make_password(str(uuid4()))
        )

    def _create_athlete(self, user: User) -> Athlete:
        """
        Создание роли спортсмена.

        :param user: Пользователь, которому назначается роль спортсмена.
        """

        return Athlete.objects.create(
            user=user,
            playing_level=self._playing_level,
            date_from=now().date(),
        )
