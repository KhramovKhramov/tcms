from django.db import models


class GenderType(models.TextChoices):
    """Типы гендера пользователя."""

    MALE = ('male', 'Мужской')
    FEMALE = ('female', 'Женский')
