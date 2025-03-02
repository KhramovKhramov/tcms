from common.managers import UserFullNameAnnotationMixin
from django.db.models import Manager, QuerySet


class GroupApplicationQuerySet(QuerySet, UserFullNameAnnotationMixin):
    user_field_name = 'user'


class GroupApplicationManager(Manager):
    """Менеджер для модели заявок на присоединение к группе."""

    use_in_migrations = True

    def get_queryset(self):
        return GroupApplicationQuerySet(
            model=self.model,
            using=self._db,
            hints=self._hints,
        )
