from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from apps.user.models import Coach


class CancelCoachService:
    """Сервис окончания действия роли тренера."""

    def __init__(self, coach: Coach) -> None:
        """
        :param coach: Тренер.
        """

        self._coach = coach

    def execute(self) -> Coach:
        self._validate()

        return self._cancel_coach()

    def _validate(self) -> None:
        """Валидация."""

        self._validate_cancelled_coach()
        # TODO добавить проверку - если есть действующие группы,
        #  надо сначала заменить в них тренера

    def _validate_cancelled_coach(self) -> None:
        """Проверка, точно ли роль тренера - действующая."""

        if self._coach.date_to is not None:
            raise ValidationError(
                'Роль данного тренера уже не является действующей'
            )

    def _cancel_coach(self) -> Coach:
        """
        Обновление объекта в таблице тренеров - в поле date_to
        ставится текущая дата.
        """

        self._coach.date_to = now().date()
        self._coach.save(update_fields=['date_to'])

        return self._coach
