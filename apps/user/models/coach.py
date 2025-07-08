from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now

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

    coach_experience = models.IntegerField(
        verbose_name='Тренерский стаж (полных лет) на дату приема',
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        default=0,
    )

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

    @property
    def current_coach_experience(self) -> int:
        """Расчет общего тренерского стажа."""

        today = now().date()
        delta = relativedelta(today, self.date_from)

        return delta.years + self.coach_experience
