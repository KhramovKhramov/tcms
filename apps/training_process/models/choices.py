from django.db import models


class PlayingLevel(models.TextChoices):
    """Типы уровней занимающихся спортсменов."""

    BEGINNER = ('beginner', 'Начинающий')
    PLAYER = ('player', 'Играющий')
    PRO = ('pro', 'Профессионал')
