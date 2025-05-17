from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from apps.user.models import Administrator


class CancelAdministratorService:
    """Сервис окончания действия роли администратора."""

    def __init__(self, administrator: Administrator) -> None:
        """
        :param administrator: Администратор.
        """

        self._administrator = administrator

    def execute(self) -> Administrator:
        self._validate()

        return self._cancel_administrator()

    def _validate(self) -> None:
        """Валидация."""

        self._validate_cancelled_administrator()

    def _validate_cancelled_administrator(self) -> None:
        """Проверка, точно ли роль администратора - действующая."""

        if self._administrator.date_to is not None:
            raise ValidationError(
                'Роль данного администратора уже не является действующей'
            )

    def _cancel_administrator(self) -> Administrator:
        """
        Обновление объекта в таблице администраторов - в поле date_to
        ставится текущая дата.
        """

        self._administrator.date_to = now().date()
        self._administrator.save(update_fields=['date_to'])

        return self._administrator
