from common.choices import Weekdays
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from django.db import models

from apps.training_process.models.choices import PlayingLevel


class Group(models.Model):
    """Модель тренировочной группы."""

    name = models.CharField(
        verbose_name='Наименование',
        max_length=300,
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=3000,
        blank=True,
        null=True,
    )
    coach = models.ForeignKey(
        to='user.Coach',
        verbose_name='Тренер',
        on_delete=models.PROTECT,
        related_name='groups',
    )
    min_participants = models.PositiveSmallIntegerField(
        verbose_name='Минимальное количество спортсменов',
        default=6,
    )
    max_participants = models.PositiveSmallIntegerField(
        verbose_name='Максимальное количество спортсменов',
        validators=[MaxValueValidator(12)],
        default=12,
    )
    playing_level = models.CharField(
        verbose_name='Уровень занимающихся',
        choices=PlayingLevel.choices,
    )
    training_days = ArrayField(
        base_field=models.CharField(
            choices=Weekdays.choices,
        ),
        verbose_name='Дни тренировок',
    )
    training_time = models.CharField(
        verbose_name='Время тренировок',
        max_length=50,
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.name

    # TODO добавить расчет актуальной заполненности группы
