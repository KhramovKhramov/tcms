from common.managers import UserFullNameAnnotationMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import (
    ExpressionWrapper,
    F,
    IntegerField,
    QuerySet,
)
from django.utils.timezone import now

from apps.user.models.utils import YearsBetween


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


class CoachQuerySet(QuerySet, UserFullNameAnnotationMixin):
    user_field_name = 'user'

    def with_all_coach_experience_annotation(self):
        """Добавляет на уровне SQL аннотацию с общим тренерским стажем."""

        return self.annotate(
            all_coach_experience=ExpressionWrapper(
                YearsBetween(now().date(), F('date_from'))
                + F('coach_experience'),
                output_field=IntegerField(),
            )
        )


class CoachManager(BaseUserManager):
    """Менеджер для модели тренера."""

    use_in_migrations = True

    def get_queryset(self):
        return CoachQuerySet(
            model=self.model,
            using=self._db,
            hints=self._hints,
        )


class AthleteQuerySet(QuerySet, UserFullNameAnnotationMixin):
    user_field_name = 'user'


class AthleteManager(BaseUserManager):
    """Менеджер для модели тренера."""

    use_in_migrations = True

    def get_queryset(self):
        return AthleteQuerySet(
            model=self.model,
            using=self._db,
            hints=self._hints,
        )
