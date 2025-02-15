from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES


class AdministratorOrderingFilter(filters.OrderingFilter):
    """
    Класс сортировки для модели Administrator.

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


class AdministratorFilter(filters.FilterSet):
    """Фильтрация и сортировка администраторов."""

    # Фильтры
    full_name = filters.CharFilter(
        label='ФИО пользователя', method='full_name_filter'
    )

    def full_name_filter(self, qs, name, value):
        """Фильтрация по ФИО пользователя."""

        return qs.with_full_name_annotation().filter(
            full_name__icontains=value,
        )

    # Сортировка
    ordering = AdministratorOrderingFilter(
        fields={
            'full_name': 'full_name',
        },
        field_labels={
            'full_name': 'ФИО пользователя',
        },
    )
