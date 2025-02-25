from django.db import models


class PlayingLevel(models.TextChoices):
    """Типы уровней занимающихся спортсменов."""

    BEGINNER = ('beginner', 'Начинающий')
    PLAYER = ('player', 'Играющий')
    PRO = ('pro', 'Профессионал')


class GroupStatus(models.TextChoices):
    """Статусы группы."""

    FUTURE = ('future', 'Будущая')
    ACTIVE = ('active', 'Действующая')
    FINISHED = ('finished', 'Закончившаяся')


class GroupApplicationStatus(models.TextChoices):
    """Статусы заявки на присоединение к группе."""

    NEW = ('new', 'Новая')
    APPROVED = ('approved', 'Подтвержденная')
    REJECT = ('reject', 'Отклоненная')
