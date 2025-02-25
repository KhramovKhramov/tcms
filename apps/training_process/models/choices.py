from django.db import models


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
