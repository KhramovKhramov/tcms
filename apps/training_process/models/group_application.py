from django.db import models

from apps.training_process.models.choices import (
    GroupApplicationStatus,
    PlayingLevel,
)


class GroupApplication(models.Model):
    """Модель заявки на присоединение к тренировочной группе."""

    user = models.ForeignKey(
        to='user.User',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='group_applications',
    )
    group = models.ForeignKey(
        to='training_process.Group',
        verbose_name='Группа',
        on_delete=models.CASCADE,
        related_name='group_applications',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата и время подачи заявки',
        auto_now_add=True,
    )
    status = models.CharField(
        verbose_name='Статус заявки',
        choices=GroupApplicationStatus.choices,
        blank=True,
        default=GroupApplicationStatus.NEW,
    )
    playing_level = models.CharField(
        verbose_name='Уровень занимающихся',
        choices=PlayingLevel.choices,
    )
    comment = models.CharField(
        verbose_name='Комментарий к заявке',
        max_length=1500,
        blank=True,
        null=True,
    )
    reject_reason = models.CharField(
        verbose_name='Причина отклонения заявки',
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Заявка на присоединение к группе'
        verbose_name_plural = 'Заявки на присоединение к группе'

    def __str__(self) -> str:
        return (
            f'Заявка с id {self.pk} пользователя {self.user.full_name} '
            f'в группу {self.group.name} '
            f'в статусе {self.status}'
        )
