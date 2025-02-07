from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.functional import cached_property

from apps.person.models.choices import GenderType
from apps.person.models.managers import PersonManager


class Person(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя системы / физического лица."""

    objects = PersonManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'phone']

    # Данные пользователя
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
        db_index=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        db_index=True,
    )
    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
    )
    date_of_birth = models.DateField(
        verbose_name='Дата рождения', db_index=True
    )
    gender = models.CharField(
        verbose_name='Пол',
        choices=GenderType.choices,
        default=GenderType.MALE,
    )

    # Контактная информация
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        db_index=True,
        unique=True,
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        # TODO добавить валидацию номера телефона,
    )

    # Техническая информация
    created_at = models.DateTimeField(
        verbose_name='Дата и время регистрации',
        auto_now_add=True,
    )
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.full_name

    @cached_property
    def full_name(self):
        """Возвращает ФИО пользователя."""

        full_name = (
            f'{self.last_name} {self.first_name} {self.patronymic or ""}'
        )

        return full_name.strip()

    @property
    def is_staff(self):
        """Проперти для панели администратора."""

        return self.is_superuser
