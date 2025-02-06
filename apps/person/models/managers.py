from django.contrib.auth.base_user import BaseUserManager


class PersonManager(BaseUserManager):
    use_in_migrations = True

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