from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES


class GroupApplicationOrderingFilter(filters.OrderingFilter):
    """
    Класс сортировки для модели GroupApplication.

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


class GroupApplicationFilter(filters.FilterSet):
    """Фильтрация и сортировка заявок на присоединение к группе."""

    # Фильтры
    full_name = filters.CharFilter(
        label='ФИО пользователя', method='full_name_filter'
    )
    user_id = filters.NumberFilter(
        label='id пользователя',
        field_name='user_id',
        lookup_expr='exact',
    )
    group_id = filters.NumberFilter(
        label='id группы',
        field_name='group_id',
        lookup_expr='exact',
    )

    def full_name_filter(self, qs, name, value):
        """Фильтрация по ФИО пользователя, подавшего заявку."""

        return qs.with_full_name_annotation().filter(
            full_name__icontains=value,
        )

    # Сортировка
    ordering = GroupApplicationOrderingFilter(
        fields={'full_name': 'full_name', 'created_at': 'created_at'},
        field_labels={
            'full_name': 'ФИО пользователя, подавшего заявку',
            'created_at': 'Дата и время подачи заявки',
        },
    )
