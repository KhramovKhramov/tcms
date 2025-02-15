from common.managers import UserFullNameAnnotationMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import QuerySet


class UserQuerySet(QuerySet, UserFullNameAnnotationMixin):
    user_field_name = None


class UserManager(BaseUserManager):
    """Менеджер для модели пользователя."""

    use_in_migrations = True

    def get_queryset(self):
        return UserQuerySet(
            model=self.model,
            using=self._db,
            hints=self._hints,
        )

    def create_user(self, email, password=None, **kwargs):
        """Создание учетной записи пользователя."""

        if email is None:
            raise TypeError('У пользователя должен быть указан email.')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        """Создание учетной записи суперюзера."""

        kwargs.setdefault('is_superuser', True)

        if password is None:
            raise TypeError('У суперюзера должен быть пароль.')

        return self.create_user(email, password, **kwargs)


class AdministratorQuerySet(QuerySet, UserFullNameAnnotationMixin):
    user_field_name = 'user'


class AdministratorManager(BaseUserManager):
    """Менеджер для модели администратора."""

    use_in_migrations = True

    def get_queryset(self):
        return AdministratorQuerySet(
            model=self.model,
            using=self._db,
            hints=self._hints,
        )
