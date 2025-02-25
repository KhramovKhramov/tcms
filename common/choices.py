from django.db import models


class Weekdays(models.TextChoices):
    """Дни недели."""

    MONDAY = ('monday', 'Понедельник')
    TUESDAY = ('tuesday', 'Вторник')
    WEDNESDAY = ('wednesday', 'Среда')
    THURSDAY = ('thursday', 'Четверг')
    FRIDAY = ('friday', 'Пятница')
    SATURDAY = ('saturday', 'Суббота')
    SUNDAY = ('sunday', 'Воскресенье')


class PlayingLevel(models.TextChoices):
    """Типы уровней занимающихся спортсменов."""

    BEGINNER = ('beginner', 'Начинающий')
    PLAYER = ('player', 'Играющий')
    PRO = ('pro', 'Профессионал')
