from rest_framework.exceptions import ValidationError

from apps.training_process.models import GroupApplication
from apps.training_process.models.choices import GroupApplicationStatus
from apps.user.models import Athlete
from apps.user.services import UserAppointAthleteService


class GroupApplicationApproveService:
    """Сервис одобрения заявок на присоединение к группе."""

    def __init__(self, group_application: GroupApplication) -> None:
        """
        :param group_application: Заявка на присоединение к группе.
        """

        self._application = group_application

    def execute(self) -> GroupApplication:
        self._validate()
        self._joining_athlete_to_group()

        return self._approve_application()

    def _validate(self) -> None:
        """Валидация."""

        self._validate_status()

    def _validate_status(self):
        """Валидация статуса заявки."""

        if not self._application.status == GroupApplicationStatus.NEW:
            raise ValidationError(
                'Одобрять можно только заявки в статусе "Новая"'
            )

    def _joining_athlete_to_group(self) -> None:
        """Присоединение спортсмена к группе."""

        # Если у пользователя нет действующей роли спортсмена, она создается
        # TODO если у спортсмена была действующая роль, надо менять ей level
        athlete = (
            Athlete.objects.filter(
                user=self._application.user, date_to__isnull=True
            ).first()
            or UserAppointAthleteService(
                user=self._application.user,
                playing_level=self._application.playing_level,
            ).execute()
        )

        athlete.groups.add(self._application.group)

    def _approve_application(self) -> GroupApplication:
        """Редактирование заявки."""

        self._application.status = GroupApplicationStatus.APPROVED
        self._application.save(update_fields=['status'])

        return self._application
