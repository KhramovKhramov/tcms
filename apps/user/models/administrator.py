from django.db import models

from apps.user.models.managers import AdministratorManager


class Administrator(models.Model):
    """Модель роли администратора."""

    objects = AdministratorManager()

    user = models.ForeignKey(
        to='user.User',
        on_delete=models.PROTECT,
        verbose_name='Пользователь',
        related_name='administrators',
    )

    date_from = models.DateField(
        verbose_name='Дата назначения роли',
    )
    date_to = models.DateField(
        verbose_name='Дата окончания действия роли',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'администратор'
        verbose_name_plural = 'администраторы'

    def __str__(self) -> str:
        return self.user.full_name
