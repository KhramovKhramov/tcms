from common.choices import PlayingLevel
from django.db import models

from apps.user.models.managers import AthleteManager


class Athlete(models.Model):
    """Модель спортсмена."""

    objects = AthleteManager()

    user = models.ForeignKey(
        to='user.User',
        on_delete=models.PROTECT,
        verbose_name='Пользователь',
        related_name='athletes',
    )

    groups = models.ManyToManyField(
        to='training_process.Group',
        verbose_name='Группы',
        related_name='athletes',
        blank=True,
    )

    date_from = models.DateField(
        verbose_name='Дата назначения роли',
    )
    date_to = models.DateField(
        verbose_name='Дата окончания действия роли',
        blank=True,
        null=True,
    )

    playing_level = models.CharField(
        verbose_name='Уровень',
        choices=PlayingLevel.choices,
    )

    class Meta:
        verbose_name = 'Спортсмен'
        verbose_name_plural = 'Спортсмены'

    def __str__(self) -> str:
        return self.user.full_name
