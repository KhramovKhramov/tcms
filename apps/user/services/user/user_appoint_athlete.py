from common.choices import PlayingLevel
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from apps.user.models import Athlete, User


class UserAppointAthleteService:
    """Сервис назначения пользователю роли спортсмена."""

    def __init__(self, user: User, playing_level: PlayingLevel) -> None:
        """
        :param user: Пользователь.
        :param playing_level: Уровень игры спортсмена.
        """

        self._user = user
        self._playing_level = playing_level

    def execute(self) -> Athlete:
        self._validate()

        return self._create_athlete()

    def _validate(self) -> None:
        """Валидация."""

        self._validate_athlete_already_exists()

    def _validate_athlete_already_exists(self) -> None:
        """
        Проверка на существование у пользователя
        действующей роли спортсмена.
        """

        athlete = Athlete.objects.filter(
            user=self._user, date_to__isnull=True
        ).exists()
        if athlete:
            raise ValidationError(
                'У пользователя уже есть действующая роль спортсмена'
            )

    def _create_athlete(self) -> Athlete:
        """Создание сущности спортсмена."""

        return Athlete.objects.create(
            user=self._user,
            date_from=now().date(),
            playing_level=self._playing_level,
        )
