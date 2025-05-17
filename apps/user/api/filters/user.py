from common.mixins import FullNameFilterMixin
from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES


class UserOrderingFilter(filters.OrderingFilter):
    """
    Класс сортировки для модели User.

    Обновляет стандартный OrderingFilter, добавляя к кверисету аннотации.
    """

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        ordering = [
            self.get_ordering_value(param)
            for param in value
            if param not in EMPTY_VALUES
        ]
        return qs.with_full_name_annotation().order_by(*ordering)


class UserFilter(FullNameFilterMixin):
    """Фильтрация и сортировка пользователей."""

    # Фильтры
    email = filters.CharFilter(label='Email', lookup_expr='icontains')
    phone = filters.CharFilter(label='Номер телефона', lookup_expr='icontains')

    # Сортировка
    ordering = UserOrderingFilter(
        fields={'full_name': 'full_name', 'created_at': 'created_at'},
        field_labels={
            'full_name': 'ФИО пользователя',
            'created_at': 'Дата и время регистрации',
        },
    )
