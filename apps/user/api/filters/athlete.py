from common.mixins import FullNameFilterMixin
from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES


class AthleteOrderingFilter(filters.OrderingFilter):
    """
    Класс сортировки для модели Athlete.

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


class AthleteFilter(FullNameFilterMixin):
    """Фильтрация и сортировка спортсменов."""

    # Фильтры
    group_id = filters.NumberFilter(
        label='Группа', field_name='groups__id', lookup_expr='exact'
    )

    # Сортировка
    ordering = AthleteOrderingFilter(
        fields={
            'full_name': 'full_name',
        },
        field_labels={
            'full_name': 'ФИО пользователя',
        },
    )
