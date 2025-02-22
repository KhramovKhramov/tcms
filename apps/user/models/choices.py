from django.db import models


class GenderType(models.TextChoices):
    """Типы гендера пользователя."""

    MALE = ('male', 'Мужской')
    FEMALE = ('female', 'Женский')


class CoachPosition(models.TextChoices):
    """Типы должностей тренеров."""

    INSTRUCTOR = ('instructor', 'Тренер-преподаватель')
    SENIOR = ('senior', 'Старший тренер')


class JudgeCategory(models.TextChoices):
    """Типы квалификации судей."""

    THIRD = ('third', 'Судья 3-й категории')
    SECOND = ('second', 'Судья 2-й категории')
    FIRST = ('first', 'Судья 1-й категории')
    HIGHEST = ('highest', 'Судья высшей категории')
