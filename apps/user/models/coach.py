from django.db import models

from apps.user.models.choices import CoachPosition, JudgeCategory
from apps.user.models.managers import CoachManager


class Coach(models.Model):
    """Модель роли тренера."""

    objects = CoachManager()

    user = models.ForeignKey(
        to='user.User',
        on_delete=models.PROTECT,
        verbose_name='Пользователь',
        related_name='coaches',
    )

    # TODO Можно вынести в миксин

    date_from = models.DateField(
        verbose_name='Дата назначения роли',
    )
    date_to = models.DateField(
        verbose_name='Дата окончания действия роли',
        blank=True,
        null=True,
    )

    # TODO добавить стаж работы

    position = models.CharField(
        verbose_name='Должность',
        choices=CoachPosition.choices,
        default=CoachPosition.INSTRUCTOR,
    )
    judge_category = models.CharField(
        verbose_name='Судейская категория',
        choices=JudgeCategory.choices,
        blank=True,
        null=True,
    )
    education = models.CharField(
        verbose_name='Образование',
        max_length=300,
        blank=True,
        null=True,
    )
    additional_info = models.TextField(
        verbose_name='Дополнительная информация',
        max_length=5000,
        blank=True,
        null=True,
    )
    achievements = models.TextField(
        verbose_name='Достижения',
        max_length=5000,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

    def __str__(self) -> str:
        return self.user.full_name
