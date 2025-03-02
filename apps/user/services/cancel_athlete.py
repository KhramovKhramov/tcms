from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from apps.user.models import Athlete


class CancelAthleteService:
    def __init__(self, athlete: Athlete):
        self._athlete = athlete

    def execute(self) -> Athlete:
        self._validate()

        return self._cancel_athlete()

    def _validate(self):
        """Валидация."""

        self._validate_cancelled__athlete()

    def _validate_cancelled__athlete(self):
        """Проверка, точно ли роль спортсмена - действующая."""

        if self._athlete.date_to is not None:
            raise ValidationError(
                'Роль данного спортсмена уже не является действующей'
            )

    def _cancel_athlete(self) -> Athlete:
        """
        Обновление объекта в таблице спортсменов - в поле date_to
        ставится текущая дата.
        """

        self._athlete.date_to = now().date()
        self._athlete.save(update_fields=['date_to'])

        return self._athlete
