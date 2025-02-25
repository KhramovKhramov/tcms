from rest_framework.exceptions import ValidationError

from apps.training_process.models import GroupApplication
from apps.training_process.models.choices import GroupApplicationStatus


class GroupApplicationRejectService:
    """Сервис отклонения заявок на присоединение к группе."""

    def __init__(
        self, group_application: GroupApplication, reject_reason: str
    ) -> None:
        """
        :param group_application: Пользователь.
        :param reject_reason: Причина отклонения заявки.
        """

        self._application = group_application
        self._reject_reason = reject_reason

    def execute(self) -> GroupApplication:
        self._validate()

        return self._reject_application()

    def _validate(self) -> None:
        """Валидация."""

        self._validate_status()

    def _validate_status(self):
        """Валидация статуса заявки."""

        if not self._application.status == GroupApplicationStatus.NEW:
            raise ValidationError(
                'Отклонять можно только заявки в статусе "Новая"'
            )

    def _reject_application(self) -> GroupApplication:
        """Редактирование заявки."""

        self._application.status = GroupApplicationStatus.REJECT
        self._application.reject_reason = self._reject_reason
        self._application.save(update_fields=['status', 'reject_reason'])

        return self._application
